"""Real OpenSSL ML-DSA-87 regression/adversarial tests (offline laboratory)."""
from __future__ import annotations

import copy
import datetime as dt
from pathlib import Path
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

from cai_g10.pqc import (
    ALGORITHM, DOMAIN, VERSION, ApprovalVerifier, Denied, Gate09CryptoGuard,
    Hold, OpenSslMldsa87, ReplayLedger, TrustedSigner, TrustRegistry,
    canonical, digest, envelope_lab, signing_bytes, strict_loads, utc,
)
from test_gate09 import fixture, NOW, approvals, wire


class CryptoLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.provider = OpenSslMldsa87()
        except Hold as exc:
            raise RuntimeError("HOLD: REAL ML-DSA-87 UNAVAILABLE") from exc
        cls.temp = tempfile.TemporaryDirectory(prefix="cai-g10-tests-")
        cls.keys = {}
        for actor, purpose in (("approver1", "EXECUTE_ACTION"),
                               ("approver2", "SECOND_PERSON_REVIEW"),
                               ("safety", "OT_SAFETY_AUTHORIZATION"),
                               ("outsider", "EXECUTE_ACTION")):
            secret, public = cls.provider.generate_lab_keypair(Path(cls.temp.name) / actor)
            cls.keys[actor] = (secret, public, cls.provider.key_id(public), purpose)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.anchors = TrustRegistry(self.provider, tuple(
            TrustedSigner(public_pem=info[1], key_id=info[2], approver_id="subject." + actor,
                          tenant_id="tenantA", allowed_purposes=frozenset({info[3]}))
            for actor, info in self.keys.items() if actor != "outsider"
        ))
        self.verifier = ApprovalVerifier(self.provider, self.anchors, ReplayLedger())
        self.binding = {
            "tenant_id": "tenantA", "audience": "fixture.gateway",
            "request_id": "REQ0001", "nonce": "N" * 24,
            "request_digest": "sha256:" + "a" * 64,
            "context_digest": "sha256:" + "b" * 64,
            "policy_digest": "sha256:" + "c" * 64,
        }

    def payload(self, actor="approver1", **updates):
        p = {
            "domain": DOMAIN, "version": VERSION, "tenant_id": self.binding["tenant_id"],
            "audience": self.binding["audience"], "purpose": self.keys[actor][3],
            "request_id": self.binding["request_id"], "nonce": self.binding["nonce"],
            "request_digest": self.binding["request_digest"],
            "context_digest": self.binding["context_digest"],
            "policy_digest": self.binding["policy_digest"],
            "issued_at": utc(NOW - dt.timedelta(seconds=5)),
            "expires_at": utc(NOW + dt.timedelta(seconds=90)),
            "approver_id": "subject." + actor, "decision": "APPROVE",
        }
        p.update(updates)
        return p

    def signed(self, actor="approver1", **updates):
        secret, public, _, _ = self.keys[actor]
        return envelope_lab(self.provider, secret, public, self.payload(actor, **updates))

    def accept(self, approvals_, purposes=None):
        self.verifier.authorize(approvals_, binding=self.binding,
                                purposes=purposes or frozenset({"EXECUTE_ACTION"}),
                                requester_id="subject.requester", now=NOW)

    def denied(self, approvals_, purposes=None):
        with self.assertRaises(Denied):
            self.accept(approvals_, purposes)

    def test_001_real_mldsa_signature(self):
        env = self.signed()
        self.assertEqual(env["algorithm"], "ML-DSA-87")
        self.assertEqual(len(__import__('base64').b64decode(env['signature_b64'])), 4627)
        self.accept([env])

    def test_002_real_openssl_version(self):
        self.assertIn("OpenSSL 3.5", self.provider.version)

    def test_003_canonical_order_is_deterministic(self):
        self.assertEqual(canonical({"z": 1, "a": 2}), b'{"a":2,"z":1}')

    def test_004_digest_is_canonical(self):
        self.assertEqual(digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1}))

    def test_005_replay_is_denied(self):
        env = self.signed()
        self.accept([env])
        self.denied([env])

    def test_006_tampered_request_digest_denied(self):
        env = self.signed()
        env["payload"]["request_digest"] = "sha256:" + "f" * 64
        self.denied([env])

    def test_007_tampered_context_denied(self):
        env = self.signed()
        env["payload"]["context_digest"] = "sha256:" + "f" * 64
        self.denied([env])

    def test_008_tampered_policy_denied(self):
        env = self.signed()
        env["payload"]["policy_digest"] = "sha256:" + "f" * 64
        self.denied([env])

    def test_009_tampered_approver_denied(self):
        env = self.signed()
        env["payload"]["approver_id"] = "subject.approver2"
        self.denied([env])

    def test_010_tampered_purpose_denied(self):
        env = self.signed()
        env["payload"]["purpose"] = "SECOND_PERSON_REVIEW"
        self.denied([env])

    def test_011_wrong_key_id_denied(self):
        env = self.signed()
        env["key_id"] = self.keys["approver2"][2]
        self.denied([env])

    def test_012_unknown_key_denied(self):
        env = self.signed("outsider")
        self.denied([env])

    def test_013_revoked_key_denied(self):
        env = self.signed()
        self.anchors.revoke(env["key_id"])
        self.denied([env])

    def test_014_expired_approval_denied(self):
        env = self.signed(issued_at=utc(NOW - dt.timedelta(seconds=70)), expires_at=utc(NOW))
        self.denied([env])

    def test_015_future_issue_denied(self):
        env = self.signed(issued_at=utc(NOW + dt.timedelta(seconds=17)))
        self.denied([env])

    def test_016_allowed_clock_skew(self):
        env = self.signed(issued_at=utc(NOW + dt.timedelta(seconds=10)))
        self.accept([env])

    def test_017_wrong_tenant_denied(self):
        self.denied([self.signed(tenant_id="tenantB")])

    def test_018_wrong_audience_denied(self):
        self.denied([self.signed(audience="other.gateway")])

    def test_019_wrong_nonce_denied(self):
        self.denied([self.signed(nonce="X" * 24)])

    def test_020_wrong_request_denied(self):
        self.denied([self.signed(request_id="REQ9999")])

    def test_021_wrong_domain_denied(self):
        with self.assertRaises(Denied):
            self.signed(domain="OTHER")

    def test_022_wrong_version_denied(self):
        with self.assertRaises(Denied):
            self.signed(version="g11")

    def test_023_wrong_decision_denied(self):
        with self.assertRaises(Denied):
            self.signed(decision="DENY")

    def test_024_unsupported_algorithm_denied(self):
        env = self.signed()
        env["algorithm"] = "Ed25519"
        self.denied([env])

    def test_025_invalid_signature_base64_denied(self):
        env = self.signed()
        env["signature_b64"] = "no$$$"
        self.denied([env])

    def test_026_modified_signature_denied(self):
        env = self.signed()
        import base64
        sig = bytearray(base64.b64decode(env["signature_b64"]))
        sig[71] ^= 1
        env["signature_b64"] = base64.b64encode(sig).decode("ascii")
        self.denied([env])

    def test_027_signature_truncated_denied(self):
        env = self.signed()
        env["signature_b64"] = env["signature_b64"][:-10]
        self.denied([env])

    def test_028_signature_wrong_key_denied(self):
        env = self.signed()
        env["signature_b64"] = self.signed("approver2")["signature_b64"]
        self.denied([env])

    def test_029_extra_envelope_field_denied(self):
        env = self.signed()
        env["privileged"] = True
        self.denied([env])

    def test_030_extra_payload_field_denied(self):
        with self.assertRaises(Denied):
            self.signed(elevation=True)

    def test_031_broken_timestamp_denied(self):
        with self.assertRaises(Denied):
            self.signed(issued_at="2026-10-20T20:00:00+00:00")

    def test_032_excessive_lifetime_denied(self):
        with self.assertRaises(Denied):
            self.signed(expires_at=utc(NOW + dt.timedelta(seconds=400)))

    def test_033_duplicate_json_key_denied(self):
        with self.assertRaisesRegex(Denied, "DUPLICATE_JSON_KEY"):
            strict_loads('{"approver_id":"a","approver_id":"b"}')

    def test_034_nonfinite_float_denied(self):
        with self.assertRaises(Denied):
            strict_loads('{"bad":NaN}')

    def test_035_unicode_noncanonical_denied(self):
        with self.assertRaises(Denied):
            canonical({"x": "e\u0301"})

    def test_036_float_denied(self):
        with self.assertRaises(Denied):
            canonical({"x": 0.1})

    def test_037_approver_is_requester_denied(self):
        env = self.signed()
        env["payload"]["approver_id"] = "subject.requester"
        self.denied([env])

    def test_038_valid_dual_signature_quorum(self):
        self.accept([self.signed(), self.signed("approver2")],
                    frozenset({"EXECUTE_ACTION", "SECOND_PERSON_REVIEW"}))

    def test_039_missing_second_approver_denied(self):
        self.denied([self.signed()], frozenset({"EXECUTE_ACTION", "SECOND_PERSON_REVIEW"}))

    def test_040_duplicate_approver_denied(self):
        self.denied([self.signed(), self.signed()],
                    frozenset({"EXECUTE_ACTION", "SECOND_PERSON_REVIEW"}))

    def test_041_safety_quorum_passes(self):
        self.accept([self.signed(), self.signed("safety")],
                    frozenset({"EXECUTE_ACTION", "OT_SAFETY_AUTHORIZATION"}))

    def test_042_wrong_quorum_purpose_denied(self):
        self.denied([self.signed(), self.signed("safety")],
                    frozenset({"EXECUTE_ACTION", "SECOND_PERSON_REVIEW"}))

    def test_043_long_purpose_denied(self):
        with self.assertRaises(Denied):
            self.signed(purpose="X" * 129)

    def test_044_unsupported_key_algorithm_denied(self):
        from subprocess import run
        with tempfile.TemporaryDirectory(prefix="cai-g10-ecdsa-") as tmp:
            key, pub = Path(tmp)/"ec.pem", Path(tmp)/"ec-pub.pem"
            r = run([self.provider.binary, "genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:prime256v1", "-out", str(key)], capture_output=True)
            self.assertEqual(r.returncode, 0)
            r = run([self.provider.binary, "pkey", "-in", str(key), "-pubout", "-out", str(pub)], capture_output=True)
            self.assertEqual(r.returncode, 0)
            with self.assertRaises(Denied):
                self.provider.key_id(pub.read_bytes())

    def test_045_tampered_trust_anchor_denied(self):
        signer = TrustedSigner(self.keys["approver1"][1], self.keys["approver2"][2], "subject.approver1", "tenantA", frozenset({"EXECUTE_ACTION"}))
        with self.assertRaises(Denied):
            TrustRegistry(self.provider, [signer])

    def test_046_replay_concurrent_one_success(self):
        env = self.signed()
        outcomes = []
        def worker(_):
            try:
                self.accept([env])
                return "PASS"
            except Denied:
                return "DENIED"
        with ThreadPoolExecutor(max_workers=6) as pool:
            outcomes = list(pool.map(worker, range(10)))
        self.assertEqual(outcomes.count("PASS"), 1)
        self.assertEqual(outcomes.count("DENIED"), 9)

    def test_047_failed_signature_does_not_consume_replay(self):
        env = self.signed()
        bogus = copy.deepcopy(env)
        bogus["payload"]["request_id"] = "REQ9999"
        self.denied([bogus])
        self.accept([env])

    def test_048_rejected_quorum_does_not_consume_approval(self):
        env = self.signed()
        self.denied([env], frozenset({"EXECUTE_ACTION", "SECOND_PERSON_REVIEW"}))
        self.accept([env])

    def test_049_g09_guard_valid_approval_runs_fixture(self):
        req, engine, world = fixture(effect="EFFECTFUL")
        self.binding.update({"tenant_id": req["tenant_id"], "audience": engine.deps.policy.audience,
                             "request_id": req["request_id"], "nonce": req["nonce"],
                             "request_digest": digest(req),
                             "context_digest": req["context"]["snapshot_digest"],
                             "policy_digest": req["policy_ref"]["policy_digest"]})
        guard = Gate09CryptoGuard(self.verifier, engine)
        outcome = guard.run(req, [self.signed()], purposes=frozenset({"EXECUTE_ACTION"}), now=NOW)
        self.assertNotEqual(outcome.execution, "BLOCKED")
        self.assertEqual(world.dispatches, 1)

    def test_050_g09_guard_bad_crypto_never_dispatches(self):
        req, engine, world = fixture(effect="EFFECTFUL")
        self.binding.update({"tenant_id": req["tenant_id"], "audience": engine.deps.policy.audience,
                             "request_id": req["request_id"], "nonce": req["nonce"],
                             "request_digest": digest(req),
                             "context_digest": req["context"]["snapshot_digest"],
                             "policy_digest": req["policy_ref"]["policy_digest"]})
        env = self.signed()
        env["payload"]["request_id"] = "ATTACK"
        guard = Gate09CryptoGuard(self.verifier, engine)
        with self.assertRaises(Denied):
            guard.run(req, [env], purposes=frozenset({"EXECUTE_ACTION"}), now=NOW)
        self.assertEqual(world.dispatches, 0)

    def test_051_g09_guard_changed_context_never_dispatches(self):
        req, engine, world = fixture(effect="EFFECTFUL")
        self.binding.update({"tenant_id": req["tenant_id"], "audience": engine.deps.policy.audience,
                             "request_id": req["request_id"], "nonce": req["nonce"],
                             "request_digest": digest(req),
                             "context_digest": req["context"]["snapshot_digest"],
                             "policy_digest": req["policy_ref"]["policy_digest"]})
        env = self.signed()
        req["context"]["snapshot_digest"] = "sha256:" + "9"*64
        guard = Gate09CryptoGuard(self.verifier, engine)
        with self.assertRaises(Denied):
            guard.run(req, [env], purposes=frozenset({"EXECUTE_ACTION"}), now=NOW)
        self.assertEqual(world.dispatches, 0)

    def test_052_no_fake_signature_is_accepted(self):
        env = self.signed()
        env["signature_b64"] = __import__('base64').b64encode(b'0' * 4627).decode('ascii')
        self.denied([env])

    def use_g09_fixture(self, impact="LOW", safety="NONE"):
        req, engine, world = fixture(effect="EFFECTFUL", impact=impact, safety=safety)
        self.binding.update({"tenant_id": req["tenant_id"], "audience": engine.deps.policy.audience,
                             "request_id": req["request_id"], "nonce": req["nonce"],
                             "request_digest": digest(req),
                             "context_digest": req["context"]["snapshot_digest"],
                             "policy_digest": req["policy_ref"]["policy_digest"]})
        return req, engine, world

    def test_053_high_risk_quorum_cannot_be_downgraded(self):
        req, engine, world = self.use_g09_fixture(impact="HIGH")
        with self.assertRaisesRegex(Denied, "QUORUM_POLICY_DOWNGRADE"):
            Gate09CryptoGuard(self.verifier, engine).run(req, [self.signed()],
                purposes=frozenset({"EXECUTE_ACTION"}), now=NOW)
        self.assertEqual(world.dispatches, 0)

    def test_054_ot_safety_quorum_cannot_be_downgraded(self):
        req, engine, world = self.use_g09_fixture(safety="OT_SAFETY_CRITICAL")
        with self.assertRaisesRegex(Denied, "QUORUM_POLICY_DOWNGRADE"):
            Gate09CryptoGuard(self.verifier, engine).run(req, [self.signed()],
                purposes=frozenset({"EXECUTE_ACTION"}), now=NOW)
        self.assertEqual(world.dispatches, 0)

    def test_055_real_dual_quorum_allows_g09_mock(self):
        req, engine, world = self.use_g09_fixture(impact="HIGH")
        result = Gate09CryptoGuard(self.verifier, engine).run(req,
            [self.signed(), self.signed("approver2")],
            purposes=frozenset({"EXECUTE_ACTION", "SECOND_PERSON_REVIEW"}), now=NOW)
        self.assertNotEqual(result.execution, "BLOCKED")
        self.assertEqual(world.dispatches, 1)

    def test_056_real_ot_safety_quorum_allows_g09_mock(self):
        req, engine, world = self.use_g09_fixture(safety="OT_SAFETY_CRITICAL")
        result = Gate09CryptoGuard(self.verifier, engine).run(req,
            [self.signed(), self.signed("safety")],
            purposes=frozenset({"EXECUTE_ACTION", "OT_SAFETY_AUTHORIZATION"}), now=NOW)
        self.assertNotEqual(result.execution, "BLOCKED")
        self.assertEqual(world.dispatches, 1)

    def test_057_trust_anchor_rotation_explicit(self):
        old_env = self.signed()
        new_signer = TrustedSigner(self.keys["approver2"][1], self.keys["approver2"][2],
                                   "subject.approver2", "tenantA", frozenset({"SECOND_PERSON_REVIEW"}))
        rotated = ApprovalVerifier(self.provider, TrustRegistry(self.provider, [new_signer]), ReplayLedger())
        with self.assertRaises(Denied):
            rotated.authorize([old_env], binding=self.binding, purposes=frozenset({"EXECUTE_ACTION"}),
                              requester_id="subject.requester", now=NOW)
        rotated.authorize([self.signed("approver2")], binding=self.binding,
                          purposes=frozenset({"SECOND_PERSON_REVIEW"}), requester_id="subject.requester", now=NOW)


if __name__ == '__main__':
    unittest.main()
