"""GATE09 lab-only RBAC/ABAC/delegation/approvals; no real tokens, MFA, signatures or network."""
from __future__ import annotations

import dataclasses
import datetime as dt
import json
import threading
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor

from cai_g08.engine import (LeaseStore, SandboxDependencies, SimulatedExecutor,
                            SimulatedObserver, SimulatedWorld, TrustedContext,
                            TrustedIdentity, TrustedPolicy, TrustedTool, sha_ref)
from cai_g09.controls import (Delegation, DirectoryActor, FixtureDirectory,
                              Gate09Sandbox, Rule, ScopedApproval,
                              policy_fingerprint)

NOW = dt.datetime(2026, 10, 20, 20, 0, tzinfo=dt.timezone.utc)
DIG = lambda c: "sha256:" + c * 64


def iso(delta: int) -> str:
    return (NOW + dt.timedelta(seconds=delta)).isoformat()


def wire(obj: dict) -> bytes:
    return json.dumps(obj, separators=(",", ":")).encode("utf-8")


def fixture(effect: str = "EFFECTFUL", *, safety: str = "NONE", impact: str = "LOW"):
    req = {
        "schema_version": "0.2.1-draft",
        "request_id": str(uuid.uuid4()), "correlation_id": str(uuid.uuid4()),
        "principal_ref": "subject.requester", "agent_ref": "agent.fixture",
        "delegation_ref": "delegation.fixture", "tenant_id": "tenantA",
        "jurisdiction": "USA", "sector_id": "IT", "data_classification": "INTERNAL",
        "action": {"tool_id": "fixture.mock", "operation": "read" if effect == "READ_ONLY" else "mutate",
                   "target_ref": "object.fixture", "arguments_digest": DIG("1"),
                   "manifest_digest": DIG("2"), "effect_type": effect},
        "risk": {"impact": impact, "ot_safety_class": safety, "blast_radius": 1, "reversible": True},
        "context": {"dsa_ref": "DSA.fixture", "esa_ref": "ESA.fixture",
                    "snapshot_digest": DIG("3"), "observed_at": iso(0)},
        "policy_ref": {"policy_id": "policy.fixture", "policy_version": "v1", "policy_digest": ""},
        "evidence_refs": [], "nonce": "N" * 24, "expires_at": iso(120),
    }
    rule = Rule("ALLOW", "operator", frozenset({"fixture.mock"}),
                frozenset({"read", "mutate"}), frozenset({"object.fixture"}),
                frozenset({"READ_ONLY", "EFFECTFUL"}), frozenset({"USA"}),
                frozenset({"IT"}), frozenset({"INTERNAL"}),
                frozenset({"LOW", "MEDIUM", "HIGH", "CRITICAL"}),
                frozenset({"NONE", "OT_REVIEW_REQUIRED", "OT_SAFETY_CRITICAL"}), 10)
    rules = (rule,)
    pd = policy_fingerprint("tenantA", "fixture.gateway", "g09-lab-v1", rules)
    req["policy_ref"]["policy_digest"] = pd
    actors = (
        DirectoryActor("subject.requester", "tenantA", frozenset({"operator"}), "LAB_ASSERTED_HIGH", iso(300)),
        DirectoryActor("subject.approver1", "tenantA", frozenset({"approver"}), "LAB_ASSERTED_HIGH", iso(300)),
        DirectoryActor("subject.approver2", "tenantA", frozenset({"approver"}), "LAB_ASSERTED_HIGH", iso(300)),
        DirectoryActor("subject.safety", "tenantA", frozenset({"safety_officer"}), "LAB_ASSERTED_HIGH", iso(300)),
        DirectoryActor("subject.other", "tenantB", frozenset({"approver"}), "LAB_ASSERTED_HIGH", iso(300)),
    )
    delegation = Delegation("delegation.fixture", "subject.requester", "agent.fixture",
                            "tenantA", frozenset({"fixture.mock"}),
                            frozenset({"read", "mutate"}), iso(300))
    directory = FixtureDirectory(actors, (delegation,))
    deps = SandboxDependencies(
        identity=TrustedIdentity("subject.requester", "agent.fixture", "delegation.fixture",
                                 "tenantA", frozenset({"operator"})),
        context=TrustedContext("DSA.fixture", "ESA.fixture", DIG("3"), iso(0)),
        policy=TrustedPolicy("policy.fixture", "v1", pd, "tenantA", "fixture.gateway",
                             frozenset({"USA"}), frozenset({"IT"}),
                             frozenset({"operator", "approver", "safety_officer"}),
                             frozenset({"INTERNAL"})),
        tool=TrustedTool(**req["action"]), core_verdict="ALLOW", clock=lambda: NOW,
        simulation_approval_enabled=True)
    world = SimulatedWorld()
    engine = Gate09Sandbox(deps, LeaseStore(), SimulatedExecutor(world),
                           SimulatedObserver(world), directory=directory, rules=rules)
    if effect == "EFFECTFUL":
        engine.scoped_approvals = tuple(approvals(req, engine, safety=safety, impact=impact))
    return req, engine, world


def approvals(req: dict, engine: Gate09Sandbox, *, safety: str, impact: str):
    binding = {"tenant": req["tenant_id"], "audience": engine.deps.policy.audience,
               "action": req["action"], "policy_digest": req["policy_ref"]["policy_digest"],
               "context_digest": req["context"]["snapshot_digest"]}
    digest = sha_ref(binding)
    core = dict(tenant="tenantA", audience="fixture.gateway",
                request_id=req["request_id"], nonce=req["nonce"],
                action_digest=digest, request_digest=sha_ref(req), context_digest=DIG("3"),
                policy_digest=req["policy_ref"]["policy_digest"], expires_at=iso(90))
    yield ScopedApproval("subject.approver1", purpose="EXECUTE_ACTION", **core)
    if safety != "NONE":
        yield ScopedApproval("subject.safety", purpose="OT_SAFETY_AUTHORIZATION", **core)
    elif impact in ("HIGH", "CRITICAL"):
        yield ScopedApproval("subject.approver2", purpose="SECOND_PERSON_REVIEW", **core)


class Gate09Tests(unittest.TestCase):
    def blocked(self, req, engine, reason):
        outcome = engine.run(wire(req))
        self.assertEqual(outcome.execution, "BLOCKED", outcome)
        self.assertEqual(outcome.reason, reason, outcome)
        self.assertEqual(engine.executor.world.dispatches, 0)
        self.assertEqual(engine.lease.consumed_count, 0)
        return outcome

    def test_G09_001_valid_effectful_lab_execution(self):
        req, gate, world = fixture()
        result = gate.run(wire(req))
        self.assertTrue(result.simulation)
        self.assertEqual(result.execution, "VERIFIED_SUCCESS")
        self.assertEqual(world.dispatches, 1)

    def test_G09_002_valid_read_only_fixture_authorization(self):
        req, gate, _ = fixture("READ_ONLY")
        self.assertEqual(gate.run(wire(req)).decision, "ALLOW")

    def test_G09_003_no_actor_record_denied(self):
        req, gate, _ = fixture()
        gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.requester"), active=False))
        self.blocked(req, gate, "G09_IDENTITY_NOT_ACTIVE")

    def test_G09_004_directory_role_change_denied(self):
        req, gate, _ = fixture()
        gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.requester"), roles=frozenset({"admin"})))
        self.blocked(req, gate, "G09_ROLE_CLAIMS_NOT_TRUSTED")

    def test_G09_005_empty_role_set_denied(self):
        req, gate, _ = fixture()
        gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.requester"), roles=frozenset()))
        self.blocked(req, gate, "G09_ROLE_CLAIMS_NOT_TRUSTED")

    def test_G09_006_low_assurance_denied(self):
        req, gate, _ = fixture()
        gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.requester"), assurance="LAB_ASSERTED_LOW"))
        self.blocked(req, gate, "G09_ASSURANCE_OR_SESSION_INVALID")

    def test_G09_007_expired_actor_denied(self):
        req, gate, _ = fixture()
        gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.requester"), expires_at=iso(-1)))
        self.blocked(req, gate, "G09_ASSURANCE_OR_SESSION_INVALID")

    def test_G09_008_delegation_revoked_denied(self):
        req, gate, _ = fixture()
        d = gate.directory.delegation("tenantA", "delegation.fixture")
        gate.directory.replace_delegation(dataclasses.replace(d, active=False))
        self.blocked(req, gate, "G09_DELEGATION_NOT_ACTIVE")

    def test_G09_009_delegation_expired_denied(self):
        req, gate, _ = fixture()
        d = gate.directory.delegation("tenantA", "delegation.fixture")
        gate.directory.replace_delegation(dataclasses.replace(d, expires_at=iso(-1)))
        self.blocked(req, gate, "G09_DELEGATION_EXPIRED")

    def test_G09_010_delegation_wrong_agent_denied(self):
        req, gate, _ = fixture()
        d = gate.directory.delegation("tenantA", "delegation.fixture")
        gate.directory.replace_delegation(dataclasses.replace(d, agent="attacker.agent"))
        self.blocked(req, gate, "G09_DELEGATION_BINDING_MISMATCH")

    def test_G09_011_delegation_scope_downgrade_denied(self):
        req, gate, _ = fixture()
        d = gate.directory.delegation("tenantA", "delegation.fixture")
        gate.directory.replace_delegation(dataclasses.replace(d, allowed_operations=frozenset({"read"})))
        self.blocked(req, gate, "G09_DELEGATION_SCOPE_DENY")

    def test_G09_012_missing_role_allow_rule_denied(self):
        req, gate, _ = fixture()
        gate.rules = (dataclasses.replace(gate.rules[0], role="reader"),)
        new_digest = policy_fingerprint("tenantA", "fixture.gateway", "g09-lab-v1", gate.rules)
        gate.deps.policy = dataclasses.replace(gate.deps.policy, policy_digest=new_digest)
        req["policy_ref"]["policy_digest"] = new_digest
        self.blocked(req, gate, "G09_DEFAULT_DENY")

    def test_G09_013_policy_rule_tampering_denied(self):
        req, gate, _ = fixture()
        gate.rules = (dataclasses.replace(gate.rules[0], max_blast_radius=500),)
        self.blocked(req, gate, "G09_POLICY_BINDING_CHANGED")

    def test_G09_014_policy_version_tampering_denied(self):
        req, gate, _ = fixture()
        gate.policy_version = "changed"
        self.blocked(req, gate, "G09_POLICY_BINDING_CHANGED")

    def test_G09_015_blast_radius_over_threshold_denied(self):
        req, gate, _ = fixture()
        req["risk"]["blast_radius"] = 11
        self.blocked(req, gate, "G09_DEFAULT_DENY")

    def test_G09_016_wrong_target_denied(self):
        req, gate, _ = fixture()
        req["action"]["target_ref"] = "object.other"
        gate.deps.tool = dataclasses.replace(gate.deps.tool, target_ref="object.other")
        self.blocked(req, gate, "G09_DEFAULT_DENY")

    def test_G09_017_cross_tenant_claim_denied(self):
        req, gate, _ = fixture()
        req["tenant_id"] = "tenantB"
        self.blocked(req, gate, "UNTRUSTED_PRINCIPAL_OR_TENANT")

    def test_G09_018_unknown_jurisdiction_denied(self):
        req, gate, _ = fixture()
        req["jurisdiction"] = "ZZ"
        self.blocked(req, gate, "UNKNOWN_JURISDICTION_OR_SECTOR")

    def test_G09_019_high_impact_dual_control_success(self):
        req, gate, _ = fixture(impact="HIGH")
        self.assertEqual(gate.run(wire(req)).execution, "VERIFIED_SUCCESS")

    def test_G09_020_critical_impact_dual_control_success(self):
        req, gate, _ = fixture(impact="CRITICAL")
        self.assertEqual(gate.run(wire(req)).execution, "VERIFIED_SUCCESS")

    def test_G09_021_ot_safety_requires_safety_officer(self):
        req, gate, _ = fixture(safety="OT_SAFETY_CRITICAL")
        gate.scoped_approvals = gate.scoped_approvals[:1]
        self.blocked(req, gate, "G09_APPROVAL_QUORUM_INVALID")

    def test_G09_022_ot_safety_two_distinct_valid_lab_approvers(self):
        req, gate, _ = fixture(safety="OT_SAFETY_CRITICAL")
        self.assertEqual(gate.run(wire(req)).execution, "VERIFIED_SUCCESS")

    def test_G09_023_high_risk_missing_second_reviewer(self):
        req, gate, _ = fixture(impact="HIGH")
        gate.scoped_approvals = (gate.scoped_approvals[0], dataclasses.replace(gate.scoped_approvals[1], purpose="OT_SAFETY_AUTHORIZATION"))
        self.blocked(req, gate, "G09_APPROVER_ROLE_MISMATCH")

    def test_G09_024_requester_self_approval_rejected(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], approver="subject.requester"),)
        self.blocked(req, gate, "G09_SEPARATION_OF_DUTIES")

    def test_G09_025_duplicate_approver_rejected(self):
        req, gate, _ = fixture(impact="HIGH")
        gate.scoped_approvals = (gate.scoped_approvals[0], dataclasses.replace(gate.scoped_approvals[1], approver="subject.approver1"))
        self.blocked(req, gate, "G09_SEPARATION_OF_DUTIES")

    def test_G09_026_approver_revocation_rechecked(self):
        req, gate, _ = fixture()
        approver = gate.directory.actor("tenantA", "subject.approver1")
        gate.directory.replace_actor(dataclasses.replace(approver, active=False))
        self.blocked(req, gate, "G09_APPROVER_NOT_TRUSTED")

    def test_G09_027_approver_wrong_role_rejected(self):
        req, gate, _ = fixture()
        gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.approver1"), roles=frozenset({"viewer"})))
        self.blocked(req, gate, "G09_APPROVER_ROLE_MISMATCH")

    def test_G09_028_approver_wrong_tenant_rejected(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], tenant="tenantB"),)
        self.blocked(req, gate, "G09_APPROVER_NOT_TRUSTED")

    def test_G09_029_wrong_audience_rejected(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], audience="other.gateway"),)
        self.blocked(req, gate, "G09_APPROVAL_SCOPE_MISMATCH")

    def test_G09_030_wrong_nonce_rejected(self):
        req, gate, _ = fixture()
        req["nonce"] = "Z" * 24
        self.blocked(req, gate, "G09_APPROVAL_SCOPE_MISMATCH")

    def test_G09_031_wrong_request_id_rejected(self):
        req, gate, _ = fixture()
        req["request_id"] = str(uuid.uuid4())
        self.blocked(req, gate, "G09_APPROVAL_SCOPE_MISMATCH")

    def test_G09_032_wrong_action_digest_rejected(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], action_digest=DIG("d")),)
        self.blocked(req, gate, "G09_APPROVAL_SCOPE_MISMATCH")

    def test_G09_033_expired_approval_rejected(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], expires_at=iso(-1)),)
        self.blocked(req, gate, "G09_APPROVAL_EXPIRED")

    def test_G09_034_invalid_provenance_rejected(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], provenance="JWT_SPOOF"),)
        self.blocked(req, gate, "G09_APPROVAL_PROVENANCE_INVALID")

    def test_G09_035_cross_purpose_approval_rejected(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], purpose="READ_LOGS"),)
        self.blocked(req, gate, "G09_APPROVAL_PURPOSE_INVALID")

    def test_G09_036_pre_dispatch_identity_revoked(self):
        req, gate, _ = fixture()
        def revoke():
            gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.requester"), active=False))
        result = gate.run(wire(req), before_dispatch=revoke)
        self.assertEqual(result.reason, "PRE_DISPATCH_POLICY_OR_CORE_CHANGED")
        self.assertEqual(gate.executor.world.dispatches, 0)

    def test_G09_037_pre_dispatch_delegation_revoked(self):
        req, gate, _ = fixture()
        def revoke():
            d = gate.directory.delegation("tenantA", "delegation.fixture")
            gate.directory.replace_delegation(dataclasses.replace(d, active=False))
        result = gate.run(wire(req), before_dispatch=revoke)
        self.assertEqual(result.reason, "PRE_DISPATCH_POLICY_OR_CORE_CHANGED")
        self.assertEqual(gate.executor.world.dispatches, 0)

    def test_G09_038_pre_dispatch_role_changes(self):
        req, gate, _ = fixture()
        def mutate():
            gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.requester"), roles=frozenset({"viewer"})))
        self.assertEqual(gate.run(wire(req), before_dispatch=mutate).reason, "PRE_DISPATCH_POLICY_OR_CORE_CHANGED")

    def test_G09_039_pre_dispatch_approver_revoked(self):
        req, gate, _ = fixture()
        def mutate():
            gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.approver1"), active=False))
        self.assertEqual(gate.run(wire(req), before_dispatch=mutate).reason, "PRE_DISPATCH_APPROVAL_INVALID")

    def test_G09_040_pre_dispatch_policy_changed(self):
        req, gate, _ = fixture()
        def mutate():
            gate.rules = (dataclasses.replace(gate.rules[0], max_blast_radius=20),)
        self.assertEqual(gate.run(wire(req), before_dispatch=mutate).reason, "PRE_DISPATCH_POLICY_OR_CORE_CHANGED")

    def test_G09_041_pre_dispatch_clock_expiry(self):
        req, gate, _ = fixture()
        def expire(): gate.deps.clock = lambda: NOW + dt.timedelta(seconds=150)
        self.assertEqual(gate.run(wire(req), before_dispatch=expire).reason, "EXPIRED_BEFORE_DISPATCH")

    def test_G09_042_replay_same_nonce_denied(self):
        req, gate, world = fixture()
        self.assertEqual(gate.run(wire(req)).execution, "VERIFIED_SUCCESS")
        self.assertEqual(gate.run(wire(req)).reason, "NONCE_REPLAY")
        self.assertEqual(world.dispatches, 1)

    def test_G09_043_nonce_rebinding_rejected(self):
        req, gate, world = fixture()
        self.assertEqual(gate.run(wire(req)).execution, "VERIFIED_SUCCESS")
        req["nonce"] = "Y" * 24
        self.assertEqual(gate.run(wire(req)).reason, "G09_APPROVAL_SCOPE_MISMATCH")
        self.assertEqual(world.dispatches, 1)

    def test_G09_044_concurrent_nonce_one_winner(self):
        req, gate, world = fixture()
        with ThreadPoolExecutor(max_workers=12) as pool:
            result = list(pool.map(gate.run, [wire(req)] * 32))
        self.assertEqual(sum(1 for r in result if r.execution == "VERIFIED_SUCCESS"), 1)
        self.assertEqual(sum(1 for r in result if r.reason == "NONCE_REPLAY"), 31)
        self.assertEqual(world.dispatches, 1)

    def test_G09_045_missing_approval_denied(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = ()
        self.blocked(req, gate, "G09_APPROVAL_QUORUM_INVALID")

    def test_G09_046_disabled_approvals_denied(self):
        req, gate, _ = fixture()
        gate.deps.simulation_approval_enabled = False
        self.blocked(req, gate, "G09_LAB_APPROVALS_DISABLED")

    def test_G09_047_trusted_core_hold_blocks(self):
        req, gate, _ = fixture()
        gate.deps.core_verdict = "HOLD"
        self.blocked(req, gate, "CANONICAL_CORE_ADAPTER_NOT_ALLOW")

    def test_G09_048_control_plane_unavailable_blocks(self):
        req, gate, _ = fixture()
        gate.deps.availability = False
        self.blocked(req, gate, "CONTROL_PLANE_UNAVAILABLE")

    def test_G09_049_approver_session_expired(self):
        req, gate, _ = fixture()
        gate.directory.replace_actor(dataclasses.replace(gate.directory.actor("tenantA", "subject.approver1"), expires_at=iso(-1)))
        self.blocked(req, gate, "G09_APPROVER_SESSION_EXPIRED")

    def test_G09_050_explicit_deny_override(self):
        req, gate, _ = fixture()
        deny = dataclasses.replace(gate.rules[0], effect="DENY")
        gate.rules = gate.rules + (deny,)
        pd = policy_fingerprint("tenantA", "fixture.gateway", "g09-lab-v1", gate.rules)
        gate.deps.policy = dataclasses.replace(gate.deps.policy, policy_digest=pd)
        req["policy_ref"]["policy_digest"] = pd
        gate.scoped_approvals = tuple(approvals(req, gate, safety="NONE", impact="LOW"))
        self.blocked(req, gate, "G09_EXPLICIT_DENY_OVERRIDE")

    def test_G09_051_invalid_policy_rejected_at_constructor(self):
        with self.assertRaises(ValueError):
            Rule("UNKNOWN", "operator", frozenset({"fixture.mock"}), frozenset({"mutate"}),
                 frozenset({"object.fixture"}), frozenset({"EFFECTFUL"}), frozenset({"USA"}),
                 frozenset({"IT"}), frozenset({"INTERNAL"}), frozenset({"LOW"}), frozenset({"NONE"}), 2)

    def test_G09_052_duplicate_identity_rejected_at_directory_init(self):
        actor = DirectoryActor("a", "tenantA", frozenset({"r"}), "LAB_ASSERTED_HIGH", iso(200))
        with self.assertRaises(ValueError):
            FixtureDirectory((actor, actor), ())

    def test_G09_053_no_external_executor(self):
        req, gate, _ = fixture()
        with self.assertRaises(TypeError):
            Gate09Sandbox(gate.deps, gate.lease, object(), gate.observer, directory=gate.directory, rules=gate.rules)

    def test_G09_054_wrong_data_classification_rejected(self):
        req, gate, _ = fixture()
        req["data_classification"] = "RESTRICTED"
        self.blocked(req, gate, "CLASSIFICATION_NOT_AUTHORIZED")

    def test_G09_055_pre_dispatch_approvals_changed(self):
        req, gate, _ = fixture()
        def mutate(): gate.scoped_approvals = ()
        self.assertEqual(gate.run(wire(req), before_dispatch=mutate).reason, "PRE_DISPATCH_APPROVAL_INVALID")

    def test_G09_056_risk_change_after_approval_rejected(self):
        req, gate, _ = fixture()
        req["risk"]["blast_radius"] = 2  # Still RBAC/ABAC-allowed but approval binds full request
        self.blocked(req, gate, "G09_APPROVAL_SCOPE_MISMATCH")

    def test_G09_057_approval_request_digest_tampered(self):
        req, gate, _ = fixture()
        gate.scoped_approvals = (dataclasses.replace(gate.scoped_approvals[0], request_digest=DIG("f")),)
        self.blocked(req, gate, "G09_APPROVAL_SCOPE_MISMATCH")

    def test_G09_058_evidence_chain_has_decision(self):
        req, gate, _ = fixture()
        gate.run(wire(req))
        self.assertTrue(gate.evidence.verify(gate.evidence.snapshot(), gate.evidence.head))


if __name__ == "__main__":
    unittest.main()
