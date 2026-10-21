"""G08 reference subset of G06 DecisionRequest semantics; NOT full JSON Schema 2020-12."""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import uuid
import unicodedata
from typing import Any

MAX_BYTES = 16384
MAX_DEPTH = 12
SCHEMA = "0.2.1-draft"
ID_RE = re.compile(r"^[A-Za-z0-9._:/@-]{1,128}$", re.ASCII)
DIGEST_RE = re.compile(r"^sha256:[a-f0-9]{64}$", re.ASCII)
NONCE_RE = re.compile(r"^[A-Za-z0-9_-]{22,128}$", re.ASCII)


class ContractError(ValueError):
    pass


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        if key in out:
            raise ContractError("DUPLICATE_JSON_KEY")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise ContractError("NON_FINITE_JSON_NUMBER")


def _depth(value: Any, remaining: int = MAX_DEPTH) -> None:
    if remaining < 0:
        raise ContractError("EXCESSIVE_JSON_DEPTH")
    if isinstance(value, dict):
        for key, entry in value.items():
            if unicodedata.normalize("NFC", key) != key:
                raise ContractError("NON_CANONICAL_UNICODE_KEY")
            _depth(entry, remaining - 1)
    elif isinstance(value, list):
        for item in value:
            _depth(item, remaining - 1)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ContractError("NON_FINITE_JSON_NUMBER")


def decode_json(raw: bytes) -> dict[str, Any]:
    if not isinstance(raw, bytes) or not 0 < len(raw) <= MAX_BYTES:
        raise ContractError("INVALID_JSON_BYTE_LENGTH")
    try:
        decoded = raw.decode("utf-8", errors="strict")
        value = json.loads(decoded, object_pairs_hook=_pairs, parse_constant=_reject_constant)
    except ContractError:
        raise
    except (UnicodeError, ValueError, TypeError, RecursionError) as exc:
        raise ContractError("INVALID_OR_AMBIGUOUS_JSON") from exc
    if type(value) is not dict:
        raise ContractError("ROOT_OBJECT_REQUIRED")
    _depth(value)
    return value


def expect_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != keys:
        raise ContractError("INVALID_FIELDS_" + label)
    return value


def ident(value: Any, label: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise ContractError("INVALID_ID_" + label)
    return value


def digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or not DIGEST_RE.fullmatch(value):
        raise ContractError("INVALID_DIGEST_" + label)
    return value


def uid(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ContractError("INVALID_UUID_" + label)
    try:
        parsed = uuid.UUID(value)
    except ValueError as exc:
        raise ContractError("INVALID_UUID_" + label) from exc
    if str(parsed) != value:
        raise ContractError("NON_CANONICAL_UUID_" + label)
    return value


def instant(value: Any, label: str) -> dt.datetime:
    if not isinstance(value, str) or len(value) > 40:
        raise ContractError("INVALID_DATETIME_" + label)
    try:
        point = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("INVALID_DATETIME_" + label) from exc
    if point.tzinfo is None or point.utcoffset() is None:
        raise ContractError("TIMEZONE_REQUIRED_" + label)
    return point.astimezone(dt.timezone.utc)


def canonical_local_bytes(value: Any) -> bytes:
    """Deterministic *local test* representation, NOT RFC 8785 / JCS signature profile."""
    if isinstance(value, float):
        raise ContractError("FLOAT_CANONICALIZATION_UNSUPPORTED")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def validate_request(value: dict[str, Any]) -> dict[str, Any]:
    expect_object(value, {"schema_version", "request_id", "correlation_id", "principal_ref", "agent_ref", "delegation_ref", "tenant_id", "jurisdiction", "sector_id", "data_classification", "action", "risk", "context", "policy_ref", "evidence_refs", "nonce", "expires_at"}, "REQUEST")
    if value["schema_version"] != SCHEMA:
        raise ContractError("SCHEMA_VERSION_MISMATCH")
    for field in ("request_id", "correlation_id"):
        uid(value[field], field)
    for field in ("principal_ref", "agent_ref", "delegation_ref", "tenant_id", "sector_id"):
        ident(value[field], field)
    if not isinstance(value["jurisdiction"], str) or not re.fullmatch(r"[A-Z]{2,3}", value["jurisdiction"]):
        raise ContractError("INVALID_JURISDICTION_FORMAT")
    if value["data_classification"] not in ("PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"):
        raise ContractError("INVALID_DATA_CLASSIFICATION")
    action = expect_object(value["action"], {"tool_id", "operation", "target_ref", "arguments_digest", "manifest_digest", "effect_type"}, "ACTION")
    for key in ("tool_id", "operation", "target_ref"):
        ident(action[key], "ACTION_" + key)
    for key in ("arguments_digest", "manifest_digest"):
        digest(action[key], "ACTION_" + key)
    if action["effect_type"] not in ("READ_ONLY", "EFFECTFUL"):
        raise ContractError("INVALID_EFFECT_TYPE")
    risk = expect_object(value["risk"], {"impact", "ot_safety_class", "blast_radius", "reversible"}, "RISK")
    if risk["impact"] not in ("LOW", "MEDIUM", "HIGH", "CRITICAL") or risk["ot_safety_class"] not in ("NONE", "OT_REVIEW_REQUIRED", "OT_SAFETY_CRITICAL"):
        raise ContractError("INVALID_RISK_CLASS")
    if type(risk["blast_radius"]) is not int or not 0 <= risk["blast_radius"] <= 1000000 or type(risk["reversible"]) is not bool:
        raise ContractError("INVALID_RISK_VALUES")
    context = expect_object(value["context"], {"dsa_ref", "esa_ref", "snapshot_digest", "observed_at"}, "CONTEXT")
    ident(context["dsa_ref"], "DSA_REF")
    ident(context["esa_ref"], "ESA_REF")
    digest(context["snapshot_digest"], "CONTEXT_DIGEST")
    instant(context["observed_at"], "OBSERVED_AT")
    policy = expect_object(value["policy_ref"], {"policy_id", "policy_version", "policy_digest"}, "POLICY")
    ident(policy["policy_id"], "POLICY_ID")
    ident(policy["policy_version"], "POLICY_VERSION")
    digest(policy["policy_digest"], "POLICY_DIGEST")
    refs = value["evidence_refs"]
    if type(refs) is not list or len(refs) > 32 or len(set(map(str, refs))) != len(refs):
        raise ContractError("INVALID_EVIDENCE_REFS")
    for ref in refs:
        ident(ref, "EVIDENCE_REF")
    if not isinstance(value["nonce"], str) or not NONCE_RE.fullmatch(value["nonce"]):
        raise ContractError("INVALID_NONCE")
    instant(value["expires_at"], "EXPIRES_AT")
    return value
