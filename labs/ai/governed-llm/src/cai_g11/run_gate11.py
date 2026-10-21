"""GATE11 offline runner: mandatory source/test inventory, no persistent writes."""
from __future__ import annotations

import csv
import json
import platform
import sys
import unittest
from pathlib import Path

from cai_g10.pqc import Hold, OpenSslMldsa87

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = 261
INHERITED = 169
NEW = 92


def iter_tests(suite):
    for entry in suite:
        if isinstance(entry, unittest.TestSuite):
            yield from iter_tests(entry)
        else:
            yield entry


def main() -> int:
    if sys.version_info < (3, 10):
        print('[HOLD] Python 3.10+ required')
        return 3
    try:
        provider = OpenSslMldsa87()
    except Hold as exc:
        print('[HOLD] ML-DSA-87 provider unavailable; no fallback: ' + str(exc))
        return 3
    print('[PASS] REAL ML-DSA-87 PROVIDER - ' + provider.version)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern='test_gate*.py',
                                                top_level_dir=str(ROOT / 'tests'))
    all_ids = [test.id() for test in iter_tests(suite)]
    g11_ids = {ref for ref in all_ids if ref.startswith('test_gate11.')}
    inherited_ids = {ref for ref in all_ids if not ref.startswith('test_gate11.')}
    trace_file = ROOT / 'verification' / 'G11-TEST-TRACEABILITY.csv'
    with trace_file.open(newline='', encoding='utf-8') as source:
        rows = list(csv.DictReader(source))
    csv_ids = [r['test_id'] for r in rows]
    control_ids = {'MCP-001','MCP-002','MCP-003','MCP-004',
                   'MCP-005','MCP-006','MCP-007','MCP-008'}
    valid = (len(all_ids) == EXPECTED and len(set(all_ids)) == EXPECTED and
             len(g11_ids) == NEW and len(inherited_ids) == INHERITED and
             len(csv_ids) == NEW and len(set(csv_ids)) == NEW and
             set(csv_ids) == g11_ids and all(r['control_id'] in control_ids for r in rows) and
             {r['control_id'] for r in rows} == control_ids and
             all(r['expected_status'] == 'LAB_TEST' for r in rows))
    if not valid:
        print('[FAIL] TRACEABILITY / TEST INVENTORY MISMATCH')
        return 1
    print('[PASS] TEST INVENTORY - 169 inherited + 92 new = 261; traceability exact')
    result = unittest.TextTestRunner(verbosity=1, stream=sys.stdout).run(suite)
    passed = result.wasSuccessful() and result.testsRun == EXPECTED and not result.skipped
    report = {
        'gate': 'G11', 'mode': 'OFFLINE_LAB', 'result': 'PASS' if passed else 'FAIL',
        'environment': platform.platform(), 'provider': provider.version,
        'tests_run': result.testsRun, 'expected': EXPECTED,
        'inherited_g08_g09_g10_tests': INHERITED, 'new_g11_tests': NEW,
        'failures': len(result.failures), 'errors': len(result.errors),
        'skipped': len(result.skipped),
        'actual_mldsa87_signature_verification': True,
        'fixture_only_tools_call_emulation': True,
        'external_mcp_server_tested': False,
        'external_execution_tested': False,
        'os_container_isolation_tested': False,
        'network_egress_firewall_tested': False,
        'llm_prompt_injection_resilience_tested': False,
        'production_idp_kms_hsm_tested': False,
        'canonical_cai_core_tested': False,
        'independent_human_ivv': False,
        'production_authorized': False,
    }
    print('G11_ACTUAL_RUNTIME_RESULT=' + json.dumps(report, sort_keys=True))
    print('[PASS] GATE11 OFFLINE MCP LAB' if passed else '[FAIL] GATE11 OFFLINE LAB')
    print('[HOLD] OS isolation, external MCP, real IdP/KMS, canonical CORE, human IV&V, release')
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
