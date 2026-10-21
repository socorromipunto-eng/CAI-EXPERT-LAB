# CAI-GOVERNED-LLM — GATE 10 — v0.3.2 — REAL ML-DSA-87 CRYPTO LAB

**Status:** BUILD-LAB-PASS / WINDOWS-EXECUTION-NOT-YET-OBSERVED / ENTERPRISE-ASSURANCE-HOLD  
**Owner:** Antonio José Socorro Marín  
**AI-assistance:** assisted drafting, prototyping and local testing; no independent IV&V claimed.  
**Legal:** preserve existing CAI-EXPERT-LAB `/legal` policies, including author ownership, reserved rights and written permissions. No new public license granted.

This package adds **actual post-quantum signing and verification**, using **OpenSSL 3.5+ ML-DSA-87** (NIST FIPS 204 algorithm family) to the isolated G08/G09 test simulation. It is NOT a mock signature, cryptographic hash masquerading as a signature or production identity system.

## What it implements

- ML-DSA-87 key generation **only in temporary laboratory directories**, asymmetric signature generation, public-key verification, 4,627-byte raw signatures, and an OpenSSL ML-DSA signing context.
- Strict signed approval payload schema, deterministic canonical JSON, explicit message domain separation, request/context/policy/tenant/audience/nonce/expiry binding.
- Explicit externally provisioned lab trust registry with SHA-256 over DER SPKI as key identifier; no self-asserted envelope key is trusted.
- Signature and identity binding, purpose-scoped signers, key revocation in memory, approval age limits, separation of duties, dual-control and OT safety signatures.
- Concurrent, atomic **in-memory** replay-consumption guard and fail-closed negative verification.
- G09 fixture executor dispatch only AFTER cryptographic quorum succeeds; no real external calls.
- G08+G09 inherited sources and tests kept byte-for-byte identical, verified against the preceding ZIP.
- **169 tests total**: G08+G09 112 regressions and G10 57 real-crypto/adversarial tests, in the creator laboratory. Actual Windows result not observed until owner runs.

## Explicit exclusions / release BLOCKERS

- **Not a CAI CORE binding**: no assertion that DSA, ESA or D(t) canonical semantics were checked.
- No production identities, federated tokens, real MFA, certificate path, PKI, HSM or managed KMS.
- Temporary *unencrypted* laboratory private-key PEM files are generated at runtime, never packaged; test-only and NOT suitable for production/private data.
- In-memory replay/revocation and in-process TOCTOU controls do not provide distributed durability, leader election or external execution fencing.
- No external MCP sandbox, SaaS, real automation, network connection, or execution receipts.
- No verified independent human technical/governance audit, FIPS-validated cryptographic module assurance, regulatory compliance, certification, or deployment approval.
- Local fake clock, actors and policy data remain G09 fixtures; cryptographic proof does NOT authenticate the individual independent of a governed trust enrollment process.
- Cryptographic agility policy / ML-DSA-87 selection remains proposed; owner may change it in a future ADR.

## Environment and fail-closed behavior

Use **Windows PowerShell 5.1**, **Python 3.10+** and **OpenSSL 3.5+** with a provider offering **ML-DSA-87**. The package has **no Python third-party dependency** and installs nothing. It performs no downloads. If compatible OpenSSL is not in PATH, runner reports **HOLD** and stops without faking signatures. This is expected for machines with OpenSSL 3.0 or without OpenSSL.

### Offline execution after verifying the outer SHA-256

Run `RUN-GATE10-ISOLATED-v1.0.0.ps1` from an extracted directory **outside** `C:\CAI-EXPERT-LAB`. It validates SHA256SUMS against the complete inventory, confirms inherited G09 source/test hashes, detects a Python interpreter and compatible OpenSSL, and runs all 169 tests. Temporary keys are created and erased via `TemporaryDirectory`; data may have filesystem recovery remnants, so use disposable lab storage only.

The owner can use the one-block download verification/extraction/run command given in the accompanying message. In this package, `exit 0` = LAB PASS; `exit 3` = environment HOLD; `exit 1` = test FAIL; exceptions = integrity FAIL.

## Contents

- `src/cai_g10/pqc.py`: genuine ML-DSA-87 provider wrapper, canonical envelope, ephemeral laboratory signer, trust registry, verification and G09-boundary wrapper.
- `src/cai_g10/run_gate10.py`: executable test runner with machine-readable **runtime** report printed to stdout.
- `src/cai_g08`, `src/cai_g09`, `tests/test_gate08.py`, `tests/test_gate09.py`: unmodified G09 distribution source and regression tests.
- `tests/test_gate10.py`: 57 new positive/negative real-crypto tests.
- `docs`: architecture, threat review, test decision, limitations and roadmap.
- `verification`: inherited source hashes and complete test coverage CSV plus observed builder log.
- `SHA256SUMS.txt`: complete hash list covering all package files except the manifest itself.

## Verified primary references

- NIST FIPS 204 (final, 2024): https://csrc.nist.gov/pubs/fips/204/final (also check NIST's 2026 planning note / errata)
- OpenSSL 3.5 `pkeyutl`: https://docs.openssl.org/3.5/man1/openssl-pkeyutl/

These references describe algorithms and interfaces. They do **not** mean this laboratory implementation is certified, independently verified or FIPS 140-validated.
