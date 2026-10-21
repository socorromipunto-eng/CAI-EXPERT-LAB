"""CAI G10 laboratory ML-DSA-87 signature assurance.

Real OpenSSL 3.5+ ML-DSA signatures, deliberately no fallback. This is an
isolated verifier, not a trusted IdP, HSM/KMS, CAI CORE, or production PDP.
"""
from __future__ import annotations

import base64
import binascii
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
import unicodedata
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

ALGORITHM = "ML-DSA-87"
DOMAIN = "CAI-GOVERNED-LLM/G10/APPROVAL/V1"
VERSION = "g10-lab-v1"
FIELD_NAMES = frozenset({
    "domain", "version", "tenant_id", "audience", "purpose", "request_id", "nonce",
    "request_digest", "context_digest", "policy_digest", "issued_at", "expires_at",
    "approver_id", "decision",
})
ENVELOPE_NAMES = frozenset({"payload", "algorithm", "key_id", "signature_b64"})
SHA_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}$")
NONCE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")
UTC_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
KEY_ID = re.compile(r"^spki-sha256:[0-9a-f]{64}$")


class Hold(RuntimeError):
    """Unavailable actual cryptography or required trust source (not a test pass)."""


class Denied(ValueError):
    """Rejected untrusted input: never authorize on this exception."""


def strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict:
    out = {}
    for key, value in pairs:
        if key in out:
            raise Denied("DUPLICATE_JSON_KEY")
        out[key] = value
    return out


def reject_constant(v: str) -> None:
    raise Denied("NONFINITE_JSON_VALUE")


def strict_loads(blob: str | bytes) -> Any:
    try:
        return json.loads(blob, object_pairs_hook=strict_object_pairs, parse_constant=reject_constant)
    except Denied:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise Denied("INVALID_JSON") from exc


def _validate_json_tree(obj: Any, depth: int = 0) -> None:
    if depth > 12:
        raise Denied("JSON_TOO_DEEP")
    if obj is None or type(obj) in (bool, int):
        return
    if type(obj) is str:
        if unicodedata.normalize("NFC", obj) != obj:
            raise Denied("NONCANONICAL_UNICODE")
        return
    if type(obj) is list:
        for x in obj:
            _validate_json_tree(x, depth + 1)
        return
    if type(obj) is dict:
        if any(type(k) is not str for k in obj):
            raise Denied("INVALID_JSON_KEY")
        for k, v in obj.items():
            _validate_json_tree(k, depth + 1)
            _validate_json_tree(v, depth + 1)
        return
    raise Denied("UNSUPPORTED_JSON_TYPE")  # floats excluded to avoid ambiguity


def canonical(data: Any) -> bytes:
    _validate_json_tree(data)
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(data: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(data)).hexdigest()


def _time(value: str) -> dt.datetime:
    if type(value) is not str or not UTC_TIME.fullmatch(value):
        raise Denied("NONCANONICAL_UTC_TIME")
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError as exc:
        raise Denied("INVALID_UTC_TIME") from exc


def utc(value: dt.datetime) -> str:
    if value.tzinfo is None or value.utcoffset() != dt.timedelta(0):
        raise Denied("NON_UTC_CLOCK")
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_payload(p: Any) -> None:
    if type(p) is not dict or frozenset(p) != FIELD_NAMES:
        raise Denied("PAYLOAD_SCHEMA_MISMATCH")
    if p["domain"] != DOMAIN or p["version"] != VERSION or p["decision"] != "APPROVE":
        raise Denied("PAYLOAD_DOMAIN_VERSION_OR_DECISION")
    for key in ("tenant_id", "audience", "purpose", "request_id", "approver_id"):
        if type(p[key]) is not str or not TOKEN.fullmatch(p[key]):
            raise Denied("INVALID_IDENTITY_OR_PURPOSE")
    if type(p["nonce"]) is not str or not NONCE.fullmatch(p["nonce"]):
        raise Denied("INVALID_NONCE")
    for key in ("request_digest", "context_digest", "policy_digest"):
        if type(p[key]) is not str or not SHA_REF.fullmatch(p[key]):
            raise Denied("INVALID_DIGEST")
    start, end = _time(p["issued_at"]), _time(p["expires_at"])
    if not start < end or (end - start) > dt.timedelta(minutes=5):
        raise Denied("APPROVAL_LIFETIME_INVALID")


def signing_bytes(p: dict) -> bytes:
    validate_payload(p)
    return b"CAI-G10-MLDSA87-V1\x00" + canonical(p)


def _command(args: list[str], *, expect_success: bool = True) -> subprocess.CompletedProcess:
    try:
        r = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Hold("OPENSSL_EXECUTION_UNAVAILABLE") from exc
    if expect_success and r.returncode != 0:
        raise Hold("OPENSSL_CRYPTO_OPERATION_FAILED")
    return r


class OpenSslMldsa87:
    def __init__(self, binary: str | None = None):
        self.binary = binary or shutil.which("openssl")
        if not self.binary:
            raise Hold("OPENSSL_3_5_NOT_INSTALLED")
        version = _command([self.binary, "version"]).stdout.decode("utf-8", errors="replace")
        found = re.search(r"OpenSSL\s+(\d+)\.(\d+)\.(\d+)", version)
        if not found or tuple(map(int, found.groups())) < (3, 5, 0):
            raise Hold("OPENSSL_3_5_REQUIRED")
        self.version = version.strip()
        algs = _command([self.binary, "list", "-signature-algorithms"]).stdout.decode("utf-8", errors="replace")
        if "ML-DSA-87" not in algs:
            raise Hold("ML_DSA_87_PROVIDER_NOT_AVAILABLE")

    def generate_lab_keypair(self, folder: Path) -> tuple[Path, bytes]:
        """Test-only key generation; private key stays in temporary workspace."""
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        secret = folder / "ephemeral-ml-dsa-87-private.pem"
        public = folder / "ephemeral-ml-dsa-87-public.pem"
        _command([self.binary, "genpkey", "-algorithm", ALGORITHM, "-out", str(secret)])
        if os.name != "nt":
            secret.chmod(0o600)
        _command([self.binary, "pkey", "-in", str(secret), "-pubout", "-out", str(public)])
        return secret, public.read_bytes()

    def _pub_file(self, public_pem: bytes, folder: Path) -> Path:
        if not isinstance(public_pem, bytes) or len(public_pem) > 20000 or b"BEGIN PUBLIC KEY" not in public_pem:
            raise Denied("INVALID_PUBLIC_KEY_ENCODING")
        path = folder / "pub.pem"
        path.write_bytes(public_pem)
        description = _command([self.binary, "pkey", "-pubin", "-in", str(path), "-text_pub", "-noout"],
                               expect_success=False)
        if description.returncode != 0 or not description.stdout.startswith(b"ML-DSA-87 Public-Key:"):
            raise Denied("PUBLIC_KEY_ALGORITHM_MISMATCH")
        return path

    def key_id(self, public_pem: bytes) -> str:
        with tempfile.TemporaryDirectory(prefix="cai-g10-pub-") as temp:
            pub = self._pub_file(public_pem, Path(temp))
            r = _command([self.binary, "pkey", "-pubin", "-in", str(pub), "-pubout", "-outform", "DER"],
                         expect_success=False)
            if r.returncode != 0:
                raise Denied("INVALID_PUBLIC_KEY")
            return "spki-sha256:" + hashlib.sha256(r.stdout).hexdigest()

    def sign_lab(self, private_file: Path, message: bytes) -> bytes:
        if len(message) > 1024 * 1024:
            raise Denied("MESSAGE_TOO_LARGE")
        with tempfile.TemporaryDirectory(prefix="cai-g10-sign-") as temp:
            inp, sig = Path(temp) / "message.bin", Path(temp) / "sig.bin"
            inp.write_bytes(message)
            _command([self.binary, "pkeyutl", "-sign", "-inkey", str(private_file),
                      "-in", str(inp), "-out", str(sig), "-pkeyopt", "context-string:CAI-G10-v1"])
            return sig.read_bytes()

    def verify(self, public_pem: bytes, message: bytes, signature: bytes) -> bool:
        if type(signature) is not bytes or len(signature) != 4627 or len(message) > 1024 * 1024:
            return False
        with tempfile.TemporaryDirectory(prefix="cai-g10-verify-") as temp:
            path = Path(temp)
            pub = self._pub_file(public_pem, path)
            inp, sig = path / "message.bin", path / "sig.bin"
            inp.write_bytes(message)
            sig.write_bytes(signature)
            result = _command([self.binary, "pkeyutl", "-verify", "-pubin", "-inkey", str(pub),
                               "-in", str(inp), "-sigfile", str(sig),
                               "-pkeyopt", "context-string:CAI-G10-v1"], expect_success=False)
            return result.returncode == 0


@dataclass(frozen=True)
class TrustedSigner:
    public_pem: bytes
    key_id: str
    approver_id: str
    tenant_id: str
    allowed_purposes: frozenset[str]
    active: bool = True


class TrustRegistry:
    """Explicit lab trust anchor. No trust from self-supplied envelope metadata."""
    def __init__(self, provider: OpenSslMldsa87, signers: Iterable[TrustedSigner]):
        self._signers = {}
        for signer in signers:
            if signer.key_id in self._signers:
                raise Denied("DUPLICATE_TRUST_KEY")
            if provider.key_id(signer.public_pem) != signer.key_id:
                raise Denied("TRUST_ANCHOR_KEY_MISMATCH")
            if not signer.approver_id or not signer.tenant_id or not signer.allowed_purposes:
                raise Denied("INVALID_TRUST_SIGNER")
            self._signers[signer.key_id] = signer
        self._revoked = set()
        self._lock = threading.RLock()

    def lookup(self, key_id: str) -> TrustedSigner | None:
        with self._lock:
            signer = self._signers.get(key_id)
            return signer if signer and signer.active and key_id not in self._revoked else None

    def revoke(self, key_id: str) -> None:
        with self._lock:
            self._revoked.add(key_id)


class ReplayLedger:
    """Thread-safe memory-only lab anti-replay; not durable/distributed."""
    def __init__(self):
        self._seen: set[tuple[str, str, str]] = set()
        self._lock = threading.Lock()

    def reserve_group(self, identifiers: list[tuple[str, str, str]]) -> bool:
        with self._lock:
            if len(set(identifiers)) != len(identifiers) or any(i in self._seen for i in identifiers):
                return False
            self._seen.update(identifiers)
            return True


def envelope_lab(provider: OpenSslMldsa87, private_file: Path, public_pem: bytes, payload: dict) -> dict:
    # Lab-only signing of an already validated structured payload.
    sig = provider.sign_lab(private_file, signing_bytes(payload))
    return {"payload": payload, "algorithm": ALGORITHM,
            "key_id": provider.key_id(public_pem),
            "signature_b64": base64.b64encode(sig).decode("ascii")}


class ApprovalVerifier:
    def __init__(self, provider: OpenSslMldsa87, anchors: TrustRegistry, ledger: ReplayLedger):
        self.provider, self.anchors, self.ledger = provider, anchors, ledger

    def _verify_one(self, env: Any, binding: Mapping[str, str], now: dt.datetime) -> tuple[str, str, str]:
        if type(env) is not dict or frozenset(env) != ENVELOPE_NAMES:
            raise Denied("ENVELOPE_SCHEMA_MISMATCH")
        if env["algorithm"] != ALGORITHM or type(env["key_id"]) is not str or not KEY_ID.fullmatch(env["key_id"]):
            raise Denied("ALGORITHM_OR_KEY_ID_INVALID")
        p = env["payload"]
        message = signing_bytes(p)
        if len(message) > 1_000_000:
            raise Denied("SIGNING_PAYLOAD_TOO_LARGE")
        if now.tzinfo is None or now.utcoffset() != dt.timedelta(0):
            raise Denied("UNTRUSTED_CLOCK")
        if _time(p["issued_at"]) > now + dt.timedelta(seconds=15):
            raise Denied("APPROVAL_FROM_FUTURE")
        if _time(p["expires_at"]) <= now:
            raise Denied("APPROVAL_EXPIRED")
        for key in ("tenant_id", "audience", "request_id", "nonce", "request_digest", "context_digest", "policy_digest"):
            if p[key] != binding.get(key):
                raise Denied("APPROVAL_BINDING_MISMATCH")
        signer = self.anchors.lookup(env["key_id"])
        if signer is None:
            raise Denied("KEY_NOT_TRUSTED_OR_REVOKED")
        if p["approver_id"] != signer.approver_id or p["tenant_id"] != signer.tenant_id:
            raise Denied("SIGNER_IDENTITY_MISMATCH")
        if p["purpose"] not in signer.allowed_purposes:
            raise Denied("SIGNER_PURPOSE_NOT_ALLOWED")
        s = env["signature_b64"]
        if type(s) is not str or len(s) > 10000:
            raise Denied("INVALID_SIGNATURE_BASE64")
        try:
            signature = base64.b64decode(s, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise Denied("INVALID_SIGNATURE_BASE64") from exc
        if not self.provider.verify(signer.public_pem, message, signature):
            raise Denied("SIGNATURE_VERIFICATION_FAILED")
        return p["tenant_id"], p["approver_id"], p["nonce"]

    def authorize(self, approvals: Iterable[dict], *, binding: Mapping[str, str],
                  purposes: frozenset[str], requester_id: str, now: dt.datetime) -> None:
        if type(requester_id) is not str or not requester_id or not purposes:
            raise Denied("INVALID_APPROVAL_POLICY")
        rows = list(approvals)
        if len(rows) != len(purposes) or len(rows) > 4:
            raise Denied("QUORUM_MISMATCH")
        names = []
        seen_actors = set()
        reservation_keys = []
        for env in rows:
            tenant, actor, nonce = self._verify_one(env, binding, now)
            purpose = env["payload"]["purpose"]
            if actor == requester_id or actor in seen_actors:
                raise Denied("SEPARATION_OF_DUTIES")
            seen_actors.add(actor)
            names.append(purpose)
            reservation_keys.append((tenant, actor, nonce))
        if frozenset(names) != purposes or len(names) != len(set(names)):
            raise Denied("PURPOSE_QUORUM_INVALID")
        if not self.ledger.reserve_group(reservation_keys):
            raise Denied("REPLAY_DETECTED")


class Gate09CryptoGuard:
    """Enforces cryptographic quorum before G09 mock executor. NOT external dispatch fencing."""
    def __init__(self, verifier: ApprovalVerifier, engine: Any):
        self.verifier = verifier
        self.engine = engine

    def run(self, request: dict, approvals: Iterable[dict], *, purposes: frozenset[str],
            now: dt.datetime):
        if type(request) is not dict:
            raise Denied("REQUEST_TYPE_INVALID")
        # Required purposes are derived from the request, never caller-controlled.
        try:
            risk = request["risk"]
            effect = request["action"]["effect_type"]
            if effect != "EFFECTFUL":
                raise Denied("SIGNED_EFFECTFUL_BOUNDARY_ONLY")
            safety = risk["ot_safety_class"]
            impact = risk["impact"]
        except (KeyError, TypeError) as exc:
            raise Denied("RISK_POLICY_UNAVAILABLE") from exc
        if safety not in {"NONE", "OT_REVIEW_REQUIRED", "OT_SAFETY_CRITICAL"} or impact not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            raise Denied("UNKNOWN_RISK_POLICY")
        required = {"EXECUTE_ACTION"}
        if safety != "NONE":
            required.add("OT_SAFETY_AUTHORIZATION")
        elif impact in {"HIGH", "CRITICAL"}:
            required.add("SECOND_PERSON_REVIEW")
        if purposes != frozenset(required):
            raise Denied("QUORUM_POLICY_DOWNGRADE")
        binding = {
            "tenant_id": request["tenant_id"], "audience": self.engine.deps.policy.audience,
            "request_id": request["request_id"], "nonce": request["nonce"],
            "request_digest": digest(request),
            "context_digest": request["context"]["snapshot_digest"],
            "policy_digest": request["policy_ref"]["policy_digest"],
        }
        self.verifier.authorize(approvals, binding=binding, purposes=purposes,
                                requester_id=self.engine.deps.identity.subject, now=now)
        # Lab G09 still holds fixture-only identity; this does not turn it into trusted IdP.
        return self.engine.run(canonical(request))
