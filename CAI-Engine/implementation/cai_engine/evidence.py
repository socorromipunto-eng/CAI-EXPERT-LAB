"""Evidence and audit layer (Architecture.md 4.7, Safety-Gates.md section 8).

The reference runtime appends records to a hash-chained JSON Lines log. Each
record carries the SHA-256 of its predecessor. verify() checks the hashes and
links of records present; it does not establish completeness or authenticity.
Removing a valid suffix, removing the log, or rebuilding a consistent chain
with sufficient write access may pass local verification. Runtime evidence
signing and external anchoring are not implemented. A signed Git commit does
not supply either control for this evidence log. The framework's immutable,
auditable-history requirement therefore remains only partly implemented.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from collections.abc import Iterator

GENESIS_HASH = "0" * 64


def _canonical(obj: dict) -> bytes:
    """Deterministic JSON encoding for hashing (sorted keys, no whitespace)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _record_hash(record_without_hash: dict) -> str:
    return hashlib.sha256(_canonical(record_without_hash)).hexdigest()


class EvidenceLog:
    """Append-only, hash-chained evidence log stored as JSON Lines."""

    def __init__(self, path: str):
        self.path = path

    # -- reading -----------------------------------------------------------
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

    # -- writing -----------------------------------------------------------
    def append(self, event_type: str, payload: dict) -> dict:
        prev_hash = self.last_hash()
        body = {
            "seq": self.count() + 1,
            "timestamp": time.time(),
            "event_type": event_type,
            "prev_hash": prev_hash,
            "payload": payload,
        }
        body["record_hash"] = _record_hash(body)
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(body, ensure_ascii=False) + "\n")
        return body

    # -- integrity ---------------------------------------------------------
    def verify(self) -> tuple[bool, str | None]:
        """Re-walk the chain. Returns (ok, error_message)."""
        prev = GENESIS_HASH
        for rec in self.records():
            stored = rec.get("record_hash")
            body = {k: v for k, v in rec.items() if k != "record_hash"}
            if body.get("prev_hash") != prev:
                return False, f"broken chain at seq {rec.get('seq')}: prev_hash mismatch"
            if _record_hash(body) != stored:
                return False, f"tampered record at seq {rec.get('seq')}: hash mismatch"
            prev = stored
        return True, None
