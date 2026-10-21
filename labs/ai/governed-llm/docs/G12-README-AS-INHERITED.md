# CAI-GOVERNED-LLM GATE 12 — v0.3.4 (LOCAL EXECUTION + EVIDENCE LAB)

**Owner:** Antonio José Socorro Marín. **AI assistance:** design, prototype and testing. **Status:** OFFLINE LOCAL-FIXTURE LAB; NO ENTERPRISE APPROVAL.

Inherits GATE 08/09/10/11 unchanged source/test files. G12 adds a **real local temporary filesystem fixture effect**, separately re-opened observation, signed approval (OpenSSL ML-DSA-87), SQLite local reservation/journal with transition hash chain, signed lab-success evidence receipts, crash recovery without automatic re-execution, and 63 additional adversarial and functional tests.

**These are local temporary-file effects, not external-system actions.** There is no MCP server, network service, real identity provider, trusted KMS/HSM, process isolation, canonical CORE decision logic, independent IV&V, production write, commit or push.

## Contents

- `src/cai_g12/execution.py`: implemented closed-world local effect broker, journal, observer, receipts.
- `tests/test_gate12.py`: 63 new tests plus inherited G08-11 tests (261 unchanged).
- `src/cai_g12/run_gate12.py`: test inventory + machine-readable observed results.
- `RUN-GATE12-ISOLATED-v1.0.0.ps1`: Windows PowerShell 5.1 runner. Validates full ZIP extraction manifest, G11 source/test hashes, Python and OpenSSL; runs entire suite in isolated OS temp directories.
- `verification/G12-TEST-TRACEABILITY.csv`: all 63 G12 test methods mapped to 8 controls.
- `verification/G11-INHERITED-SOURCE-AND-TEST-SHA256.txt`: inherited files exact hashes.
- `verification/G12-BUILDER-RUN.txt`: evidence of actual builder run, not Windows.
- `contracts/G12-request-schema-proposal.json`: illustrative schema; Python enforces additional NFC restrictions.
- `docs/`: technical limits, fault model, governance, decision, and Git checkpoint plan.
- `SHA256SUMS.txt`: all files except itself, verified by runner.

## Usage

Verify the downloaded ZIP hash from the accompanying response **before extraction**. Extract only outside `C:\CAI-EXPERT-LAB`. Execute the PowerShell runner provided in the accompanying message. Python 3.10+ and OpenSSL 3.5+ with ML-DSA-87 must already be installed; no automatic installs/downloads.

`PASS` means only reproducible isolated local fixture tests. `HOLD` means unavailable required provider or unreviewed enterprise conditions. Do not include simulated, ephemeral private keys or temp files in Git or disclose them.

The ZIP is **not a software release or independent certification**. No license is granted to third parties beyond authoritative `/legal` documents.


## G12.1 Windows SQLite handle correction (2026-10-21)

This v0.3.4.1 patch changes only three SQLite connection context statements in `tests/test_gate12.py` by wrapping the connection with `contextlib.closing`. The prior `with sqlite3.connect(...)` commits/rolls back the transaction but does not guarantee connection closure; Windows prevents cleanup of files with still-open SQLite handles. All 261 inherited tests and the G12 runtime source remain byte-for-byte unchanged. The three observed Windows errors require traceback confirmation; this is a targeted portability hypothesis, NOT an assertion of verified root cause. No production, HSM/KMS, CORE integration, release or independent IV&V authorization is implied.
