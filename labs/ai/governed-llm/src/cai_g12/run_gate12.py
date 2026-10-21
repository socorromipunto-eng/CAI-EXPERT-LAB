"""GATE12 preflight/test runner: package inventory, crypto, exact test lineage."""
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
G08_TO_G11 = 261
G12_NEW = 63
TOTAL = G08_TO_G11 + G12_NEW


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def main() -> int:
    if sys.version_info < (3,10):
        print('[HOLD] Python 3.10+ unavailable'); return 3
    try:
        provider = OpenSslMldsa87()
    except Hold as exc:
        print('[HOLD] Missing ML-DSA-87 provider: ' + str(exc)); return 3
    print('[PASS] ML-DSA-87 PROVIDER - ' + provider.version)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'),pattern='test_gate*.py',top_level_dir=str(ROOT / 'tests'))
    names = [t.id() for t in flatten(suite)]
    inherited = {n for n in names if not n.startswith('test_gate12.')}
    new = {n for n in names if n.startswith('test_gate12.')}
    with (ROOT/'verification'/'G12-TEST-TRACEABILITY.csv').open(encoding='utf-8',newline='') as inp:
        refs = list(csv.DictReader(inp))
    test_refs = [r['test_id'] for r in refs]
    controls = {'EXEC-001','EXEC-002','EXEC-003','EXEC-004','EXEC-005','EXEC-006','EXEC-007','EXEC-008'}
    checks = len(names) == TOTAL and len(set(names)) == TOTAL and len(inherited) == G08_TO_G11 and len(new) == G12_NEW
    checks = checks and len(test_refs) == G12_NEW and len(set(test_refs)) == G12_NEW and set(test_refs) == new
    checks = checks and all(r['control_id'] in controls and r['expected_status']=='LAB_TEST' for r in refs)
    checks = checks and {r['control_id'] for r in refs} == controls
    if not checks:
        print('[FAIL] Test inventory/traceability mismatch'); return 1
    print(f'[PASS] TRACEABILITY - {len(inherited)} inherited + {len(new)} G12 = {len(names)} total, 0 orphans')
    result = unittest.TextTestRunner(stream=sys.stdout,verbosity=1).run(suite)
    passed = result.wasSuccessful() and result.testsRun == TOTAL and not result.skipped
    report = {
        'gate':'G12','mode':'OFFLINE_TEMPORARY_FILESYSTEM_LAB',
        'result':'PASS' if passed else 'FAIL','environment':platform.platform(),
        'provider':provider.version,'expected':TOTAL,'tests_run':result.testsRun,
        'inherited_g08_to_g11':G08_TO_G11,'new_g12_tests':G12_NEW,
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'local_filesystem_fixture_effects_tested':True,
        'separate_observer_code_path_tested':True,
        'ml_dsa_87_real_signature_tested':True,
        'sqlite_local_journal_tested':True,
        'distributed_transaction_tested':False,'process_or_container_isolation_tested':False,
        'remote_or_external_system_effects_tested':False,'external_mcp_tested':False,
        'canonical_core_tested':False,'independent_ivv_done':False,
        'trusted_timestamp_hsm_kms_tested':False,'production_authorized':False,
    }
    print('G12_ACTUAL_RUNTIME_RESULT=' + json.dumps(report,sort_keys=True))
    print('[PASS] GATE12 LOCAL EFFECT/EVIDENCE LAB' if passed else '[FAIL] GATE12 LOCAL LAB')
    print('[HOLD] Real OS isolation/remote execution, durable trusted audit, persistent distributed fencing, HSM/KMS, CORE adapter and independent IV&V')
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
