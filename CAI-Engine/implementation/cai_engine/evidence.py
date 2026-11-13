"""Durable, locally verifiable evidence log for the isolated R01-R10 candidate.

Local hash-chain verification establishes integrity of records that remain. It
does not establish historical completeness or authenticity without an external
anchor; callers must report that limit.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager

GENESIS_HASH = "0" * 64
_LOCKS: dict[str, threading.RLock] = {}
_LOCKS_GUARD = threading.Lock()
_LOCK_STATE = threading.local()


class EvidenceBusyError(RuntimeError):
    """The runtime writer lock could not be acquired before its timeout."""


class EvidenceError(RuntimeError):
    """Evidence cannot be safely read or appended."""


def _canonical(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def _record_hash(record_without_hash: dict) -> str:
    return hashlib.sha256(_canonical(record_without_hash)).hexdigest()


def _fsync_directory(path: str) -> None:
    if os.name == "nt":
        return
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class EvidenceLog:
    """Append-only hash-chained JSONL with a cooperating-writer OS lock."""

    def __init__(self, path: str):
        # Preserve the caller's path contract (including relative paths).
        self.path = os.fspath(path)
        self.lock_path = self.path + ".lock"

    @contextmanager
    def writer_lock(self, timeout: float = 2.0):
        key = self.lock_path
        with _LOCKS_GUARD:
            thread_lock = _LOCKS.setdefault(key, threading.RLock())
        if not thread_lock.acquire(timeout=timeout):
            raise EvidenceBusyError("BUSY: evidence writer lock timeout")
        try:
            held = getattr(_LOCK_STATE, "held", None)
            if held is None:
                held = {}
                _LOCK_STATE.held = held
            if key in held:
                held[key]["depth"] += 1
                try:
                    yield
                finally:
                    held[key]["depth"] -= 1
                return

            os.makedirs(os.path.dirname(os.path.abspath(key)), exist_ok=True)
            with open(key, "a+b") as lock_file:
                lock_file.seek(0, os.SEEK_END)
                if lock_file.tell() == 0:
                    lock_file.write(b"\0")
                    lock_file.flush()
                deadline = time.monotonic() + timeout
                while True:
                    try:
                        lock_file.seek(0)
                        if os.name == "nt":
                            import msvcrt
                            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                        else:
                            import fcntl
                            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        break
                    except (OSError, BlockingIOError):
                        if time.monotonic() >= deadline:
                            raise EvidenceBusyError("BUSY: evidence writer lock timeout")
                        time.sleep(0.01)
                held[key] = {"depth": 1, "file": lock_file}
                try:
                    yield
                finally:
                    held.pop(key, None)
                    lock_file.seek(0)
                    if os.name == "nt":
                        import msvcrt
                        msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        finally:
            thread_lock.release()

    def records(self) -> Iterator[dict]:
        if not os.path.exists(self.path):
            return
        with open(self.path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def last_hash(self) -> str:
        prev = GENESIS_HASH
        for rec in self.records():
            prev = rec.get("record_hash", prev)
        return prev

    def count(self) -> int:
        return sum(1 for _ in self.records())

    def append(self, event_type: str, payload: dict) -> dict:
        with self.writer_lock():
            created_log = not os.path.exists(self.path)
            if not created_log:
                valid, error = self.verify()
                if not valid:
                    raise EvidenceError(f"evidence log is not appendable: {error}")
            records = list(self.records()) if not created_log else []
            prev_hash = records[-1]["record_hash"] if records else GENESIS_HASH
            body = {
                "seq": len(records) + 1,
                "timestamp": time.time(),
                "event_type": event_type,
                "prev_hash": prev_hash,
                "payload": payload,
            }
            body["record_hash"] = _record_hash(body)
            parent = os.path.dirname(os.path.abspath(self.path))
            os.makedirs(parent, exist_ok=True)
            flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
            if created_log:
                flags |= os.O_EXCL
            fd = os.open(self.path, flags, 0o600)
            try:
                data = (json.dumps(body, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
                view = memoryview(data)
                while view:
                    written = os.write(fd, view)
                    if written <= 0:
                        raise EvidenceError("short evidence write")
                    view = view[written:]
                os.fsync(fd)
            finally:
                os.close(fd)
            if created_log:
                _fsync_directory(parent)
            return body

    def verify(self) -> tuple[bool, str | None]:
        if not os.path.exists(self.path):
            # A standalone empty EvidenceLog is the genesis state. The engine
            # separately refuses to operate without its initialized runtime.
            return True, None
        if not os.path.isfile(self.path):
            return False, "evidence log is not a regular file"
        try:
            records = list(self.records())
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
            return False, "evidence log is malformed or unreadable"
        prev = GENESIS_HASH
        required = {"seq", "timestamp", "event_type", "prev_hash", "payload", "record_hash"}
        for line_number, rec in enumerate(records, start=1):
            if not isinstance(rec, dict) or not required.issubset(rec):
                return False, f"invalid evidence record at line {line_number}"
            body = {k: v for k, v in rec.items() if k != "record_hash"}
            if body.get("prev_hash") != prev:
                return False, f"broken chain at seq {rec.get('seq')}: prev_hash mismatch"
            try:
                actual = _record_hash(body)
            except (TypeError, ValueError, OverflowError):
                return False, f"invalid record encoding at line {line_number}"
            if actual != rec["record_hash"]:
                return False, f"tampered record at seq {rec.get('seq')}: hash mismatch"
            if type(rec["seq"]) is not int or rec["seq"] != line_number:
                return False, f"tampered record at seq {rec.get('seq')}: hash mismatch"
            if (not isinstance(rec["event_type"], str) or not isinstance(rec["payload"], dict)
                    or not isinstance(rec["record_hash"], str) or not isinstance(rec["prev_hash"], str)):
                return False, f"invalid record fields at line {line_number}"
            prev = rec["record_hash"]
        return True, None
