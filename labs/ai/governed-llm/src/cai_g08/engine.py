"""G08 sandbox-only reference kernel. This is NOT CAI CORE, cryptography or production authorization."""
from __future__ import annotations

import datetime as dt
import hashlib
import threading
from dataclasses import dataclass, field
from typing import Callable

from .contracts import ContractError, canonical_local_bytes, decode_json, instant, validate_request
from .evidence import EvidenceLog


def sha_ref(obj: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_local_bytes(obj)).hexdigest()


@dataclass(frozen=True)
class TrustedIdentity:
    subject: str
    agent: str
    delegation: str
    tenant: str
    roles: frozenset[str]
    assurance: str = "G08_TEST_IDENTITY_ONLY"


@dataclass(frozen=True)
class TrustedContext:
    dsa_ref: str
    esa_ref: str
    snapshot_digest: str
    observed_at: str


@dataclass(frozen=True)
class TrustedTool:
    tool_id: str
    operation: str
    target_ref: str
    manifest_digest: str
    arguments_digest: str
    effect_type: str


@dataclass(frozen=True)
class TrustedPolicy:
    policy_id: str
    policy_version: str
    policy_digest: str
    tenant: str
    audience: str
    jurisdictions: frozenset[str]
    sectors: frozenset[str]
    allowed_roles: frozenset[str]
    allowed_data_classes: frozenset[str]
    enabled: bool = True


@dataclass(frozen=True)
class SandboxApproval:
    """Controlled fixture statement ONLY. No cryptographic signature or MFA claim."""
    subject: str
    tenant: str
    audience: str
    decision_action_digest: str
    context_digest: str
    policy_digest: str
    purpose: str
    expires_at: str
    provenance: str = "G08_TEST_FIXTURE_NON_CRYPTOGRAPHIC"


@dataclass(frozen=True)
class Result:
    decision: str
    execution: str
    reason: str
    action_digest: str = ""
    evidence_head: str = ""
    stages: tuple[str, ...] = ()
    simulation: bool = True


class LeaseStore:
    """Atomic in-process single-use leases; NOT distributed durable fencing."""
    def __init__(self):
        self._lock = threading.Lock()
        self._used: set[tuple[str, str, str]] = set()
        self._epoch = 0

    def consume(self, tenant: str, nonce: str, purpose: str) -> int | None:
        key = (tenant, nonce, purpose)
        with self._lock:
            if key in self._used:
                return None
            self._used.add(key)
            self._epoch += 1
            return self._epoch

    @property
    def consumed_count(self) -> int:
        with self._lock:
            return len(self._used)


class SimulatedWorld:
    """In-memory side effects, NEVER external systems."""
    def __init__(self):
        self._lock = threading.Lock()
        self.effects: dict[str, str] = {}
        self.dispatches = 0

    def effect(self, action_digest: str, value: str) -> None:
        with self._lock:
            self.dispatches += 1
            self.effects[action_digest] = value

    def read_effect(self, action_digest: str) -> str | None:
        with self._lock:
            return self.effects.get(action_digest)


class UncertainDispatch(RuntimeError):
    pass


class SimulatedExecutor:
    def __init__(self, world: SimulatedWorld):
        if type(world) is not SimulatedWorld:
            raise TypeError("G08_REQUIRES_IN_MEMORY_WORLD")
        self.world = world
        self.mode = "ACK"  # ACK | LOST_ACK_AFTER_EFFECT | REJECT_BEFORE_EFFECT

    def dispatch(self, action_digest: str) -> str:
        if self.mode == "REJECT_BEFORE_EFFECT":
            return "PROVEN_NO_EFFECT"
        self.world.effect(action_digest, "fixture-effect-applied")
        if self.mode == "LOST_ACK_AFTER_EFFECT":
            raise UncertainDispatch("ACK_LOST_AFTER_POSSIBLE_EFFECT")
        return "ACK_ONLY"


class SimulatedObserver:
    """Distinct read of fixture state; NOT independent external verifier or IV&V."""
    def __init__(self, world: SimulatedWorld):
        if type(world) is not SimulatedWorld:
            raise TypeError("G08_REQUIRES_IN_MEMORY_WORLD")
        self.world = world
        self.available = True
        self.force_negative = False

    def inspect(self, action_digest: str) -> str:
        if not self.available:
            return "UNKNOWN"
        if self.force_negative:
            return "NO_EFFECT"
        return "EFFECT_PRESENT" if self.world.read_effect(action_digest) == "fixture-effect-applied" else "NO_EFFECT"


@dataclass
class SandboxDependencies:
    # All authority sources are injected by an explicitly labelled sandbox test harness.
    identity: TrustedIdentity | None
    context: TrustedContext | None
    policy: TrustedPolicy | None
    tool: TrustedTool | None
    core_verdict: str = "HOLD"  # Fixture-only adapter result: DENY | HOLD | ALLOW
    approvals: tuple[SandboxApproval, ...] = ()
    clock: Callable[[], dt.datetime] = field(default=lambda: dt.datetime.now(dt.timezone.utc))
    availability: bool = True
    core_available: bool = True
    evidence_available: bool = True
    signer_available: bool = False  # Not implemented. Fixture approvals allowed only in simulation.
    simulation_approval_enabled: bool = False


class Gate08Sandbox:
    """One-request evidence-oriented G08 simulator; production connectors intentionally forbidden."""
    def __init__(self, deps: SandboxDependencies, lease: LeaseStore, executor: SimulatedExecutor, observer: SimulatedObserver):
        if type(executor) is not SimulatedExecutor or type(observer) is not SimulatedObserver:
            raise TypeError("EXTERNAL_EXECUTION_FORBIDDEN")
        if executor.world is not observer.world:
            raise TypeError("FIXTURE_WORLD_MISMATCH")
        self.deps = deps
        self.lease = lease
        self.executor = executor
        self.observer = observer
        self.evidence = EvidenceLog()

    def _reply(self, decision: str, execution: str, reason: str, action_digest: str = "", stages: tuple[str, ...] = ()) -> Result:
        self.evidence.append("SIMULATED_DECISION", {"decision": decision, "execution": execution, "reason": reason, "action_digest": action_digest})
        return Result(decision, execution, reason, action_digest, self.evidence.head, stages)

    def _fresh(self, request: dict, now: dt.datetime) -> bool:
        snap = self.deps.context
        if snap is None:
            return False
        requested = request["context"]
        if (requested["dsa_ref"], requested["esa_ref"], requested["snapshot_digest"]) != (snap.dsa_ref, snap.esa_ref, snap.snapshot_digest):
            return False
        observed = instant(snap.observed_at, "TRUSTED_OBSERVED")
        if observed != instant(requested["observed_at"], "REQUEST_OBSERVED"):
            return False
        # Fixture policy: reject snapshots in future or older than two minutes.
        return dt.timedelta(0) <= now - observed <= dt.timedelta(seconds=120)

    def _policy_and_tool(self, req: dict) -> str | None:
        dep = self.deps
        identity, policy, tool = dep.identity, dep.policy, dep.tool
        if not dep.availability or not dep.core_available or not dep.evidence_available:
            return "CONTROL_PLANE_UNAVAILABLE"
        if identity is None:
            return "MISSING_TRUSTED_IDENTITY"
        if not all((req["principal_ref"] == identity.subject, req["agent_ref"] == identity.agent, req["delegation_ref"] == identity.delegation, req["tenant_id"] == identity.tenant)):
            return "UNTRUSTED_PRINCIPAL_OR_TENANT"
        if policy is None or not policy.enabled:
            return "TRUSTED_POLICY_UNAVAILABLE"
        if not (policy.tenant == identity.tenant == req["tenant_id"]):
            return "TENANT_MISMATCH"
        if req["jurisdiction"] not in policy.jurisdictions or req["sector_id"] not in policy.sectors:
            return "UNKNOWN_JURISDICTION_OR_SECTOR"
        if req["data_classification"] not in policy.allowed_data_classes:
            return "CLASSIFICATION_NOT_AUTHORIZED"
        p = req["policy_ref"]
        if (p["policy_id"], p["policy_version"], p["policy_digest"]) != (policy.policy_id, policy.policy_version, policy.policy_digest):
            return "POLICY_CHANGED_OR_UNTRUSTED"
        if not identity.roles.intersection(policy.allowed_roles):
            return "INSUFFICIENT_PRIVILEGE"
        if tool is None:
            return "UNREGISTERED_TOOL"
        a = req["action"]
        if (a["tool_id"], a["operation"], a["target_ref"], a["manifest_digest"], a["arguments_digest"], a["effect_type"]) != (tool.tool_id, tool.operation, tool.target_ref, tool.manifest_digest, tool.arguments_digest, tool.effect_type):
            return "UNTRUSTED_TOOL_OR_ARGUMENTS"
        return None

    def _approve_fixture(self, req: dict, action_digest: str, now: dt.datetime) -> str | None:
        if req["action"]["effect_type"] != "EFFECTFUL":
            return None
        if not self.deps.simulation_approval_enabled:
            return "PQC_SIGNATURE_AND_REAL_APPROVAL_NOT_CONFIGURED"
        policy = self.deps.policy
        identity = self.deps.identity
        if policy is None or identity is None:
            return "TRUSTED_POLICY_UNAVAILABLE"
        required = 2 if req["risk"]["ot_safety_class"] != "NONE" else 1
        if len(self.deps.approvals) < required:
            return "APPROVALS_MISSING"
        seen: set[str] = set()
        safety_found = False
        for item in self.deps.approvals:
            if item.provenance != "G08_TEST_FIXTURE_NON_CRYPTOGRAPHIC":
                return "UNTRUSTED_APPROVAL_SOURCE"
            if item.subject == identity.subject or item.subject in seen:
                return "SEPARATION_OF_DUTIES_VIOLATION"
            seen.add(item.subject)
            if (item.tenant, item.audience, item.decision_action_digest, item.context_digest, item.policy_digest) != (identity.tenant, policy.audience, action_digest, req["context"]["snapshot_digest"], policy.policy_digest):
                return "APPROVAL_BINDING_MISMATCH"
            if instant(item.expires_at, "APPROVAL_EXPIRY") <= now:
                return "APPROVAL_EXPIRED"
            if item.purpose == "OT_SAFETY_AUTHORIZATION":
                safety_found = True
            if item.purpose not in ("EXECUTE_ACTION", "OT_SAFETY_AUTHORIZATION"):
                return "APPROVAL_PURPOSE_REJECTED"
        if required == 2 and not safety_found:
            return "SAFETY_APPROVER_MISSING"
        return None

    def run(self, raw: bytes, before_dispatch: Callable[[], None] | None = None) -> Result:
        try:
            req = validate_request(decode_json(raw))
        except ContractError as exc:
            return self._reply("DENY", "BLOCKED", str(exc))
        now = self.deps.clock()
        if instant(req["expires_at"], "EXPIRES_AT") <= now:
            return self._reply("DENY", "BLOCKED", "REQUEST_EXPIRED")
        validation = self._policy_and_tool(req)
        if validation:
            decision = "HOLD" if validation in {"CONTROL_PLANE_UNAVAILABLE", "TRUSTED_POLICY_UNAVAILABLE", "UNKNOWN_JURISDICTION_OR_SECTOR", "POLICY_CHANGED_OR_UNTRUSTED"} else "DENY"
            return self._reply(decision, "BLOCKED", validation)
        if not self._fresh(req, now):
            return self._reply("HOLD", "BLOCKED", "CONTEXT_STALE_OR_DRIFTED")
        if self.deps.core_verdict not in ("ALLOW", "DENY", "HOLD"):
            return self._reply("HOLD", "BLOCKED", "CANONICAL_CORE_ADAPTER_INVALID")
        if self.deps.core_verdict != "ALLOW":
            return self._reply(self.deps.core_verdict, "BLOCKED", "CANONICAL_CORE_ADAPTER_NOT_ALLOW")
        binding = {
            "tenant": req["tenant_id"], "audience": self.deps.policy.audience,
            "action": req["action"], "policy_digest": req["policy_ref"]["policy_digest"],
            "context_digest": req["context"]["snapshot_digest"],
        }
        action_digest = sha_ref(binding)
        approval_error = self._approve_fixture(req, action_digest, now)
        if approval_error:
            return self._reply("HOLD", "BLOCKED", approval_error, action_digest)
        if before_dispatch is not None:
            before_dispatch()  # test-injection hook; not present in production
        now = self.deps.clock()
        if instant(req["expires_at"], "EXPIRES_AT") <= now:
            return self._reply("HOLD", "BLOCKED", "EXPIRED_BEFORE_DISPATCH", action_digest)
        if self._policy_and_tool(req) or self.deps.core_verdict != "ALLOW":
            return self._reply("HOLD", "BLOCKED", "PRE_DISPATCH_POLICY_OR_CORE_CHANGED", action_digest)
        if not self._fresh(req, now):
            return self._reply("HOLD", "BLOCKED", "PRE_DISPATCH_CONTEXT_DRIFT", action_digest)
        if self._approve_fixture(req, action_digest, now):
            return self._reply("HOLD", "BLOCKED", "PRE_DISPATCH_APPROVAL_INVALID", action_digest)
        epoch = self.lease.consume(req["tenant_id"], req["nonce"], "ACTION")
        if epoch is None:
            return self._reply("DENY", "BLOCKED", "NONCE_REPLAY", action_digest)
        self.evidence.append("SIMULATED_LEASE_CONSUMED", {"epoch": epoch, "action_digest": action_digest})
        try:
            result = self.executor.dispatch(action_digest)
        except UncertainDispatch:
            return self._reply("ALLOW", "INDETERMINATE", "ACK_LOST_NO_BLIND_RETRY", action_digest, ("AUTHORIZED", "DISPATCHED", "INDETERMINATE"))
        except Exception:
            return self._reply("ALLOW", "INDETERMINATE", "EXECUTOR_UNEXPECTED_EXCEPTION", action_digest, ("AUTHORIZED", "DISPATCHED", "INDETERMINATE"))
        if result == "PROVEN_NO_EFFECT":
            return self._reply("ALLOW", "VERIFIED_FAILURE", "SIMULATED_EXECUTOR_PROVEN_NO_EFFECT", action_digest, ("AUTHORIZED", "DISPATCHED", "VERIFIED_FAILURE"))
        if result != "ACK_ONLY":
            return self._reply("ALLOW", "INDETERMINATE", "UNRECOGNIZED_EXECUTOR_RESPONSE", action_digest)
        # ACK alone never means successful execution.
        if self.observer.available:
            observation = self.observer.inspect(action_digest)
            if observation == "EFFECT_PRESENT":
                return self._reply("ALLOW", "VERIFIED_SUCCESS", "SIMULATED_POSTCONDITION_OBSERVED", action_digest, ("AUTHORIZED", "DISPATCHED", "EXECUTED_UNVERIFIED", "VERIFIED_SUCCESS"))
            if observation == "NO_EFFECT":
                return self._reply("ALLOW", "VERIFIED_FAILURE", "SIMULATED_POSTCONDITION_NEGATIVE", action_digest, ("AUTHORIZED", "DISPATCHED", "EXECUTED_UNVERIFIED", "VERIFIED_FAILURE"))
        return self._reply("ALLOW", "EXECUTED_UNVERIFIED", "ACK_ONLY_NO_POSTCONDITION", action_digest, ("AUTHORIZED", "DISPATCHED", "EXECUTED_UNVERIFIED"))
