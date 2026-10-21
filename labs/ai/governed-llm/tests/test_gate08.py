"""Executable isolated fixture tests; no production CAI CORE, HSM, MCP or network."""
from __future__ import annotations

import copy
import dataclasses
import datetime as dt
import json
import threading
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor

from cai_g08.contracts import ContractError, canonical_local_bytes, decode_json, validate_request
from cai_g08.engine import (
    Gate08Sandbox, LeaseStore, SandboxApproval, SandboxDependencies,
    SimulatedExecutor, SimulatedObserver, SimulatedWorld, TrustedContext,
    TrustedIdentity, TrustedPolicy, TrustedTool, sha_ref,
)
from cai_g08.evidence import EvidenceLog, Event

NOW = dt.datetime(2026, 10, 20, 20, 0, tzinfo=dt.timezone.utc)
DIG = lambda c: "sha256:" + c * 64


def timestamp(offset: int) -> str:
    return (NOW + dt.timedelta(seconds=offset)).isoformat()


def make_request(effect: str = "READ_ONLY", safety: str = "NONE") -> dict:
    return {
        "schema_version": "0.2.1-draft",
        "request_id": str(uuid.uuid4()),
        "correlation_id": str(uuid.uuid4()),
        "principal_ref": "subject.requester", "agent_ref": "agent.fixture", "delegation_ref": "delegation.fixture",
        "tenant_id": "tenantA", "jurisdiction": "USA", "sector_id": "IT",
        "data_classification": "INTERNAL",
        "action": {"tool_id": "fixture.mock", "operation": "read" if effect == "READ_ONLY" else "mutate",
                   "target_ref": "object.fixture", "arguments_digest": DIG("1"), "manifest_digest": DIG("2"), "effect_type": effect},
        "risk": {"impact": "LOW", "ot_safety_class": safety, "blast_radius": 1, "reversible": True},
        "context": {"dsa_ref": "DSA.fixture", "esa_ref": "ESA.fixture", "snapshot_digest": DIG("3"), "observed_at": timestamp(0)},
        "policy_ref": {"policy_id": "policy.fixture", "policy_version": "v1", "policy_digest": DIG("4")},
        "evidence_refs": [], "nonce": "N" * 24, "expires_at": timestamp(120),
    }


def wire(request: dict) -> bytes:
    return json.dumps(request, separators=(",", ":")).encode("utf-8")


def setup(effect="READ_ONLY", safety="NONE", *, approval=True):
    req = make_request(effect, safety)
    pol = TrustedPolicy("policy.fixture", "v1", DIG("4"), "tenantA", "fixture.gateway", frozenset({"USA"}), frozenset({"IT"}), frozenset({"analyst"}), frozenset({"INTERNAL"}))
    deps = SandboxDependencies(
        identity=TrustedIdentity("subject.requester", "agent.fixture", "delegation.fixture", "tenantA", frozenset({"analyst"})),
        context=TrustedContext("DSA.fixture", "ESA.fixture", DIG("3"), timestamp(0)),
        policy=pol,
        tool=TrustedTool(**req["action"]),
        core_verdict="ALLOW", clock=lambda: NOW,
    )
    world = SimulatedWorld()
    engine = Gate08Sandbox(deps, LeaseStore(), SimulatedExecutor(world), SimulatedObserver(world))
    if effect == "EFFECTFUL" and approval:
        grant_approval(req, engine)
    return req, engine, world


def grant_approval(req: dict, engine: Gate08Sandbox):
    binding = {"tenant": "tenantA", "audience": "fixture.gateway", "action": req["action"], "policy_digest": DIG("4"), "context_digest": DIG("3")}
    action_digest = sha_ref(binding)
    engine.deps.simulation_approval_enabled = True
    engine.deps.approvals = (SandboxApproval("subject.approver1", "tenantA", "fixture.gateway", action_digest, DIG("3"), DIG("4"), "EXECUTE_ACTION", timestamp(60)),)


class Gate08Tests(unittest.TestCase):
    def assert_blocked(self, req, eng, reason=None):
        out = eng.run(wire(req))
        self.assertEqual(out.execution, "BLOCKED", out)
        self.assertEqual(eng.executor.world.dispatches, 0)
        if reason:
            self.assertEqual(out.reason, reason)
        return out

    def test_P01_read_only_fixture_success_has_labeled_simulation(self):
        req, eng, world = setup()
        out = eng.run(wire(req))
        self.assertEqual(out.execution, "VERIFIED_SUCCESS")
        self.assertIn("SIMULATED", out.reason)
        self.assertTrue(out.simulation)
        self.assertEqual(world.dispatches, 1)

    def test_P02_core_missing_fails_closed(self):
        req, eng, _ = setup()
        eng.deps.core_verdict = "HOLD"
        self.assertEqual(self.assert_blocked(req, eng).decision, "HOLD")

    def test_P03_core_denial_fails_closed(self):
        req, eng, _ = setup()
        eng.deps.core_verdict = "DENY"
        self.assertEqual(self.assert_blocked(req, eng).decision, "DENY")

    def test_P04_corrupt_core_response_hold(self):
        req, eng, _ = setup()
        eng.deps.core_verdict = "GUESS"
        self.assert_blocked(req, eng, "CANONICAL_CORE_ADAPTER_INVALID")

    def test_P05_request_expired(self):
        req, eng, _ = setup()
        req["expires_at"] = timestamp(-1)
        self.assert_blocked(req, eng, "REQUEST_EXPIRED")

    def test_P06_valid_same_response_auditable_chain(self):
        req, eng, _ = setup()
        res = eng.run(wire(req))
        self.assertTrue(EvidenceLog.verify(eng.evidence.snapshot(), res.evidence_head))

    def test_P07_bad_schema_version(self):
        req, eng, _ = setup()
        req["schema_version"] = "production"
        self.assert_blocked(req, eng, "SCHEMA_VERSION_MISMATCH")

    def test_P08_policy_disables(self):
        req, eng, _ = setup()
        eng.deps.policy = dataclasses.replace(eng.deps.policy, enabled=False)
        self.assert_blocked(req, eng, "TRUSTED_POLICY_UNAVAILABLE")

    def test_P09_classification_fail_closed(self):
        req, eng, _ = setup()
        req["data_classification"] = "RESTRICTED"
        self.assert_blocked(req, eng, "CLASSIFICATION_NOT_AUTHORIZED")

    def test_P10_wrong_schema_extra_field(self):
        req, eng, _ = setup()
        req["admin"] = True
        self.assert_blocked(req, eng, "INVALID_FIELDS_REQUEST")

    def test_T01_missing_authenticated_identity(self):
        req, eng, _ = setup()
        eng.deps.identity = None
        self.assert_blocked(req, eng, "MISSING_TRUSTED_IDENTITY")

    def test_T02_low_privilege_subject(self):
        req, eng, _ = setup()
        eng.deps.identity = dataclasses.replace(eng.deps.identity, roles=frozenset({"viewer"}))
        self.assert_blocked(req, eng, "INSUFFICIENT_PRIVILEGE")

    def test_T03_separation_of_duties(self):
        req, eng, _ = setup("EFFECTFUL")
        item = eng.deps.approvals[0]
        eng.deps.approvals = (dataclasses.replace(item, subject="subject.requester"),)
        self.assert_blocked(req, eng, "SEPARATION_OF_DUTIES_VIOLATION")

    def test_T04_change_target_or_arguments_after_approval(self):
        req, eng, _ = setup("EFFECTFUL")
        req["action"]["arguments_digest"] = DIG("a")
        self.assert_blocked(req, eng, "UNTRUSTED_TOOL_OR_ARGUMENTS")

    def test_T05_expired_approval(self):
        req, eng, _ = setup("EFFECTFUL")
        eng.deps.approvals = (dataclasses.replace(eng.deps.approvals[0], expires_at=timestamp(-1)),)
        self.assert_blocked(req, eng, "APPROVAL_EXPIRED")

    def test_T06_nonce_replay_prevented(self):
        req, eng, world = setup("EFFECTFUL")
        first = eng.run(wire(req))
        second = eng.run(wire(req))
        self.assertEqual(first.execution, "VERIFIED_SUCCESS")
        self.assertEqual(second.reason, "NONCE_REPLAY")
        self.assertEqual(world.dispatches, 1)
        self.assertEqual(eng.lease.consumed_count, 1)

    def test_T07_untrusted_signature_approval_source_rejected(self):
        req, eng, _ = setup("EFFECTFUL")
        eng.deps.approvals = (dataclasses.replace(eng.deps.approvals[0], provenance="CLIENT_ASSERTED_CRYPTO"),)
        self.assert_blocked(req, eng, "UNTRUSTED_APPROVAL_SOURCE")

    def test_T08_cross_purpose_approval_rejected(self):
        req, eng, _ = setup("EFFECTFUL")
        eng.deps.approvals = (dataclasses.replace(eng.deps.approvals[0], purpose="EVIDENCE_CHECKPOINT"),)
        self.assert_blocked(req, eng, "APPROVAL_PURPOSE_REJECTED")

    def test_T10_context_drift_pre_dispatch(self):
        req, eng, _ = setup("EFFECTFUL")
        def drift():
            eng.deps.context = dataclasses.replace(eng.deps.context, snapshot_digest=DIG("5"))
        out = eng.run(wire(req), before_dispatch=drift)
        self.assertEqual(out.reason, "PRE_DISPATCH_CONTEXT_DRIFT")
        self.assertEqual(eng.executor.world.dispatches, 0)
        self.assertEqual(eng.lease.consumed_count, 0)

    def test_T12_unknown_mcp_tool_rejected(self):
        req, eng, _ = setup()
        eng.deps.tool = None
        self.assert_blocked(req, eng, "UNREGISTERED_TOOL")

    def test_T13_timeout_after_effect_indeterminate(self):
        req, eng, world = setup("EFFECTFUL")
        eng.executor.mode = "LOST_ACK_AFTER_EFFECT"
        out = eng.run(wire(req))
        self.assertEqual(out.execution, "INDETERMINATE")
        self.assertEqual(world.dispatches, 1)
        self.assertEqual(eng.run(wire(req)).reason, "NONCE_REPLAY")
        self.assertEqual(world.dispatches, 1)

    def test_T14_ack_is_not_effect_proof(self):
        req, eng, _ = setup("EFFECTFUL")
        eng.observer.available = False
        out = eng.run(wire(req))
        self.assertEqual(out.execution, "EXECUTED_UNVERIFIED")
        self.assertNotEqual(out.execution, "VERIFIED_SUCCESS")

    def test_T15_policy_digest_change_at_dispatch(self):
        req, eng, _ = setup("EFFECTFUL")
        def change():
            eng.deps.policy = dataclasses.replace(eng.deps.policy, policy_digest=DIG("6"))
        self.assertEqual(eng.run(wire(req), before_dispatch=change).reason, "PRE_DISPATCH_POLICY_OR_CORE_CHANGED")
        self.assertEqual(eng.executor.world.dispatches, 0)

    def test_T16_concurrent_nonce_dispatch_single_winner(self):
        req, eng, world = setup("EFFECTFUL")
        data = wire(req)
        with ThreadPoolExecutor(max_workers=8) as pool:
            outs = list(pool.map(eng.run, [data] * 24))
        self.assertEqual(sum(x.execution == "VERIFIED_SUCCESS" for x in outs), 1)
        self.assertEqual(sum(x.reason == "NONCE_REPLAY" for x in outs), 23)
        self.assertEqual(world.dispatches, 1)

    def test_T17_evidence_mutation_detected(self):
        log = EvidenceLog()
        log.append("EVENT", {"code": "A"})
        log.append("EVENT", {"code": "B"})
        original = log.snapshot()
        head = log.head
        self.assertTrue(EvidenceLog.verify(original, head))
        altered = list(original)
        altered[0] = dataclasses.replace(altered[0], details={"code": "EVIL"})
        self.assertFalse(EvidenceLog.verify(altered, head))
        self.assertFalse(EvidenceLog.verify(original[:1], head))

    def test_T18_safety_approval_required(self):
        req, eng, _ = setup("EFFECTFUL", "OT_SAFETY_CRITICAL")
        self.assert_blocked(req, eng, "APPROVALS_MISSING")

    def test_T19_duplicate_json_key_rejected(self):
        req, eng, _ = setup()
        encoded = wire(req)
        modified = encoded.replace(b'"tenant_id":"tenantA",', b'"tenant_id":"tenantB","tenant_id":"tenantA",')
        out = eng.run(modified)
        self.assertEqual(out.execution, "BLOCKED")
        self.assertIn("DUPLICATE", out.reason)

    def test_T20_cross_tenant_approval_rejected(self):
        req, eng, _ = setup("EFFECTFUL")
        eng.deps.approvals = (dataclasses.replace(eng.deps.approvals[0], tenant="tenantB"),)
        self.assert_blocked(req, eng, "APPROVAL_BINDING_MISMATCH")

    def test_T21_unregistered_jurisdiction_hold(self):
        req, eng, _ = setup()
        req["jurisdiction"] = "ZZ"
        out = self.assert_blocked(req, eng, "UNKNOWN_JURISDICTION_OR_SECTOR")
        self.assertEqual(out.decision, "HOLD")

    def test_T22_direct_external_executor_forbidden(self):
        req, eng, _ = setup()
        class BadExecutor:
            def dispatch(self, a):
                raise AssertionError("external")
        with self.assertRaises(TypeError):
            Gate08Sandbox(eng.deps, eng.lease, BadExecutor(), eng.observer)

    def test_T23_unavailable_control_plane(self):
        req, eng, _ = setup()
        eng.deps.evidence_available = False
        self.assert_blocked(req, eng, "CONTROL_PLANE_UNAVAILABLE")

    def test_T24_default_no_cryptography_no_effectful_authorization(self):
        req, eng, _ = setup("EFFECTFUL", approval=False)
        self.assert_blocked(req, eng, "PQC_SIGNATURE_AND_REAL_APPROVAL_NOT_CONFIGURED")

    def test_X01_spoofing_claims_blocked(self):
        req, eng, _ = setup()
        req["principal_ref"] = "superadmin"
        self.assert_blocked(req, eng, "UNTRUSTED_PRINCIPAL_OR_TENANT")

    def test_X02_wrong_tenant_blocked(self):
        req, eng, _ = setup()
        req["tenant_id"] = "tenantB"
        self.assert_blocked(req, eng, "UNTRUSTED_PRINCIPAL_OR_TENANT")

    def test_X03_cross_audience_approval_blocked(self):
        req, eng, _ = setup("EFFECTFUL")
        eng.deps.approvals = (dataclasses.replace(eng.deps.approvals[0], audience="tenantB.gateway"),)
        self.assert_blocked(req, eng, "APPROVAL_BINDING_MISMATCH")

    def test_X04_wrong_approval_policy_rejected(self):
        req, eng, _ = setup("EFFECTFUL")
        eng.deps.approvals = (dataclasses.replace(eng.deps.approvals[0], policy_digest=DIG("f")),)
        self.assert_blocked(req, eng, "APPROVAL_BINDING_MISMATCH")

    def test_X05_observation_negative_failure_not_success(self):
        req, eng, _ = setup()
        eng.observer.force_negative = True
        self.assertEqual(eng.run(wire(req)).execution, "VERIFIED_FAILURE")

    def test_X06_executor_failure_proven_before_effect(self):
        req, eng, world = setup()
        eng.executor.mode = "REJECT_BEFORE_EFFECT"
        self.assertEqual(eng.run(wire(req)).execution, "VERIFIED_FAILURE")
        self.assertEqual(world.dispatches, 0)

    def test_X07_weak_untimed_context_rejected(self):
        req, eng, _ = setup()
        req["context"]["observed_at"] = timestamp(-180)
        self.assert_blocked(req, eng, "CONTEXT_STALE_OR_DRIFTED")

    def test_X08_unicode_ambiguous_json_field_rejected(self):
        with self.assertRaises(ContractError):
            decode_json(b'{"na\\u0301me":1}')

    def test_X09_non_finite_number_rejected(self):
        with self.assertRaises(ContractError):
            decode_json(b'{"x":NaN}')

    def test_X10_bytes_limit_rejected(self):
        with self.assertRaises(ContractError):
            decode_json(b' ' * 17000)

    def test_X11_corrupt_utf8_rejected(self):
        with self.assertRaises(ContractError):
            decode_json(b'{"a":"\xff"}')

    def test_X12_time_without_tz_rejected(self):
        req, eng, _ = setup()
        req["expires_at"] = "2026-10-20T20:00:00"
        self.assert_blocked(req, eng, "TIMEZONE_REQUIRED_EXPIRES_AT")

    def test_X13_invalid_uuid_rejected(self):
        req, eng, _ = setup()
        req["request_id"] = "not-a-uuid"
        self.assert_blocked(req, eng, "INVALID_UUID_request_id")

    def test_X14_unexpected_action_field_rejected(self):
        req, eng, _ = setup()
        req["action"]["extra"] = "none"
        self.assert_blocked(req, eng, "INVALID_FIELDS_ACTION")

    def test_X15_pre_dispatch_role_change_rejected(self):
        req, eng, _ = setup("EFFECTFUL")
        def change():
            eng.deps.identity = dataclasses.replace(eng.deps.identity, roles=frozenset())
        self.assertEqual(eng.run(wire(req), before_dispatch=change).reason, "PRE_DISPATCH_POLICY_OR_CORE_CHANGED")

    def test_X16_expiry_before_dispatch(self):
        req, eng, _ = setup("EFFECTFUL")
        def move_clock():
            eng.deps.clock = lambda: NOW + dt.timedelta(seconds=180)
        self.assertEqual(eng.run(wire(req), before_dispatch=move_clock).reason, "EXPIRED_BEFORE_DISPATCH")

    def test_X17_execution_unknown_exception_is_indeterminate(self):
        req, eng, world = setup()
        def broken(*args):
            raise RuntimeError("unknown")
        eng.executor.dispatch = broken
        self.assertEqual(eng.run(wire(req)).execution, "INDETERMINATE")

    def test_X18_no_implicit_approval_on_effectful(self):
        req, eng, _ = setup("EFFECTFUL", approval=False)
        eng.deps.signer_available = True
        self.assert_blocked(req, eng, "PQC_SIGNATURE_AND_REAL_APPROVAL_NOT_CONFIGURED")

    def test_X19_safety_approval_two_distinct_fixture_signers(self):
        req, eng, _ = setup("EFFECTFUL", "OT_SAFETY_CRITICAL")
        binding = eng.deps.approvals[0]
        eng.deps.approvals = (binding, dataclasses.replace(binding, subject="subject.safety", purpose="OT_SAFETY_AUTHORIZATION"))
        out = eng.run(wire(req))
        self.assertEqual(out.execution, "VERIFIED_SUCCESS")
        self.assertTrue(out.simulation)

    def test_X20_duplicate_approvers_rejected(self):
        req, eng, _ = setup("EFFECTFUL", "OT_SAFETY_CRITICAL")
        item = eng.deps.approvals[0]
        eng.deps.approvals = (item, dataclasses.replace(item, purpose="OT_SAFETY_AUTHORIZATION"))
        self.assert_blocked(req, eng, "SEPARATION_OF_DUTIES_VIOLATION")

    def test_X21_non_clock_future_snapshot(self):
        req, eng, _ = setup()
        eng.deps.context = dataclasses.replace(eng.deps.context, observed_at=timestamp(100))
        req["context"]["observed_at"] = timestamp(100)
        self.assert_blocked(req, eng, "CONTEXT_STALE_OR_DRIFTED")

    def test_X22_evidence_absence_never_authorizes(self):
        req, eng, _ = setup()
        eng.deps.evidence_available = False
        out = eng.run(wire(req))
        self.assertEqual(out.execution, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
