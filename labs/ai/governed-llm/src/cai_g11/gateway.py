"""CAI G11 closed-world tools/call emulator and signed authorization gate.

Security boundary is an IN-PROCESS LABORATORY allowlist of immutable tool and
fixture definitions; this module is NOT an OS/container isolation mechanism,
real MCP server, LLM prompt-injection sanitizer, or production identity source.
There are no pluggable functions, network transports, filesystem operations,
or effectful tools here. Approvals are actual G10 ML-DSA-87 signatures over
an operation/resource/session-bound intent, but keys/trust remain lab fixtures.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import threading
from dataclasses import dataclass
from typing import Any, Callable

from cai_g10.pqc import ApprovalVerifier, Denied, Hold, canonical, digest, strict_loads

MAX_WIRE_BYTES = 8192
MAX_RESULT_BYTES = 4096
MCP_METHOD = "tools/call"
MCP_TOOL = "cai.fixture.read"
MCP_VERSION = "2.0"
DOMAIN = "CAI-G11-MCP-TOOL-INTENT/V1"
RES_RE = re.compile(r"^[a-z][a-z0-9_-]{0,31}(?:/[a-z][a-z0-9_-]{0,31}){0,3}$")
TOKEN_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.:/-]{0,100}$")
NONCE_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")
LEVEL = {"PUBLIC": 0, "INTERNAL": 1, "CONFIDENTIAL": 2, "RESTRICTED": 3}
EXPOSE_MAX = "CONFIDENTIAL"  # deliberate deny regardless of holder clearance


@dataclass(frozen=True)
class Session:
    """SERVER-PROVISIONED LAB FIXTURE, not a self-authenticating bearer token."""
    tenant: str
    principal: str
    audience: str
    context_digest: str
    policy_digest: str
    clearance: str
    allowed_tools: frozenset[str]
    active: bool = True

    def __post_init__(self):
        if (not all(type(x) is str and TOKEN_RE.fullmatch(x)
                    for x in (self.tenant, self.principal, self.audience)) or
            self.clearance not in LEVEL or type(self.allowed_tools) is not frozenset or
            not self.allowed_tools or type(self.active) is not bool):
            raise ValueError("INVALID_SERVER_SESSION")
        for ref in (self.context_digest, self.policy_digest):
            if type(ref) is not str or not re.fullmatch(r"sha256:[0-9a-f]{64}", ref):
                raise ValueError("INVALID_SERVER_DIGEST")


@dataclass(frozen=True)
class Tool:
    name: str
    operation: str
    max_classification: str
    enabled: bool = True

    def __post_init__(self):
        if (self.name != MCP_TOOL or self.operation != "READ" or
            self.max_classification not in LEVEL or type(self.enabled) is not bool):
            raise ValueError("NON_ALLOWLISTED_TOOL_DEFINITION")


@dataclass(frozen=True)
class Record:
    tenant: str
    resource: str
    classification: str
    text: str

    def __post_init__(self):
        if (type(self.tenant) is not str or not TOKEN_RE.fullmatch(self.tenant) or
            type(self.resource) is not str or not RES_RE.fullmatch(self.resource) or
            self.classification not in LEVEL or type(self.text) is not str or
            len(self.text.encode("utf-8")) > MAX_RESULT_BYTES):
            raise ValueError("INVALID_LAB_RECORD")
        # Return data verbatim as untrusted data; no data-to-instruction promotion.
        canonical({"text": self.text})


class FixtureAuthority:
    """A mutable test authority. Locking is local; no distributed atomicity."""
    def __init__(self, sessions: tuple[Session, ...], tools: tuple[Tool, ...], records: tuple[Record, ...]):
        self._lock = threading.RLock()
        self._sessions: dict[tuple[str, str], Session] = {}
        self._tools: dict[str, Tool] = {}
        self._records: dict[tuple[str, str], Record] = {}
        for s in sessions:
            key = (s.tenant, s.principal)
            if key in self._sessions:
                raise ValueError("DUPLICATE_SESSION")
            self._sessions[key] = s
        for t in tools:
            if t.name in self._tools:
                raise ValueError("DUPLICATE_TOOL")
            self._tools[t.name] = t
        for r in records:
            key = (r.tenant, r.resource)
            if key in self._records:
                raise ValueError("DUPLICATE_RESOURCE")
            self._records[key] = r
        self._epoch = 0

    def snapshot(self, session: Session, tool_id: str, resource: str) -> tuple[int, Tool, Record]:
        with self._lock:
            authoritative = self._sessions.get((session.tenant, session.principal))
            if authoritative != session or not session.active:
                raise Denied("AUTHORITY_MISSING_OR_REVOKED")
            tool = self._tools.get(tool_id)
            if tool is None or not tool.enabled or tool.name not in session.allowed_tools:
                raise Denied("TOOL_NOT_PERMITTED")
            record = self._records.get((session.tenant, resource))
            if record is None:
                raise Denied("RESOURCE_NOT_PERMITTED")
            if (LEVEL[record.classification] > LEVEL[session.clearance] or
                LEVEL[record.classification] > LEVEL[tool.max_classification] or
                LEVEL[record.classification] > LEVEL[EXPOSE_MAX]):
                raise Denied("DATA_RELEASE_NOT_PERMITTED")
            return self._epoch, tool, record

    def release_if_unchanged(self, session: Session, tool_id: str, resource: str,
                             reference: tuple[int, Tool, Record]) -> Record:
        """Atomic authority recheck plus fixture read at one local linearization point."""
        with self._lock:
            current = self.snapshot(session, tool_id, resource)
            if current != reference:
                raise Denied("PRE_DISPATCH_CONTEXT_CHANGED")
            return current[2]

    def update_session(self, new_session: Session) -> None:
        with self._lock:
            if (new_session.tenant, new_session.principal) not in self._sessions:
                raise KeyError("NO_LAB_SESSION")
            self._sessions[(new_session.tenant, new_session.principal)] = new_session
            self._epoch += 1

    def update_tool(self, new_tool: Tool) -> None:
        with self._lock:
            if new_tool.name not in self._tools:
                raise KeyError("NO_LAB_TOOL")
            self._tools[new_tool.name] = new_tool
            self._epoch += 1

    def update_record(self, new_record: Record) -> None:
        with self._lock:
            if (new_record.tenant, new_record.resource) not in self._records:
                raise KeyError("NO_LAB_RECORD")
            self._records[(new_record.tenant, new_record.resource)] = new_record
            self._epoch += 1


class Gateway:
    """Signed, deny-by-default tools/call facade over a closed fixture store.

    A test-only callback can exercise TOCTOU just before dispatch. The callback
    MUST NOT be offered as a caller-facing or production extension point.
    """
    def __init__(self, authority: FixtureAuthority, verifier: ApprovalVerifier,
                 now: Callable[[], dt.datetime]):
        if not isinstance(authority, FixtureAuthority) or not isinstance(verifier, ApprovalVerifier):
            raise TypeError("TRUSTED_GATEWAY_DEPENDENCIES_REQUIRED")
        self.authority, self.verifier, self.now = authority, verifier, now
        self._audit: list[dict[str, str]] = []
        self._audit_lock = threading.Lock()

    @property
    def audit_snapshot(self) -> tuple[dict[str, str], ...]:
        with self._audit_lock:
            return tuple(dict(item) for item in self._audit)

    def _record(self, code: str, identifier: str | None) -> None:
        # No tool arguments, content, signature or identity details in public logs.
        safe_id = identifier if type(identifier) is str else ""
        event = {"result": "DENIED" if code != "ALLOWED" else "ALLOWED",
                 "code": code,
                 "request_sha256": hashlib.sha256(safe_id.encode("utf-8")).hexdigest()}
        with self._audit_lock:
            self._audit.append(event)  # untrusted in-memory audit, NOT immutable evidence

    @staticmethod
    def _parse(wire: bytes | str) -> tuple[dict[str, Any], str, str, str]:
        if type(wire) not in (bytes, str):
            raise Denied("INVALID_WIRE_TYPE")
        try:
            size = len(wire if type(wire) is bytes else wire.encode("utf-8"))
        except UnicodeEncodeError as exc:
            raise Denied("INVALID_UNICODE") from exc
        if size == 0 or size > MAX_WIRE_BYTES:
            raise Denied("WIRE_LENGTH_INVALID")
        data = strict_loads(wire)
        canonical(data)  # recursive NFC, integer-only and depth checks
        if (type(data) is not dict or frozenset(data) !=
                frozenset({"jsonrpc", "id", "method", "params"}) or
                data["jsonrpc"] != MCP_VERSION or data["method"] != MCP_METHOD):
            raise Denied("MCP_METHOD_OR_ENVELOPE_INVALID")
        ident = data["id"]
        if type(ident) is not str or not TOKEN_RE.fullmatch(ident):
            raise Denied("REQUEST_ID_INVALID")
        params = data["params"]
        if type(params) is not dict or frozenset(params) != frozenset({"name", "arguments", "_meta"}):
            raise Denied("MCP_PARAMS_INVALID")
        if params["name"] != MCP_TOOL:
            raise Denied("TOOL_UNKNOWN_OR_UNAPPROVED")
        args = params["arguments"]
        if type(args) is not dict or frozenset(args) != frozenset({"resource_id"}):
            raise Denied("ARGUMENTS_SCHEMA_INVALID")
        resource = args["resource_id"]
        if type(resource) is not str or not RES_RE.fullmatch(resource):
            raise Denied("RESOURCE_ID_INVALID")
        meta = params["_meta"]
        if type(meta) is not dict or frozenset(meta) != frozenset({"cai_nonce"}):
            raise Denied("MCP_META_INVALID")
        nonce = meta["cai_nonce"]
        if type(nonce) is not str or not NONCE_RE.fullmatch(nonce):
            raise Denied("NONCE_INVALID")
        return data, ident, resource, nonce

    def _prepared(self, wire: bytes | str, session: Session) -> tuple[dict, dict, tuple[int, Tool, Record], str]:
        if type(session) is not Session:
            raise Denied("SERVER_SESSION_REQUIRED")
        data, req_id, resource, nonce = self._parse(wire)
        snap = self.authority.snapshot(session, data["params"]["name"], resource)
        _, tool, record = snap
        intent = {
            "domain": DOMAIN,
            "mcp": data,
            "principal": session.principal,
            "tenant_id": session.tenant,
            "audience": session.audience,
            "context_digest": session.context_digest,
            "policy_digest": session.policy_digest,
            "clearance": session.clearance,
            "tool": {"name": tool.name, "operation": tool.operation,
                     "max_classification": tool.max_classification},
            "resource": {"id": resource, "tenant_id": record.tenant,
                         "classification": record.classification, "digest": digest(record.text)},
        }
        binding = {"tenant_id": session.tenant, "audience": session.audience,
                   "request_id": req_id, "nonce": nonce,
                   "request_digest": digest(intent),
                   "context_digest": session.context_digest,
                   "policy_digest": session.policy_digest}
        return binding, data, snap, resource

    def prepare_lab_binding(self, wire: bytes | str, session: Session) -> dict[str, str]:
        """Test harness signing intent only; does not authorize or dispatch."""
        binding, _, _, _ = self._prepared(wire, session)
        return binding

    def call(self, wire: bytes | str, session: Session, approvals: list[dict],
             *, before_dispatch_lab: Callable[[], None] | None = None) -> dict:
        req_id = None
        try:
            binding, data, snap, resource = self._prepared(wire, session)
            req_id = binding["request_id"]
            if type(approvals) is not list:
                raise Denied("APPROVAL_LIST_REQUIRED")
            current = self.now()
            self.verifier.authorize(approvals, binding=binding,
                                    purposes=frozenset({"MCP_TOOL_CALL"}),
                                    requester_id=session.principal, now=current)
            if before_dispatch_lab is not None:
                before_dispatch_lab()  # only test harness can install callback
            # Recheck after signature verified. Even an unrelated authority
            # revision fails closed rather than accepting a stale observation.
            record = self.authority.release_if_unchanged(session, data["params"]["name"], resource, snap)
            # A successful MCP-looking response is NOT proof of any external work.
            result = {"jsonrpc": MCP_VERSION, "id": req_id,
                      "result": {"content": [{"type": "text", "text": record.text}],
                                 "isError": False,
                                 "_meta": {"cai_data_trust": "UNTRUSTED_FIXTURE_DATA",
                                           "cai_classification": record.classification,
                                           "cai_execution": "IN_MEMORY_FIXTURE_READ_ONLY"}}}
            if len(canonical(result)) > MAX_RESULT_BYTES + 1024:
                raise Denied("RESULT_TOO_LARGE")
            self._record("ALLOWED", req_id)
            return result
        except Exception as exc:
            code = str(exc) if type(exc) in (Denied, Hold) else "INPUT_OR_INTERNAL_FAILURE"
            self._record(code, req_id)
            # Never reflect input, class, tenant, path, nonce or exception text.
            return {"jsonrpc": MCP_VERSION, "id": None,
                    "error": {"code": -32001, "message": "CAI_GATEWAY_DENIED"}}
