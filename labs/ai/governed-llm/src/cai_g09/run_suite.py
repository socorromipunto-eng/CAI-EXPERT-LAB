"""Offline lab test runner; reports actual counts; never writes files or calls network."""
from __future__ import annotations

import json
import os
import sys
import unittest


MIN_EXPECTED = 112


def main() -> int:
    suite = unittest.defaultTestLoader.discover(start_dir="tests", pattern="test_*.py")
    discovered = suite.countTestCases()
    if discovered != MIN_EXPECTED:
        print("[FAIL] DISCOVERY_COUNT expected=%d got=%d" % (MIN_EXPECTED, discovered))
        return 2
    print("[INFO] GATE09 test discovery=%d; G08 regression=54; G09 new=58" % discovered)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    summary = {
        "gate": "G09", "environment": "runtime_local", "status": "PASS" if result.wasSuccessful() and result.testsRun == MIN_EXPECTED and not result.skipped else "FAIL",
        "tests_run": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skipped": len(result.skipped),
        "external_effects_tested": False,
        "real_authentication_tested": False, "real_cryptographic_signatures_tested": False,
        "real_cai_core_semantics_tested": False,
        "source_policy": "fixture_only", "release_authorized": False,
    }
    print("G09_ACTUAL_RUNTIME_RESULT=" + json.dumps(summary, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
