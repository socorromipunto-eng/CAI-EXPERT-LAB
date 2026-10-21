# G12-WIN-001 — SQLite connection lifetime in Windows tests

Status: PROPOSED PORTABILITY REMEDIATION / WINDOWS RETEST REQUIRED
Version: G12 v0.3.4.1, 2026-10-21
Baseline: G12 v0.3.4 (original ZIP SHA256 174559369DC3A7FE2736E345821B23A1450527D498B995B6C375AA891089E36F)

## Reported symptom
Windows-11-10.0.26300-SP0 runner executed 324 tests in 56.246 seconds, reported errors=3, failures=0. Error tracebacks were not available. Builder Linux run completed 324/324.

## Evidence-based hypothesis
There are exactly three `with sqlite3.connect(self.journal.db) as con:` statements in `tests/test_gate12.py` in tests 23, 24 and 42. `sqlite3.Connection.__exit__` handles transaction commit/rollback, not connection closure. When connection references remain live, Windows file handle sharing can prevent TemporaryDirectory.cleanup from deleting the SQLite file. This is a plausible explanation for the three errors but is not proven without original tracebacks.

## Exact changes
- Import `closing` from `contextlib`.
- For the three test connections, replace `with sqlite3.connect(...) as con:` with `with closing(sqlite3.connect(...)) as con, con:`. Context exit now commits/rolls back and then *closes* the connection, even if assertions raise.
- README updated with incident context.
- This document added, and SHA256SUMS.txt rebuilt.
- No changes to production-like reference code in `src/`, no change to G08-G11 tests, no changes to case IDs, no new dependencies, no network, no repository mutations.

## Evidence required to close
1. ZIP SHA-256 matches the separately furnished hash.
2. Manifest validates all file digests and no extra files.
3. Same 324 tests execute with errors=0, failures=0 on user's Windows.
4. Preservation of G08-G11 source/test lineage passes runner.
5. If failures remain, capture full unittest `ERROR` + `Traceback` blocks and classify them; do not claim closed.

## Remaining assurance limitations
Lab-only; ephemeral test keys; SQLite and local file observer not independent IV&V; canonical CORE binding, OS isolation, distributed fencing, production IdP/KMS/HSM and release remain HOLD.
