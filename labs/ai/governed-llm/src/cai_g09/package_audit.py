"""Offline checks: G08 source-byte lineage and test-to-coverage IDs, no file modifications."""
from __future__ import annotations

import ast
import csv
import hashlib
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[2]
G08 = {
    "src/cai_g08/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "src/cai_g08/contracts.py": "8172ee6c5c410624b68c73e39f2767a95b0e536cef764b53e98b02758664a0b3",
    "src/cai_g08/engine.py": "3cecea0dfc9360c7bf23cb94b18ca16a66779b9ca4d0efe02a4ed64a69408a3d",
    "src/cai_g08/evidence.py": "243a122725a25f4b29f0aa3a494e1d58d6ff6fd3ce545b83217f94c56ee1a321",
    "tests/test_gate08.py": "12de90e6ef55ae7ef5d4f7a1d6ad536e46471ef1d3d4874f5777ab9caee54c8a",
}


def main() -> int:
    failures = []
    for relative, expected in G08.items():
        path = BASE / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            failures.append("G08_SOURCE_LINEAGE: " + relative)
    tests = {}
    for path in (BASE / "tests").glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found = {node.name for cls in tree.body if isinstance(cls, ast.ClassDef)
                 for node in cls.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")}
        tests[path.name] = found
    with (BASE / "verification" / "G09-TEST-COVERAGE.csv").open(newline="", encoding="utf-8") as fd:
        rows = list(csv.DictReader(fd))
    declared = [(row["SourceFile"], row["TestMethod"]) for row in rows]
    if len(rows) != 112 or len(set(declared)) != 112:
        failures.append("COVERAGE_ROWS_NOT_112_OR_DUPLICATE")
    if len({row["TestID"] for row in rows}) != 112:
        failures.append("TEST_ID_NOT_UNIQUE")
    for source, method in declared:
        if method not in tests.get(source, set()):
            failures.append("ORPHAN_COVERAGE: " + source + ":" + method)
    for source, found in tests.items():
        for method in found:
            if (source, method) not in declared:
                failures.append("UNMAPPED_TEST: " + source + ":" + method)
    if failures:
        for issue in failures:
            print("[FAIL] " + issue)
        return 2
    print("[PASS] G08 SOURCE LINEAGE - 5/5 exact SHA256 unchanged")
    print("[PASS] TEST TRACEABILITY - 112/112 mapped; unique; no orphan tests")
    print("[HOLD] Assurance remains LAB ONLY; no real identity provider, CAI CORE, PQC or independent human review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
