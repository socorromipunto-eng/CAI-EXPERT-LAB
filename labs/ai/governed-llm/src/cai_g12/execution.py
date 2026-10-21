"""GATE12 test-only local-file effect with independently re-opened observation.

An in-process fixture, NOT OS isolation, distributed exactly-once delivery,
real MCP, authenticated identity, durable production evidence or external action.
No subprocess, shell, network, arbitrary path, plugin or user-selected target.
"""
from __future__ import annotations

import base64
import binascii
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import stat
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable

from cai_g10.pqc import ApprovalVerifier, Denied, Hold, OpenSslMldsa87, canonical, digest

DOMAIN = "CAI-G12-LOCAL-EFFECT/V1"
RECEIPT_DOMAIN = "CAI-G12-EVIDENCE-RECEIPT/V1"
RECEIPT_FIELDS = frozenset({"domain","status","tenant_id","request_id","request_digest","observed_digest","journal_head","verification","receipt_author"})
PURPOSE = "G12_LOCAL_EFFECT"
TOKEN = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")
REQUEST_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
NONCE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")
SHA = re.compile(r"^sha256:[0-9a-f]{64}$")
ALLOWED = frozenset({"domain", "tenant_id", "requester_id", "request_id", "nonce", "audience", "context_digest", "policy_digest", "operation", "key", "value"})
ZERO = "0" * 64
MAX_PAYLOAD = 512


class LabInterruption(Exception):
    """Injected by tests only; outcome of effect is not assumed."""


def _safe_root(root: Path) -> Path:
    if not isinstance(root, Path) or not root.is_dir() or root.is_symlink():
        raise Denied("INVALID_LAB_ROOT")
    return root.resolve(strict=True)


def validate_request(value: Any) -> dict:
    if type(value) is not dict or frozenset(value) != ALLOWED:
        raise Denied("INVALID_REQUEST_SHAPE")
    canonical(value)  # rejects non-NFC, floats, recursion, unknown JSON data
    if value["domain"] != DOMAIN or value["operation"] != "PUT_ONCE":
        raise Denied("NOT_ALLOWLISTED")
    for name in ("tenant_id", "requester_id", "key"):
        if type(value[name]) is not str or not TOKEN.fullmatch(value[name]):
            raise Denied("INVALID_IDENTIFIER")
    if type(value["audience"]) is not str or value["audience"] != "cai.lab.execution":
        raise Denied("WRONG_AUDIENCE")
    if type(value["request_id"]) is not str or not REQUEST_ID.fullmatch(value["request_id"]):
        raise Denied("BAD_REQUEST_ID")
    if type(value["nonce"]) is not str or not NONCE.fullmatch(value["nonce"]):
        raise Denied("BAD_NONCE")
    if any(type(value[n]) is not str or not SHA.fullmatch(value[n]) for n in ("context_digest", "policy_digest")):
        raise Denied("BAD_POLICY_OR_CONTEXT")
    if type(value["value"]) is not str or not (1 <= len(value["value"].encode("utf-8")) <= MAX_PAYLOAD):
        raise Denied("BAD_VALUE_LENGTH")
    return value


def effect_bytes(req: dict) -> bytes:
    return canonical({"domain": DOMAIN, "tenant_id": req["tenant_id"], "key": req["key"],
                      "value": req["value"], "request_digest": digest(req)})


def target_name(req: dict) -> str:
    return hashlib.sha256((req["tenant_id"] + "\0" + req["key"]).encode("utf-8")).hexdigest() + ".effect"


class LabAuthority:
    """Test-provisioned lab authority, never a real IdP or canonical CAI policy."""
    def __init__(self, tenant: str, requester: str, context: str, policy: str):
        self.lock = threading.RLock()
        self.tenant, self.requester, self.context, self.policy = tenant, requester, context, policy
        self.active = True
        self.epoch = 0

    def snapshot(self, req: dict) -> int:
        with self.lock:
            if (not self.active or req["tenant_id"] != self.tenant or
                req["requester_id"] != self.requester or req["context_digest"] != self.context or
                req["policy_digest"] != self.policy):
                raise Denied("AUTHORITY_DENIED")
            return self.epoch

    def require_unchanged(self, req: dict, epoch: int) -> None:
        if self.snapshot(req) != epoch:
            raise Denied("AUTHORITY_CHANGED")

    def change(self, *, context: str | None = None, policy: str | None = None, active: bool | None = None):
        with self.lock:
            if context is not None: self.context = context
            if policy is not None: self.policy = policy
            if active is not None: self.active = active
            self.epoch += 1


class LabJournal:
    """SQLite local durable-ish test journal, NOT distributed or tamper-proof.

    Each transition is hash-chained; SQLite contents remain locally mutable.
    Owner-provided root is restricted to a disposable, isolated test directory.
    """
    def __init__(self, root: Path):
        self.root = _safe_root(root)
        self.db = self.root / "g12-journal.sqlite3"
        self.lock = threading.RLock()
        with self._db() as con:
            con.executescript("""
            CREATE TABLE IF NOT EXISTS operations (
              tenant TEXT NOT NULL, request_id TEXT NOT NULL, effect_key TEXT NOT NULL,
              operation_digest TEXT NOT NULL, status TEXT NOT NULL,
              PRIMARY KEY(tenant,request_id), UNIQUE(tenant,effect_key));
            CREATE TABLE IF NOT EXISTS events (
              seq INTEGER PRIMARY KEY AUTOINCREMENT, tenant TEXT NOT NULL,
              request_id TEXT NOT NULL, status TEXT NOT NULL, observed_digest TEXT,
              previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL);
            """)

    @contextmanager
    def _db(self):
        con = sqlite3.connect(str(self.db), timeout=5, isolation_level=None)
        try:
            con.execute("PRAGMA busy_timeout=5000")
            yield con
        finally:
            con.close()

    @staticmethod
    def _event_hash(seq: int, tenant: str, reqid: str, status: str,
                    observation: str | None, prev: str) -> str:
        return hashlib.sha256(canonical({"seq":seq,"tenant":tenant,"request_id":reqid,
            "status":status,"observation":observation,"previous":prev})).hexdigest()

    def _assert_chain(self, con) -> str:
        prev = ZERO
        rows = con.execute("SELECT seq,tenant,request_id,status,observed_digest,previous_hash,event_hash FROM events ORDER BY seq").fetchall()
        for seq, tenant, reqid, status, obs, previous, recorded in rows:
            if (previous != prev or recorded != self._event_hash(seq, tenant, reqid, status, obs, prev)):
                raise Hold("EVENT_CHAIN_INTEGRITY_FAILURE")
            prev = recorded
        return prev

    def check_chain(self) -> str:
        with self.lock:
            with self._db() as con:
                return self._assert_chain(con)

    def _append(self, con, tenant: str, reqid: str, status: str, observation: str | None):
        prev = self._assert_chain(con)
        cursor = con.execute("INSERT INTO events(tenant,request_id,status,observed_digest,previous_hash,event_hash) VALUES(?,?,?,?,?,?)",
                             (tenant, reqid, status, observation, prev, "PENDING"))
        seq = cursor.lastrowid
        h = self._event_hash(seq, tenant, reqid, status, observation, prev)
        con.execute("UPDATE events SET event_hash=? WHERE seq=?", (h, seq))
        return h

    def reserve(self, req: dict) -> None:
        with self.lock:
            with self._db() as con:
                con.execute("BEGIN IMMEDIATE")
                try:
                    self._assert_chain(con)
                    con.execute("INSERT INTO operations VALUES(?,?,?,?,?)",
                                (req["tenant_id"], req["request_id"], req["key"], digest(req), "PREPARED"))
                    self._append(con, req["tenant_id"], req["request_id"], "PREPARED", None)
                    con.commit()
                except sqlite3.IntegrityError as exc:
                    con.rollback()
                    raise Denied("DUPLICATE_OR_CONFLICTING_OPERATION") from exc
                except Exception:
                    con.rollback()
                    raise

    def transition(self, req: dict, status: str, observation: str | None = None) -> str:
        if status not in {"DISPATCHED", "SUCCEEDED", "FAILED", "INDETERMINATE"}:
            raise Denied("INVALID_STATE")
        with self.lock:
            with self._db() as con:
                con.execute("BEGIN IMMEDIATE")
                try:
                    self._assert_chain(con)
                    row = con.execute("SELECT operation_digest,status FROM operations WHERE tenant=? AND request_id=?",
                                      (req["tenant_id"], req["request_id"])).fetchone()
                    if row is None or row[0] != digest(req): raise Denied("MISSING_OR_CHANGED_OPERATION")
                    previous = row[1]
                    transitions = {"PREPARED":{"DISPATCHED","INDETERMINATE"},
                                   "DISPATCHED":{"SUCCEEDED","FAILED","INDETERMINATE"},
                                   "INDETERMINATE":{"SUCCEEDED","FAILED"},
                                   "FAILED":set(), "SUCCEEDED":set()}
                    if status not in transitions.get(previous, set()):
                        raise Denied("INVALID_TRANSITION")
                    con.execute("UPDATE operations SET status=? WHERE tenant=? AND request_id=?",
                                (status, req["tenant_id"], req["request_id"]))
                    h = self._append(con, req["tenant_id"], req["request_id"], status, observation)
                    con.commit()
                    return h
                except Exception:
                    con.rollback()
                    raise

    def succeed_signed(self, req: dict, observation: str, signer: "LabEvidenceSigner") -> dict:
        """Commit success ONLY if its ML-DSA-87 receipt was signed successfully.

        Hold the local SQLite write transaction while signing the predicted
        next event hash; failures rollback rather than recording false success.
        This is local-only serialization, not real distributed commit/IV&V.
        """
        if type(observation) is not str or not SHA.fullmatch(observation):
            raise Denied("INVALID_OBSERVATION")
        with self.lock:
            with self._db() as con:
                con.execute("BEGIN IMMEDIATE")
                try:
                    prev = self._assert_chain(con)
                    row = con.execute("SELECT operation_digest,status FROM operations WHERE tenant=? AND request_id=?",
                                      (req["tenant_id"], req["request_id"])).fetchone()
                    if row is None or row[0] != digest(req) or row[1] not in {"DISPATCHED","INDETERMINATE"}:
                        raise Denied("UNAUTHORIZED_SUCCESS_TRANSITION")
                    seq = con.execute("SELECT COALESCE(MAX(seq),0)+1 FROM events").fetchone()[0]
                    next_hash = self._event_hash(seq,req["tenant_id"],req["request_id"],
                                                 "SUCCEEDED",observation,prev)
                    payload = {"domain":RECEIPT_DOMAIN,"status":"SUCCEEDED",
                               "tenant_id":req["tenant_id"],"request_id":req["request_id"],
                               "request_digest":digest(req),"observed_digest":observation,
                               "journal_head":next_hash,"verification":"LOCAL_REOPEN_OBSERVER",
                               "receipt_author":"UNTRUSTED_LAB_TEST_KEY"}
                    signed = signer.sign(payload)  # may raise Hold: SQL transaction rolled back
                    con.execute("INSERT INTO events(seq,tenant,request_id,status,observed_digest,previous_hash,event_hash) VALUES(?,?,?,?,?,?,?)",
                                (seq,req["tenant_id"],req["request_id"],"SUCCEEDED",observation,prev,next_hash))
                    con.execute("UPDATE operations SET status='SUCCEEDED' WHERE tenant=? AND request_id=?",
                                (req["tenant_id"],req["request_id"]))
                    con.commit()
                    return signed
                except Exception:
                    con.rollback()
                    raise

    def status(self, tenant: str, request_id: str) -> str | None:
        with self.lock:
            with self._db() as con:
                self._assert_chain(con)
                row = con.execute("SELECT status FROM operations WHERE tenant=? AND request_id=?",
                                  (tenant, request_id)).fetchone()
                return row[0] if row else None


class LocalEffectExecutor:
    """No arbitrary paths: derived names, O_EXCL, scratch-folder only."""
    def __init__(self, root: Path):
        self.root = _safe_root(root)
        self.effects = self.root / "lab-effects"
        self.effects.mkdir(mode=0o700, exist_ok=True)
        if self.effects.is_symlink() or not self.effects.is_dir():
            raise Denied("INVALID_EFFECT_DIRECTORY")

    def apply(self, req: dict, *, fault_lab: str | None = None) -> str:
        if fault_lab == "BEFORE_WRITE": raise LabInterruption("INTERRUPTED_BEFORE_WRITE")
        if self.effects.is_symlink() or self.effects.resolve() != self.root / "lab-effects":
            raise Hold("LAB_FOLDER_BOUNDARY_CHANGED")
        path = self.effects / target_name(req)
        flags = os.O_CREAT | os.O_WRONLY | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(str(path), flags, 0o600)
        try:
            data = effect_bytes(req)
            with os.fdopen(fd, "wb", closefd=True) as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        except Exception:
            raise  # partial effect becomes indeterminate until observed
        if fault_lab == "AFTER_WRITE": raise LabInterruption("INTERRUPTED_AFTER_WRITE")
        return "UNTRUSTED_EXECUTOR_ACK"


class EvidenceObserver:
    """Separate code path re-opens observed bytes; does not trust executor ACK."""
    def __init__(self, executor: LocalEffectExecutor):
        self.effects = executor.effects

    def observe(self, req: dict) -> tuple[str, str | None]:
        path = self.effects / target_name(req)
        if self.effects.is_symlink() or not self.effects.is_dir():
            return "UNKNOWN", None
        try:
            st = path.lstat()
            if not stat.S_ISREG(st.st_mode) or st.st_size > 2048:
                return "MISMATCH", None
            with path.open("rb") as stream:
                raw = stream.read(2049)
        except (FileNotFoundError, OSError):
            return "UNKNOWN", None
        if len(raw) > 2048:
            return "MISMATCH", None
        seen = "sha256:" + hashlib.sha256(raw).hexdigest()
        return ("MATCH" if raw == effect_bytes(req) else "MISMATCH"), seen


class LabEvidenceSigner:
    """Different lab key from human approver; neither is a real IV&V authority."""
    def __init__(self, provider: OpenSslMldsa87, private_key: Path, public_key: bytes):
        self.provider, self.private_key, self.public_key = provider, private_key, public_key
        self.key_id = provider.key_id(public_key)

    def sign(self, payload: dict) -> dict:
        raw = b"CAI-G12-LAB-RECEIPT-V1\x00" + canonical(payload)
        return {"payload": payload, "key_id": self.key_id, "algorithm": "ML-DSA-87",
                "signature_b64": base64.b64encode(self.provider.sign_lab(self.private_key, raw)).decode("ascii")}

    def verify(self, envelope: Any) -> bool:
        if type(envelope) is not dict or frozenset(envelope) != frozenset({"payload", "key_id", "algorithm", "signature_b64"}):
            return False
        try:
            if (envelope["key_id"] != self.key_id or envelope["algorithm"] != "ML-DSA-87" or
                type(envelope["signature_b64"]) is not str):
                return False
            payload = envelope["payload"]
            if (type(payload) is not dict or frozenset(payload) != RECEIPT_FIELDS or
                payload.get("domain") != RECEIPT_DOMAIN or payload.get("status") != "SUCCEEDED" or
                payload.get("verification") != "LOCAL_REOPEN_OBSERVER" or
                payload.get("receipt_author") != "UNTRUSTED_LAB_TEST_KEY" or
                type(payload["journal_head"]) is not str or not re.fullmatch(r"[0-9a-f]{64}",payload["journal_head"]) or
                type(payload["request_digest"]) is not str or not SHA.fullmatch(payload["request_digest"]) or
                type(payload["observed_digest"]) is not str or not SHA.fullmatch(payload["observed_digest"])):
                return False
            sig = base64.b64decode(envelope["signature_b64"], validate=True)
            return self.provider.verify(self.public_key, b"CAI-G12-LAB-RECEIPT-V1\x00" + canonical(payload), sig)
        except (Denied, Hold, ValueError, TypeError, binascii.Error):
            return False


class ControlledBroker:
    def __init__(self, authority: LabAuthority, verifier: ApprovalVerifier,
                 journal: LabJournal, executor: LocalEffectExecutor, observer: EvidenceObserver,
                 evidence_signer: LabEvidenceSigner, now: Callable[[], dt.datetime]):
        self.authority, self.verifier, self.journal = authority, verifier, journal
        self.executor, self.observer, self.evidence_signer, self.now = executor, observer, evidence_signer, now

    def prepare_lab_binding(self, request: Any) -> dict[str, str]:
        req = validate_request(request)
        self.authority.snapshot(req)
        return {"tenant_id":req["tenant_id"], "audience":req["audience"],
                "request_id":req["request_id"], "nonce":req["nonce"],
                "request_digest":digest({"domain":DOMAIN,"operation":req,"effect_digest":"sha256:" + hashlib.sha256(effect_bytes(req)).hexdigest()}),
                "context_digest":req["context_digest"], "policy_digest":req["policy_digest"]}

    def execute(self, request: Any, approvals: Any, *, fault_lab: str | None = None,
                before_dispatch_lab: Callable[[], None] | None = None) -> dict:
        """No actual remote effects. `fault_lab` and callback are test-only injection."""
        reserved = False
        req = None
        try:
            req = validate_request(request)
            if fault_lab not in (None, "BEFORE_WRITE", "AFTER_WRITE"):
                raise Denied("UNKNOWN_LAB_FAULT")
            epoch = self.authority.snapshot(req)
            if type(approvals) is not list:
                raise Denied("APPROVALS_REQUIRED")
            self.verifier.authorize(approvals, binding=self.prepare_lab_binding(req),
                                   purposes=frozenset({PURPOSE}), requester_id=req["requester_id"], now=self.now())
            # Local critical section only; not proof of cross-host TOCTOU fencing.
            with self.authority.lock:
                if before_dispatch_lab is not None: before_dispatch_lab()
                self.authority.require_unchanged(req, epoch)
                self.journal.reserve(req)
                reserved = True
                self.journal.transition(req, "DISPATCHED")
                try:
                    _ack = self.executor.apply(req, fault_lab=fault_lab)
                except (LabInterruption, OSError, Hold):
                    self.journal.transition(req, "INDETERMINATE")
                    return {"status":"INDETERMINATE", "receipt":None}
                # _ack is deliberately ignored. Only observer observation controls success.
                observation, observed_digest = self.observer.observe(req)
                if observation == "MATCH":
                    receipt = self.journal.succeed_signed(req, observed_digest, self.evidence_signer)
                    return {"status":"SUCCEEDED", "receipt":receipt}
                if observation == "MISMATCH":
                    self.journal.transition(req, "FAILED", observed_digest)
                    return {"status":"FAILED", "receipt":None}
                self.journal.transition(req, "INDETERMINATE")
                return {"status":"INDETERMINATE", "receipt":None}
        except (Denied, Hold, sqlite3.DatabaseError, OSError, ValueError, TypeError):
            # Do not treat an attempted effect as DENIED after a journal reservation.
            if reserved and req is not None:
                try:
                    if self.journal.status(req["tenant_id"], req["request_id"]) == "DISPATCHED":
                        self.journal.transition(req, "INDETERMINATE")
                except Exception:
                    pass
                return {"status":"INDETERMINATE", "receipt":None}
            return {"status":"DENIED", "receipt":None}

    def reconcile(self, req: Any) -> dict:
        """Observation only; never re-dispatches an operation or reuses approvals."""
        try:
            req = validate_request(req)
            self.journal.check_chain()
            status = self.journal.status(req["tenant_id"], req["request_id"])
            if status not in {"PREPARED", "DISPATCHED", "INDETERMINATE"}:
                return {"status":"DENIED", "receipt":None}
            # Prepared with no dispatch evidence may NOT be promoted to success,
            # even if a file with matching bytes happens to exist.
            if status == "PREPARED":
                self.journal.transition(req, "INDETERMINATE")
                return {"status":"INDETERMINATE", "receipt":None}
            observation, observed_digest = self.observer.observe(req)
            if observation == "MATCH":
                receipt = self.journal.succeed_signed(req, observed_digest, self.evidence_signer)
                return {"status":"SUCCEEDED", "receipt":receipt}
            if observation == "MISMATCH":
                self.journal.transition(req, "FAILED", observed_digest)
                return {"status":"FAILED", "receipt":None}
            if status == "DISPATCHED":
                self.journal.transition(req, "INDETERMINATE")
            return {"status":"INDETERMINATE", "receipt":None}
        except (Denied, Hold, sqlite3.DatabaseError, OSError, ValueError, TypeError):
            return {"status":"DENIED", "receipt":None}
