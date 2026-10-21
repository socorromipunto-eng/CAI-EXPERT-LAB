"""GATE12 local sandbox-file effect tests; never production access."""
import base64
import copy
import datetime as dt
import os
import sqlite3
from contextlib import closing
import tempfile
import threading
import unittest
from pathlib import Path

from cai_g10.pqc import ApprovalVerifier, OpenSslMldsa87, ReplayLedger, TrustRegistry, TrustedSigner, digest, envelope_lab
from cai_g12.execution import (
    ControlledBroker, DOMAIN, EvidenceObserver, LabAuthority, LabEvidenceSigner,
    LabJournal, LocalEffectExecutor, PURPOSE, effect_bytes, target_name, validate_request,
)

NOW = dt.datetime(2026, 10, 20, 23, 0, tzinfo=dt.timezone.utc)
CONTEXT = digest({"simulated_context":"G12"})
POLICY = digest({"simulated_policy":"DENY_BY_DEFAULT"})


def request(**kw):
    req = {"domain":DOMAIN,"tenant_id":"tenant1","requester_id":"operator",
           "request_id":"op-a","nonce":"NonceABCDEF12345678","audience":"cai.lab.execution",
           "context_digest":CONTEXT,"policy_digest":POLICY,"operation":"PUT_ONCE",
           "key":"sample","value":"HELLO"}
    req.update(kw)
    return req


class Gate12Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.crypto = OpenSslMldsa87()
        cls.keytemp = tempfile.TemporaryDirectory(prefix="cai-g12-keys-")
        keyroot = Path(cls.keytemp.name)
        cls.approval_secret, cls.approval_pub = cls.crypto.generate_lab_keypair(keyroot / 'approver')
        cls.evidence_secret, cls.evidence_pub = cls.crypto.generate_lab_keypair(keyroot / 'evidence')
        cls.approval_keyid = cls.crypto.key_id(cls.approval_pub)

    @classmethod
    def tearDownClass(cls):
        cls.keytemp.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cai-g12-effect-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.auth = LabAuthority("tenant1", "operator", CONTEXT, POLICY)
        signer = TrustedSigner(self.approval_pub, self.approval_keyid, "reviewer", "tenant1",
                               frozenset({PURPOSE}))
        self.registry = TrustRegistry(self.crypto, [signer])
        self.replay = ReplayLedger()
        self.verifier = ApprovalVerifier(self.crypto, self.registry, self.replay)
        self.journal = LabJournal(self.root)
        self.executor = LocalEffectExecutor(self.root)
        self.observer = EvidenceObserver(self.executor)
        self.evidence = LabEvidenceSigner(self.crypto, self.evidence_secret, self.evidence_pub)
        self.broker = ControlledBroker(self.auth, self.verifier, self.journal, self.executor,
                                       self.observer, self.evidence, lambda: NOW)
        self.req = request()

    def approval(self, req=None, **overrides):
        req = req or self.req
        bind = self.broker.prepare_lab_binding(req)
        p = {"domain":"CAI-GOVERNED-LLM/G10/APPROVAL/V1", "version":"g10-lab-v1",
             "tenant_id":bind["tenant_id"],"audience":bind["audience"],
             "purpose":PURPOSE,"request_id":bind["request_id"],"nonce":bind["nonce"],
             "request_digest":bind["request_digest"],"context_digest":bind["context_digest"],
             "policy_digest":bind["policy_digest"],"issued_at":"2026-10-20T22:59:30Z",
             "expires_at":"2026-10-20T23:02:00Z", "approver_id":"reviewer", "decision":"APPROVE"}
        p.update(overrides)
        return envelope_lab(self.crypto, self.approval_secret, self.approval_pub, p)

    def signed_execute(self, req=None, **kwargs):
        req = req or self.req
        return self.broker.execute(req, [self.approval(req)], **kwargs)

    def test_01_signed_effect_written_and_observed(self):
        output = self.signed_execute()
        self.assertEqual(output['status'], 'SUCCEEDED')
        self.assertTrue(self.evidence.verify(output['receipt']))
        p = self.executor.effects / target_name(self.req)
        self.assertEqual(p.read_bytes(), effect_bytes(self.req))
        self.assertEqual(self.journal.status('tenant1','op-a'), 'SUCCEEDED')
        self.assertEqual(self.observer.observe(self.req)[0], 'MATCH')

    def test_02_no_signature_rejected_no_effect(self):
        self.assertEqual(self.broker.execute(self.req, [])['status'], 'DENIED')
        self.assertFalse((self.executor.effects / target_name(self.req)).exists())

    def test_03_tampered_signature_rejected(self):
        env = self.approval(); env['signature_b64'] = 'AA=='
        self.assertEqual(self.broker.execute(self.req, [env])['status'], 'DENIED')

    def test_04_wrong_approval_purpose_rejected(self):
        env = self.approval(purpose='MCP_TOOL_CALL')
        self.assertEqual(self.broker.execute(self.req, [env])['status'], 'DENIED')

    def test_05_wrong_signature_request_rejected(self):
        env = self.approval()
        altered = request(value='OTHER')
        self.assertEqual(self.broker.execute(altered, [env])['status'], 'DENIED')

    def test_06_duplicate_request_no_second_write(self):
        self.assertEqual(self.signed_execute()['status'], 'SUCCEEDED')
        self.assertEqual(self.signed_execute()['status'], 'DENIED')
        self.assertEqual(self.journal.status('tenant1','op-a'), 'SUCCEEDED')

    def test_07_same_key_different_id_blocked(self):
        self.assertEqual(self.signed_execute()['status'], 'SUCCEEDED')
        new = request(request_id='op-b',nonce='NonceABCDEF12345679')
        self.assertEqual(self.signed_execute(new)['status'], 'DENIED')

    def test_08_same_key_other_tenant_not_authorized(self):
        req = request(tenant_id='tenant2')
        self.assertEqual(self.broker.execute(req,[])['status'],'DENIED')

    def test_09_approval_replay_altered_nonce_rejected(self):
        env = self.approval()
        req = request(nonce='NonceABCDEF12345679')
        self.assertEqual(self.broker.execute(req,[env])['status'],'DENIED')

    def test_10_revoked_key_rejected(self):
        env=self.approval()
        self.registry.revoke(self.approval_keyid)
        self.assertEqual(self.broker.execute(self.req,[env])['status'],'DENIED')

    def test_11_context_changes_before_dispatch_rejected(self):
        env=self.approval()
        self.assertEqual(self.broker.execute(self.req,[env],before_dispatch_lab=lambda:self.auth.change(context=digest({'v':2})))['status'],'DENIED')

    def test_12_policy_changes_before_dispatch_rejected(self):
        env=self.approval()
        self.assertEqual(self.broker.execute(self.req,[env],before_dispatch_lab=lambda:self.auth.change(policy=digest({'v':2})))['status'],'DENIED')

    def test_13_deactivation_before_dispatch_rejected(self):
        env=self.approval()
        self.assertEqual(self.broker.execute(self.req,[env],before_dispatch_lab=lambda:self.auth.change(active=False))['status'],'DENIED')

    def test_14_reconcile_after_write_interruption(self):
        self.assertEqual(self.signed_execute(fault_lab='AFTER_WRITE')['status'],'INDETERMINATE')
        self.assertEqual(self.journal.status('tenant1','op-a'),'INDETERMINATE')
        result=self.broker.reconcile(self.req)
        self.assertEqual(result['status'],'SUCCEEDED')
        self.assertTrue(self.evidence.verify(result['receipt']))

    def test_15_unknown_before_write_never_success(self):
        self.assertEqual(self.signed_execute(fault_lab='BEFORE_WRITE')['status'],'INDETERMINATE')
        self.assertEqual(self.broker.reconcile(self.req)['status'],'INDETERMINATE')

    def test_16_reconcile_without_record_denied(self):
        self.assertEqual(self.broker.reconcile(self.req)['status'],'DENIED')

    def test_17_reconcile_cannot_mutate_request(self):
        self.assertEqual(self.signed_execute(fault_lab='AFTER_WRITE')['status'],'INDETERMINATE')
        self.assertEqual(self.broker.reconcile(request(value='EVIL'))['status'],'DENIED')

    def test_18_executor_ack_without_observation_is_not_success(self):
        original=self.observer.observe
        self.observer.observe=lambda r:('UNKNOWN',None)
        self.assertEqual(self.signed_execute()['status'],'INDETERMINATE')
        self.observer.observe=original
        self.assertEqual(self.broker.reconcile(self.req)['status'],'SUCCEEDED')

    def test_19_corrupt_observation_is_failed(self):
        self.assertEqual(self.signed_execute(fault_lab='AFTER_WRITE')['status'],'INDETERMINATE')
        target=self.executor.effects/target_name(self.req)
        target.write_bytes(b'MALICIOUS')
        self.assertEqual(self.broker.reconcile(self.req)['status'],'FAILED')

    def test_20_missing_observation_is_unknown(self):
        self.assertEqual(self.signed_execute(fault_lab='AFTER_WRITE')['status'],'INDETERMINATE')
        (self.executor.effects/target_name(self.req)).unlink()
        self.assertEqual(self.broker.reconcile(self.req)['status'],'INDETERMINATE')

    def test_21_signed_receipt_tampering_rejected(self):
        result=self.signed_execute()
        for field in ('observed_digest','request_id','journal_head'):
            copy_env=copy.deepcopy(result['receipt']); copy_env['payload'][field]='TAMPER'
            self.assertFalse(self.evidence.verify(copy_env))

    def test_22_receipt_wrong_signer_key_rejected(self):
        result=self.signed_execute()
        result['receipt']['key_id']='spki-sha256:'+'0'*64
        self.assertFalse(self.evidence.verify(result['receipt']))

    def test_23_corrupted_journal_chain_detected(self):
        self.assertEqual(self.signed_execute()['status'],'SUCCEEDED')
        with closing(sqlite3.connect(self.journal.db)) as con, con:
            con.execute("UPDATE events SET event_hash=? WHERE seq=1",('deadbeef',))
        with self.assertRaises(Exception):
            self.journal.check_chain()

    def test_24_corrupted_journal_blocks_new_execution(self):
        self.assertEqual(self.signed_execute()['status'],'SUCCEEDED')
        with closing(sqlite3.connect(self.journal.db)) as con, con:
            con.execute("UPDATE events SET status=? WHERE seq=1",('FAKE',))
        later=request(request_id='op-b',nonce='NonceABCDEF12345679', key='other')
        self.assertEqual(self.signed_execute(later)['status'],'DENIED')

    def test_25_symlink_at_target_does_not_follow(self):
        target=self.executor.effects/target_name(self.req)
        other=self.root/'other.secret'; other.write_text('ORIGINAL')
        try:
            target.symlink_to(other)
        except (OSError, NotImplementedError):
            # Windows may not permit test symlinks without elevation.
            # O_EXCL must still protect preexisting files.
            target.write_text('PREEXISTING')
        response=self.signed_execute()
        self.assertEqual(response['status'],'INDETERMINATE')
        self.assertEqual(other.read_text(),'ORIGINAL')

    def test_26_concurrent_identical_request_single_effect(self):
        env1=self.approval(); env2=copy.deepcopy(env1)
        results=[]; lock=threading.Lock()
        def worker(env):
            answer=self.broker.execute(self.req,[env])['status']
            with lock: results.append(answer)
        t1=threading.Thread(target=worker,args=(env1,)); t2=threading.Thread(target=worker,args=(env2,))
        t1.start();t2.start();t1.join();t2.join()
        self.assertEqual(sorted(results),['DENIED','SUCCEEDED'])

    def test_27_receipt_cannot_claim_unobserved_success(self):
        self.assertEqual(self.signed_execute(fault_lab='BEFORE_WRITE')['status'],'INDETERMINATE')
        self.assertIsNone(self.broker.reconcile(self.req)['receipt'])

    def test_28_prepared_cannot_mark_succeeded(self):
        self.journal.reserve(self.req)
        from cai_g10.pqc import Denied
        with self.assertRaises(Denied): self.journal.transition(self.req,'SUCCEEDED')

    def test_29_succeeded_is_terminal(self):
        self.assertEqual(self.signed_execute()['status'],'SUCCEEDED')
        from cai_g10.pqc import Denied
        with self.assertRaises(Denied): self.journal.transition(self.req,'DISPATCHED')

    def test_30_two_distinct_keys_possible(self):
        self.assertEqual(self.signed_execute()['status'],'SUCCEEDED')
        other=request(request_id='op-b',nonce='NonceABCDEF12345679',key='other')
        self.assertEqual(self.signed_execute(other)['status'],'SUCCEEDED')
        self.assertEqual(len(tuple(self.executor.effects.glob('*.effect'))),2)

    def test_31_wrong_evidence_signature_is_rejected(self):
        result=self.signed_execute()
        result['receipt']['signature_b64']=base64.b64encode(b'X'*4627).decode('ascii')
        self.assertFalse(self.evidence.verify(result['receipt']))

    def test_32_reconcile_no_duplicate_effect(self):
        self.assertEqual(self.signed_execute(fault_lab='AFTER_WRITE')['status'],'INDETERMINATE')
        self.assertEqual(self.broker.reconcile(self.req)['status'],'SUCCEEDED')
        self.assertEqual(self.broker.reconcile(self.req)['status'],'DENIED')
        self.assertEqual(len(tuple(self.executor.effects.glob('*.effect'))),1)

    def test_33_policy_epoch_after_approval_denied_even_same_digest(self):
        env=self.approval()
        self.assertEqual(self.broker.execute(self.req,[env],before_dispatch_lab=lambda:self.auth.change())['status'],'DENIED')

    def test_34_refuses_unknown_fault(self):
        self.assertEqual(self.broker.execute(self.req,[self.approval()],fault_lab='FAKE')['status'],'DENIED')

    def test_35_effect_bytes_bind_to_full_intent(self):
        old=effect_bytes(self.req)
        self.assertNotEqual(old,effect_bytes(request(request_id='other')))
        self.assertNotEqual(old,effect_bytes(request(value='OTHER')))

    def test_36_conflicting_preexisting_file_indeterminate(self):
        (self.executor.effects/target_name(self.req)).write_text('UNTRUSTED')
        result=self.signed_execute()
        self.assertEqual(result['status'],'INDETERMINATE')
        self.assertEqual(self.broker.reconcile(self.req)['status'],'FAILED')

    def test_37_journal_chain_repeatable(self):
        self.assertEqual(self.journal.check_chain(),'0'*64)
        self.assertEqual(self.signed_execute()['status'],'SUCCEEDED')
        self.assertEqual(self.journal.check_chain(),self.signed_execute.__self__.journal.check_chain())

    def test_38_reconcile_does_not_dispatch_after_unknown(self):
        self.assertEqual(self.signed_execute(fault_lab='BEFORE_WRITE')['status'],'INDETERMINATE')
        for _ in range(3): self.assertEqual(self.broker.reconcile(self.req)['status'],'INDETERMINATE')
        self.assertFalse((self.executor.effects/target_name(self.req)).exists())

    def test_39_no_execution_on_invalid_wire(self):
        self.assertEqual(self.broker.execute(None,[])['status'],'DENIED')
        self.assertFalse(tuple(self.executor.effects.glob('*.effect')))

    def test_40_empty_signer_list_rejected(self):
        self.assertEqual(self.broker.execute(self.req,[])['status'],'DENIED')

    def test_41_evidence_receipt_domain_replay_defended(self):
        receipt=self.signed_execute()['receipt']
        receipt['payload']['domain']='CAI-G10-APPROVAL'
        self.assertFalse(self.evidence.verify(receipt))

    def test_43_restart_recovery_after_dispatch_and_effect(self):
        self.journal.reserve(self.req)
        self.journal.transition(self.req,'DISPATCHED')
        self.executor.apply(self.req)
        restarted = LabJournal(self.root)
        other = ControlledBroker(self.auth,self.verifier,restarted,self.executor,
                                 self.observer,self.evidence,lambda:NOW)
        answer=other.reconcile(self.req)
        self.assertEqual(answer['status'],'SUCCEEDED')
        self.assertTrue(self.evidence.verify(answer['receipt']))
        self.assertEqual(restarted.status('tenant1','op-a'),'SUCCEEDED')

    def test_44_restart_recovery_unknown_effect_never_auto_retries(self):
        self.journal.reserve(self.req)
        self.journal.transition(self.req,'DISPATCHED')
        restarted = LabJournal(self.root)
        other = ControlledBroker(self.auth,self.verifier,restarted,self.executor,
                                 self.observer,self.evidence,lambda:NOW)
        answer=other.reconcile(self.req)
        self.assertEqual(answer['status'],'INDETERMINATE')
        self.assertFalse(tuple(self.executor.effects.glob('*.effect')))
        self.assertEqual(restarted.status('tenant1','op-a'),'INDETERMINATE')

    def test_45_restart_prepared_does_not_promote_forged_effect(self):
        self.journal.reserve(self.req)
        (self.executor.effects/target_name(self.req)).write_bytes(effect_bytes(self.req))
        other = ControlledBroker(self.auth,self.verifier,LabJournal(self.root),self.executor,
                                 self.observer,self.evidence,lambda:NOW)
        answer=other.reconcile(self.req)
        self.assertEqual(answer['status'],'INDETERMINATE')
        self.assertIsNone(answer['receipt'])

    def test_46_signature_service_failure_cannot_commit_success(self):
        from cai_g10.pqc import Hold
        original=self.evidence.sign
        def broken(payload):
            raise Hold('SIMULATED_EVIDENCE_SIGNER_DOWN')
        self.evidence.sign=broken
        try:
            response=self.signed_execute()
            self.assertEqual(response['status'],'INDETERMINATE')
            self.assertIsNone(response['receipt'])
            self.assertEqual(self.journal.status('tenant1','op-a'),'INDETERMINATE')
        finally:
            self.evidence.sign=original
        recovered=self.broker.reconcile(self.req)
        self.assertEqual(recovered['status'],'SUCCEEDED')
        self.assertTrue(self.evidence.verify(recovered['receipt']))

    def test_42_journal_mutation_not_authentic_audit(self):
        self.assertEqual(self.signed_execute()['status'],'SUCCEEDED')
        # This test only shows *detection* of uncoordinated mutation; a local admin can recompute chain.
        with closing(sqlite3.connect(self.journal.db)) as con, con:
            con.execute("UPDATE events SET observed_digest=? WHERE seq=(SELECT MAX(seq) FROM events)",('sha256:'+'f'*64,))
        with self.assertRaises(Exception): self.journal.check_chain()


BAD_FIELDS = {
    'bad_domain': {'domain':'unknown'}, 'wrong_operation':{'operation':'DELETE'},
    'unsafe_path':{'key':'../etc'}, 'windows_path':{'key':'c\\windows'},
    'long_value':{'value':'A'*513},'empty_value':{'value':''},
    'bad_nonce':{'nonce':'short'}, 'bad_context':{'context_digest':'fake'},
    'bad_policy':{'policy_digest':'sha256:xyz'},
    'float_value':{'value':1.0},'boolean_value':{'value':True},
    'bad_id':{'request_id':'not good'},'bad_tenant':{'tenant_id':'tenant/evil'},
    'wrong_audience':{'audience':'external.prod'}, 'bad_requester':{'requester_id':'Operator'},
    'unexpected_field':{'unexpected':'bad'}, 'list_context':{'context_digest':[]},
}
for label, changes in BAD_FIELDS.items():
    def make_case(update):
        def test(self):
            r=request(**update)
            self.assertEqual(self.broker.execute(r,[])['status'],'DENIED')
        return test
    setattr(Gate12Tests,'test_bad_wire_'+label,make_case(changes))
