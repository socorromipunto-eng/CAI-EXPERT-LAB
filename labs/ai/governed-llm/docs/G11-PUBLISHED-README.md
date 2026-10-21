# CAI-GOVERNED-LLM GATE 11 — v0.3.3 MCP Security Gateway (OFFLINE LAB)

**Status:** BUILDER OFFLINE LAB PASS; OWNER WINDOWS EXECUTION PENDING; ENTERPRISE ASSURANCE HOLD.  
**Owner and decision authority:** Antonio José Socorro Marín.  
**AI assistance:** source code, drafting, and first-party verification assistance; NOT independent IV&V.  
**Provenance:** immutable GATE 08/09/10 source+test files inherited from the GATE 10 ZIP, checked byte-for-byte with SHA-256.  
**Rights:** preserve the existing `/legal` documents of CAI-EXPERT-LAB, with all rights reserved; nothing here grants third-party redistribution rights.

## What is actually executable

A closed-world, offline, deliberately narrow **MCP-style JSON-RPC `tools/call` laboratory emulator**, **NOT** a complete MCP server. It implements one `cai.fixture.read` capability over immutable-style, in-memory test records; no adapters exist for network, shell, filesystem or real tools. The gateway:

1. Strictly validates bounded JSON-RPC 2.0 `tools/call` messages: rejects duplicate keys, unsafe extra fields, unsupported methods/tools, noncanonical Unicode, oversized inputs and unsafe resource names.
2. Accepts only server-provisioned **fixture** sessions, tools and tenant-scoped resource catalogs; rejects absent/expired/revoked (fixture) authority and cross-tenant resource access. No genuine IdP, session token verification or MFA.
3. Requires a **real OpenSSL ML-DSA-87 signature**, checked using the unchanged GATE 10 verifier and laboratory trust anchors. The signed digest covers exact request JSON, caller, tenant, context/policy, tool, resource classification and resource-content digest.
4. Enforces classification-based read-only output release, output bounds, non-elevation of tool-output text to instructions, redacted generic public denial, and in-memory metadata-only audit entries.
5. Atomically consumes nonce values via the inherited **local-memory** replay ledger and rechecks in-memory authority/resource epoch before releasing fixture data.
6. Regresses all **169 GATE 08–10 tests** and adds **92 GATE 11** positive, negative, authorization, concurrency, revocation and data-trust tests. Test names are mapped 1:1 to controls in `verification/G11-TEST-TRACEABILITY.csv`.

### Security limitations: MUST NOT be represented as production safeguards

- **No OS/container boundary.** A Python fixture allowlist is NOT process isolation; arbitrary untrusted code running inside this process could bypass it. The test harness can deliberately mutate laboratory authority.
- **No external MCP transport, real LLM, prompt-injection model robustness evaluation, network egress enforcement, DNS/SSRF sandbox, filesystem mediation or effectful execution.** Malicious-looking strings are preserved as untrusted *data*; they are not analyzed by an LLM.
- **No authentic identity federation/MFA, trusted production key enrollment, HSM/KMS, key persistence, distributed replay, durable audit ledger, time authority, cross-node fencing or external execution receipts.** Keys are created as ephemeral, unencrypted lab PEM files, removed by temporary-directory cleanup; forensic data remnants possible.
- **No canonical CAI CORE adapter.** DSA, ESA, `D(t)` and context-drift semantics are NOT asserted to be implemented or independently validated. Production tool functionality and release remain unauthorized.
- JSON Schema documentation is informative and is not validated by a third-party schema engine; strict wire constraints are executed by Python. Not general MCP specification conformance.

## Files

- `src/cai_g11/gateway.py`: signed, narrow gateway and in-memory trust/fixture authority.
- `src/cai_g11/run_gate11.py`: machine-readable test runner, source coverage gate.
- `tests/test_gate11.py`: 92 executable new cases; tests G08/G09/G10 remain byte-for-byte identical.
- `src/cai_g08`, `src/cai_g09`, `src/cai_g10`: inherited code; no edits.
- `contracts`: proposed Lab wire JSON Schema and sample.
- `docs`: security architecture, negative-test threat review, controls, release blockers and decision record.
- `verification`: full SHA-256 source lineage, requirement/test mapping, local build result, and legacy G10 README/runner/manifest archived without changing their bytes.
- `RUN-GATE11-ISOLATED-v1.0.0.ps1`: isolated Windows PowerShell 5.1 test runner. Verifies full manifest and G10 source/test hashes, detects Python 3.10+ and a Git OpenSSL installation, then runs the tests. Changes to `PATH` are **process-only**.

## Reproduction

First verify the downloaded ZIP SHA-256 against the digest given with the downloadable artifact. Extract outside `C:\CAI-EXPERT-LAB` and run the included `RUN-GATE11-ISOLATED-v1.0.0.ps1` using the one-block command in the response. Requires preinstalled Python 3.10+ and OpenSSL 3.5+ with ML-DSA-87; user previously observed OpenSSL 3.5.7 in `C:\Program Files\Git\usr\bin\openssl.exe`.

Runner exit 0 = offline test PASS, 3 = dependency HOLD, other nonzero = FAIL. ZIP hash, signature tests and SHA lineage do not constitute external security assurance. No installs, network downloads, repository writes, commits, pushes or production actions are performed.
