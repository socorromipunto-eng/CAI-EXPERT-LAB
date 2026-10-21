"""GATE13 offline adversarial suite runner; actual observed test result, no simulation."""
from __future__ import annotations
import csv
import hashlib
import json
import platform
import sys
import unittest
from pathlib import Path
from cai_g10.pqc import Hold, OpenSslMldsa87

ROOT = Path(__file__).resolve().parents[2]
INHERITED = 324
NEW = 89
EXPECTED = INHERITED + NEW
CONTROLS = {f'ADV-{i:03d}' for i in range(1,11)}


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite): yield from flatten(item)
        else: yield item


def main() -> int:
    if sys.version_info < (3,10):
        print('[HOLD] Python 3.10+ required');return 3
    try:
        provider=OpenSslMldsa87()
    except Hold as ex:
        print('[HOLD] OpenSSL ML-DSA-87 provider unavailable:',str(ex));return 3
    print('[PASS] REAL ML-DSA-87 PROVIDER - '+provider.version)
    with (ROOT/'verification'/'G12-INHERITED-SOURCE-AND-TEST-SHA256.txt').open(encoding='utf-8') as stream:
        rows=[x.strip().split('|',1) for x in stream if x.strip()]
    if not rows or any(len(row)!=2 or
                       not (ROOT/row[1]).is_file() or
                       hashlib.sha256((ROOT/row[1]).read_bytes()).hexdigest()!=row[0]
                       for row in rows):
        print('[FAIL] G12 INHERITED SOURCE/TEST LINEAGE');return 1
    print(f'[PASS] G12 SOURCE/TEST LINEAGE - {len(rows)}/{len(rows)} exact SHA256')
    suite = unittest.defaultTestLoader.discover(str(ROOT/'tests'), pattern='test_gate*.py',top_level_dir=str(ROOT/'tests'))
    tests=[t.id() for t in flatten(suite)]
    newer={x for x in tests if x.startswith('test_gate13.')}
    legacy={x for x in tests if not x.startswith('test_gate13.')}
    with (ROOT/'verification'/'G13-TEST-TRACEABILITY.csv').open(encoding='utf-8',newline='') as stream:
        trace=list(csv.DictReader(stream))
    trace_ids=[x['test_id'] for x in trace]
    correct=(len(tests)==EXPECTED and len(set(tests))==EXPECTED and
             len(newer)==NEW and len(legacy)==INHERITED and
             len(trace)==NEW and len(set(trace_ids))==NEW and set(trace_ids)==newer and
             {x['control_id'] for x in trace}==CONTROLS and
             all(x['control_id'] in CONTROLS and x['expected_status']=='LAB_TEST' for x in trace))
    if not correct:
        print(f'[FAIL] TRACEABILITY: discovered={len(tests)}, inherited={len(legacy)}, new={len(newer)}, trace={len(trace)}')
        return 1
    print(f'[PASS] TRACEABILITY - {INHERITED} inherited + {NEW} new = {EXPECTED} tests; 0 orphan')
    result=unittest.TextTestRunner(stream=sys.stdout,verbosity=1).run(suite)
    passed=result.wasSuccessful() and result.testsRun==EXPECTED and not result.skipped
    report={
        'gate':'G13','version':'v0.3.5','environment':platform.platform(),
        'mode':'OFFLINE_CLOSED_WORLD_ADVERSARIAL_INTEGRATION_LAB',
        'result':'PASS' if passed else 'FAIL','provider':provider.version,
        'expected':EXPECTED,'tests_run':result.testsRun,'inherited_g08_to_g12':INHERITED,
        'new_g13_tests':NEW,'failures':len(result.failures),'errors':len(result.errors),
        'skipped':len(result.skipped),
        'real_mldsa87_signature_verification':True,
        'dual_domain_approval_lab_tested':True,
        'untrusted_fixture_data_does_not_become_a_tool_command_tested':True,
        'receipt_and_journal_local_cross_checks_tested':True,
        'mock_socket_network_attempts_blocked_during_one_test':True,
        'real_llm_prompt_injection_resilience_tested':False,
        'external_mcp_transport_tested':False,'actual_network_firewall_tested':False,
        'os_process_container_isolation_tested':False,
        'enterprise_idp_kms_hsm_tested':False,'distributed_fencing_tested':False,
        'canonical_cai_core_adapter_tested':False,'independent_human_ivv':False,
        'repository_mutated':False,'production_authorized':False,
    }
    print('G13_ACTUAL_RUNTIME_RESULT='+json.dumps(report,sort_keys=True))
    print('[PASS] GATE13 OFFLINE ADVERSARIAL INTEGRATION LAB' if passed else '[FAIL] GATE13 LAB')
    print('[HOLD] Real LLM injection defense, external MCP, process/OS isolation, firewall, real IdP/KMS, CORE adapter, IV&V, release')
    return 0 if passed else 1


if __name__=='__main__':
    sys.exit(main())
