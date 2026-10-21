"""G09 executable authorization fixtures layered on an unmodified G08 isolated kernel.

SECURITY SCOPE: Everything named 'trusted' below is test-harness configured and
in-process only. These are NOT verified JWTs, MFA, HSM signatures, a secure
identity provider or a durable distributed policy decision point. Fail closed.
"""
from __future__ import annotations

import datetime as dt
import threading
from dataclasses import dataclass, replace
from typing import Callable

from cai_g08.contracts import instant
from cai_g08.engine import Gate08Sandbox, sha_ref

CLASS_RANK = {"PUBLIC": 0, "INTERNAL": 1, "CONFIDENTIAL": 2, "RESTRICTED": 3}
IMPACT_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
RISK_OT = frozenset({"NONE", "OT_REVIEW_REQUIRED", "OT_SAFETY_CRITICAL"})


@dataclass(frozen=True)
class DirectoryActor:
    subject: str
    tenant: str
    roles: frozenset[str]
    assurance: str  # 'LAB_ASSERTED_HIGH' is a fixture, never proof of MFA
    expires_at: str
    active: bool = True


@dataclass(frozen=True)
class Delegation:
    delegation_ref: str
    principal: str
    agent: str
    tenant: str
    allowed_tool_ids: frozenset[str]
    allowed_operations: frozenset[str]
    expires_at: str
    active: bool = True


class FixtureDirectory:
    """Thread-safe in-memory directory. All identities/delegations are fixture statements."""
    def __init__(self, actors: tuple[DirectoryActor, ...], delegations: tuple[Delegation, ...]):
        if len({(a.tenant, a.subject) for a in actors}) != len(actors):
            raise ValueError("DUPLICATE_ACTOR_IN_FIXTURE")
        if len({(d.tenant, d.delegation_ref) for d in delegations}) != len(delegations):
            raise ValueError("DUPLICATE_DELEGATION_IN_FIXTURE")
        self._lock = threading.RLock()
        self._actors = {(a.tenant, a.subject): a for a in actors}
        self._delegations = {(d.tenant, d.delegation_ref): d for d in delegations}

    def actor(self, tenant: str, subject: str) -> DirectoryActor | None:
        with self._lock:
            return self._actors.get((tenant, subject))

    def delegation(self, tenant: str, reference: str) -> Delegation | None:
        with self._lock:
            return self._delegations.get((tenant, reference))

    def replace_actor(self, actor: DirectoryActor) -> None:
        """TEST-ONLY mutation to exercise revocation/TOCTOU. No external directory."""
        with self._lock:
            if (actor.tenant, actor.subject) not in self._actors:
                raise KeyError("UNKNOWN_ACTOR")
            self._actors[(actor.tenant, actor.subject)] = actor

    def replace_delegation(self, delegation: Delegation) -> None:
        with self._lock:
            if (delegation.tenant, delegation.delegation_ref) not in self._delegations:
                raise KeyError("UNKNOWN_DELEGATION")
            self._delegations[(delegation.tenant, delegation.delegation_ref)] = delegation


@dataclass(frozen=True)
class Rule:
    """Explicit per-role allow/deny; no wildcards, no implicit escalation."""
    effect: str   # DENY / ALLOW
    role: str
    tools: frozenset[str]
    operations: frozenset[str]
    targets: frozenset[str]
    effect_types: frozenset[str]
    jurisdictions: frozenset[str]
    sectors: frozenset[str]
    data_classes: frozenset[str]
    impacts: frozenset[str]
    ot_safety_classes: frozenset[str]
    max_blast_radius: int

    def __post_init__(self) -> None:
        if (self.effect not in {"ALLOW", "DENY"} or not self.role or
            not self.tools or not self.operations or not self.targets or
            not self.effect_types <= frozenset({"READ_ONLY", "EFFECTFUL"}) or
            not self.jurisdictions or not self.sectors or
            not self.data_classes or not self.data_classes <= frozenset(CLASS_RANK) or
            not self.impacts or not self.impacts <= frozenset(IMPACT_RANK) or
            not self.ot_safety_classes or not self.ot_safety_classes <= RISK_OT or
            type(self.max_blast_radius) is not int or self.max_blast_radius < 0):
            raise ValueError("INVALID_POLICY_RULE")

    def matches(self, roles: frozenset[str], req: dict) -> bool:
        action, risk = req["action"], req["risk"]
        return (self.role in roles and
                action["tool_id"] in self.tools and
                action["operation"] in self.operations and
                action["target_ref"] in self.targets and
                action["effect_type"] in self.effect_types and
                req["jurisdiction"] in self.jurisdictions and
                req["sector_id"] in self.sectors and
                req["data_classification"] in self.data_classes and
                risk["impact"] in self.impacts and
                risk["ot_safety_class"] in self.ot_safety_classes and
                risk["blast_radius"] <= self.max_blast_radius)


def policy_fingerprint(tenant: str, audience: str, version: str, rules: tuple[Rule, ...]) -> str:
    # Local deterministic encoding; NOT a signed policy, NOT RFC 8785.
    def encode(rule: Rule) -> dict:
        return {
            "effect": rule.effect, "role": rule.role,
            "tools": sorted(rule.tools), "operations": sorted(rule.operations),
            "targets": sorted(rule.targets), "effect_types": sorted(rule.effect_types),
            "jurisdictions": sorted(rule.jurisdictions), "sectors": sorted(rule.sectors),
            "data_classes": sorted(rule.data_classes), "impacts": sorted(rule.impacts),
            "ot_safety_classes": sorted(rule.ot_safety_classes),
            "max_blast_radius": rule.max_blast_radius,
        }
    return sha_ref({"g09": "policy-fixture-v1", "tenant": tenant, "audience": audience,
                    "version": version, "rules": [encode(r) for r in rules]})


@dataclass(frozen=True)
class ScopedApproval:
    """INSECURE TEST ASSERTION. Not an actual signature or real human approval."""
    approver: str
    tenant: str
    audience: str
    request_id: str
    nonce: str
    action_digest: str
    request_digest: str
    context_digest: str
    policy_digest: str
    purpose: str
    expires_at: str
    provenance: str = "G09_LAB_FIXTURE_NOT_CRYPTOGRAPHIC"


class Gate09Sandbox(Gate08Sandbox):
    """G09 policy enforcement on G08's no-network fixture executor.

    G08.run performs a pre-dispatch _policy_and_tool/_approve_fixture recheck.
    Overrides below ensure a revoked principal/delegation, changed rules, or
    expired approval cannot pass that recheck. The external execution boundary
    still does not exist: no atomicity claim beyond in-memory nonce consume.
    """
    def __init__(self, *args, directory: FixtureDirectory, rules: tuple[Rule, ...],
                 approvals: tuple[ScopedApproval, ...] = (),
                 policy_version: str = "g09-lab-v1", **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(directory, FixtureDirectory):
            raise TypeError("LAB_DIRECTORY_REQUIRED")
        if not rules or any(type(r) is not Rule for r in rules):
            raise ValueError("LAB_POLICY_RULES_REQUIRED")
        self.directory = directory
        self.rules = rules
        self.scoped_approvals = approvals
        self.policy_version = policy_version

    def _policy_and_tool(self, req: dict) -> str | None:
        basic = super()._policy_and_tool(req)
        if basic:
            return basic
        ident, policy = self.deps.identity, self.deps.policy
        if ident is None or policy is None:
            return "G09_AUTHORITY_UNAVAILABLE"
        now = self.deps.clock()
        actor = self.directory.actor(ident.tenant, ident.subject)
        if actor is None or not actor.active:
            return "G09_IDENTITY_NOT_ACTIVE"
        if actor.subject != ident.subject or actor.tenant != ident.tenant:
            return "G09_PRINCIPAL_BINDING_MISMATCH"
        if actor.roles != ident.roles or not actor.roles:
            return "G09_ROLE_CLAIMS_NOT_TRUSTED"
        if actor.assurance != "LAB_ASSERTED_HIGH" or instant(actor.expires_at, "ACTOR_EXPIRY") <= now:
            return "G09_ASSURANCE_OR_SESSION_INVALID"
        delegation = self.directory.delegation(req["tenant_id"], req["delegation_ref"])
        if delegation is None or not delegation.active:
            return "G09_DELEGATION_NOT_ACTIVE"
        if ((delegation.principal, delegation.agent, delegation.tenant, delegation.delegation_ref) !=
            (ident.subject, ident.agent, ident.tenant, req["delegation_ref"])):
            return "G09_DELEGATION_BINDING_MISMATCH"
        if instant(delegation.expires_at, "DELEGATION_EXPIRY") <= now:
            return "G09_DELEGATION_EXPIRED"
        action = req["action"]
        if action["tool_id"] not in delegation.allowed_tool_ids or action["operation"] not in delegation.allowed_operations:
            return "G09_DELEGATION_SCOPE_DENY"
        digest = policy_fingerprint(policy.tenant, policy.audience, self.policy_version, self.rules)
        if digest != req["policy_ref"]["policy_digest"] or digest != policy.policy_digest:
            return "G09_POLICY_BINDING_CHANGED"
        matching = [r for r in self.rules if r.matches(actor.roles, req)]
        if any(r.effect == "DENY" for r in matching):
            return "G09_EXPLICIT_DENY_OVERRIDE"
        if not any(r.effect == "ALLOW" for r in matching):
            return "G09_DEFAULT_DENY"
        return None

    def _approve_fixture(self, req: dict, action_digest: str, now: dt.datetime) -> str | None:
        if req["action"]["effect_type"] == "READ_ONLY":
            return None
        if not self.deps.simulation_approval_enabled:
            return "G09_LAB_APPROVALS_DISABLED"
        policy, requester = self.deps.policy, self.deps.identity
        if policy is None or requester is None:
            return "G09_AUTHORITY_UNAVAILABLE"
        # Risk-based dual control. OT always requires a separate safety officer.
        safety = req["risk"]["ot_safety_class"] != "NONE"
        dual = safety or req["risk"]["impact"] in {"HIGH", "CRITICAL"}
        required = 2 if dual else 1
        if len(self.scoped_approvals) != required:
            return "G09_APPROVAL_QUORUM_INVALID"
        seen: set[str] = set()
        purposes: set[str] = set()
        for approval in self.scoped_approvals:
            if type(approval) is not ScopedApproval or approval.provenance != "G09_LAB_FIXTURE_NOT_CRYPTOGRAPHIC":
                return "G09_APPROVAL_PROVENANCE_INVALID"
            if approval.approver == requester.subject or approval.approver == requester.agent or approval.approver in seen:
                return "G09_SEPARATION_OF_DUTIES"
            seen.add(approval.approver)
            approver = self.directory.actor(approval.tenant, approval.approver)
            if approver is None or not approver.active or approver.assurance != "LAB_ASSERTED_HIGH":
                return "G09_APPROVER_NOT_TRUSTED"
            if instant(approver.expires_at, "APPROVER_SESSION_EXPIRY") <= now:
                return "G09_APPROVER_SESSION_EXPIRED"
            if ((approval.tenant, approval.audience, approval.request_id, approval.nonce,
                 approval.action_digest, approval.request_digest, approval.context_digest, approval.policy_digest) !=
                (requester.tenant, policy.audience, req["request_id"], req["nonce"],
                 action_digest, sha_ref(req), req["context"]["snapshot_digest"], policy.policy_digest)):
                return "G09_APPROVAL_SCOPE_MISMATCH"
            if instant(approval.expires_at, "APPROVAL_EXPIRY") <= now:
                return "G09_APPROVAL_EXPIRED"
            if approval.purpose not in {"EXECUTE_ACTION", "OT_SAFETY_AUTHORIZATION", "SECOND_PERSON_REVIEW"}:
                return "G09_APPROVAL_PURPOSE_INVALID"
            need = "safety_officer" if approval.purpose == "OT_SAFETY_AUTHORIZATION" else "approver"
            if need not in approver.roles:
                return "G09_APPROVER_ROLE_MISMATCH"
            if approval.purpose in purposes:
                return "G09_DUPLICATE_APPROVAL_PURPOSE"
            purposes.add(approval.purpose)
        if "EXECUTE_ACTION" not in purposes:
            return "G09_PRIMARY_APPROVAL_MISSING"
        if safety and "OT_SAFETY_AUTHORIZATION" not in purposes:
            return "G09_OT_SAFETY_APPROVAL_MISSING"
        if dual and not safety and "SECOND_PERSON_REVIEW" not in purposes:
            return "G09_SECOND_PERSON_MISSING"
        return None
