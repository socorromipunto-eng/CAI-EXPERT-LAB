# CAI-GOVERNED-LLM — GATE 13 v0.3.5 — Adversarial Integration Offline Lab

**Owner / project author:** Antonio José Socorro Marín  
**Development assistance:** AI-assisted; *not* human-independent review.  
**Status:** BUILDER OFFLINE LAB PASS; OWNER WINDOWS PENDING; ENTERPRISE ASSURANCE HOLD.  
**Authorization:** development of an offline GATE13 package only; repository integration, Git commit/push, third-party execution, production and installation not authorized.

## What runs

This is executable Python code, not just a security checklist:

- `src/cai_g13/integration.py`: `SignedDualGatePipeline` combining independently ML-DSA-87-approved G11 **read-only** fixture inspection and separately ML-DSA-87-approved G12 **local temp-file PUT_ONCE**; a trusted in-process plan pins resource, actor, tenant, read digest and exact effect request digest. The read text is treated strictly as opaque untrusted data and is NEVER parsed as a new command. `ReceiptInspector` independently re-opens the file via a different *code path*, compares bytes, and correlates the signed receipt to local SQLite journal state. It is **not** independent OS isolation or human IV&V.
- `tests/test_gate13.py`: 89 new test methods, with 12 additional prompt-like malicious data cases under `subTest`. Tests validate dual authorizations, tenant/identity rejection, content-to-command separation, replay, signature tampering, receipt forgery, journal tampering, interruption handling, and concurrent duplicate attempts. Injected shell/network/LLM strings **are inert fixture text**: no live LLM is involved.
- `src/cai_g13/run_gate13.py`: verified test inventory, G12 exact-code/test SHA256 lineage, 10 control traceability, 413 test runs, machine-readable observed outcome, explicit `HOLD` claims.
- `RUN-GATE13-ISOLATED-v1.0.0.ps1`: PowerShell 5.1 runner; checks extraction completeness and hashes; requires previously installed Python >=3.10 and OpenSSL >=3.5 with ML-DSA-87; runs locally outside the repo. No downloading or installing dependencies, no Git mutation or remote systems.

## Baseline and inherited evidence

All **22** `src/cai_g08` through `src/cai_g12` Python source files and corresponding `tests/test_gate08.py` through `tests/test_gate12.py` files are inherited **byte-for-byte** from the corrected G12 v0.3.4.1 ZIP. The prior G12 README and manifest are preserved separately in `docs/G12-README-AS-INHERITED.md` and `verification/G12-MANIFEST-AS-INHERITED.txt`. All other inherited G12 files remain present, including the Windows SQLite handle correction.

G12 Windows lab PASS was **reported by the owner** in chat after correction. This ZIP contains no independently fetched Windows transcript. G13 builder tests passed in Linux OpenSSL 3.5.5; user Windows G13 execution has **not happened** at package creation time.

## Threat-assurance distinction

- **TESTED:** local denial of in-process attempts to promote adversarial fixture text to local file effect; actual ML-DSA-87 local signatures; tampered receipts/journal detection for specific cases; local replay and concurrency cases.
- **NOT TESTED:** actual LLM prompt injection defense, external MCP protocol transport or arbitrary tools, Windows security boundary, hostile same-process actor, network egress firewall, production IdP/MFA/HSM/KMS, distributed fencing/persistence, trusted clock/immutable audit, canonical CAI CORE DSA/ESA/D(t), OT safety, independent human IV&V or enterprise release.
- A locally valid `SUCCEEDED` receipt asserts only a matching effect was *currently observed in the lab*; it is not proof of enterprise action completion or persistence. The test keys are temporary **unencrypted** PEM; no keys are included in the ZIP.

## Run instructions

Verify the ZIP SHA-256 supplied with this answer, inspect/extract it outside `C:\CAI-EXPERT-LAB`, and run the PowerShell snippet provided with the package. Never run it in production. A nonzero exit means FAIL/HOLD, not PASS. `python -B -m cai_g13.run_gate13` may also be called in an authorized lab with `PYTHONPATH` pointed at `src`.

## Review and commit status

See `docs/G13-GOVERNANCE-AND-GATE14.md`. The proposed sequence remains G13 owner replay -> G14 independently performed technical/governance audit -> separately authorized scoped repository integration and staging -> separate commit approval at G15 -> distinct push/release decisions. No commit or push in this delivery.

Official license/terms remain those in the owner's canonical `/legal`; this ZIP provides no new permission to third parties.
