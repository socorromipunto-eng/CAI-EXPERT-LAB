"""Offline G10 executable test runner; does not write persistent evidence files."""
from __future__ import annotations
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import unittest

from cai_g10.pqc import Hold, OpenSslMldsa87

ROOT = Path(__file__).resolve().parents[2]
TEST_COUNT = 169
G09_COUNT = 112
G10_COUNT = 57


def main() -> int:
    if sys.version_info < (3, 10):
        print('[HOLD] Python 3.10+ required')
        return 3
    try:
        provider = OpenSslMldsa87()
    except Hold as exc:
        print(f'[HOLD] REAL ML-DSA-87 PROVIDER - {exc}; no fallback, no installs')
        return 3
    print('[PASS] REAL ML-DSA-87 PROVIDER - ' + provider.version)
    tests_path = ROOT / 'tests'
    discovered = 0
    for f in sorted(tests_path.glob('test_gate*.py')):
        tree = ast.parse(f.read_text(encoding='utf-8'))
        discovered += sum(1 for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith('test_'))
    if discovered != TEST_COUNT:
        print(f'[FAIL] TEST INVENTORY {discovered}; expected {TEST_COUNT}')
        return 1
    print(f'[PASS] TEST INVENTORY - {discovered}/{TEST_COUNT}; 112 G08+G09 and 57 G10')
    suite = unittest.defaultTestLoader.discover(str(tests_path), pattern='test_gate*.py', top_level_dir=str(tests_path))
    result = unittest.TextTestRunner(verbosity=1, stream=sys.stdout).run(suite)
    ok = result.wasSuccessful() and result.testsRun == TEST_COUNT and len(result.skipped) == 0
    rec = {
        'gate': 'G10', 'result': 'PASS' if ok else 'FAIL', 'mode': 'OFFLINE_LAB',
        'actual_runtime_environment': platform.platform(), 'openssl_provider': provider.version,
        'total_run': result.testsRun, 'expected': TEST_COUNT,
        'gate08_and_gate09_regression': G09_COUNT, 'gate10_real_crypto_tests': G10_COUNT,
        'errors': len(result.errors), 'failures': len(result.failures), 'skipped': len(result.skipped),
        'real_mldsa87_sign_verify': True,
        'keys_ephemeral_local_unencrypted': True,
        'hsm_kms_tested': False, 'real_idp_tested': False, 'mfa_tested': False,
        'mcp_isolation_tested': False, 'distributed_replay_store_tested': False,
        'canonical_cai_core_adapter_tested': False,
        'independent_ivv_completed': False, 'production_authorized': False,
    }
    print('G10_ACTUAL_RUNTIME_RESULT=' + json.dumps(rec, sort_keys=True))
    print('[PASS] GATE10 OFFLINE PQC LAB' if ok else '[FAIL] GATE10 LOCAL TESTS')
    print('[HOLD] KMS/HSM, real IdP/MFA, persistent distributed replay, canonical CORE, independent human IV&V, release')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
