# G11-DEC-001 — Controlled Engineering Decision

**Author / owner:** Antonio José Socorro Marín.  
**AI assistance:** design/source/tests and local self-verification, not independent technical/governance IV&V.  
**Authorization:** owner approved isolated GATE 11 lab code, offline testing, ZIP + SHA + PowerShell; NOT repository mutation, commit, push, external identity/network connections or production.

## Source controls

- Prior GATE 10 Windows evidence supplied by owner: 169/169 PASS, OpenSSL 3.5.7, real ML-DSA-87, no enterprise assurance claim.
- Unmodified G08/G09/G10 implementation/test files are covered by exact GATE 10 ZIP SHA-256 lineage checks.
- Current G11 runner enforces complete package SHA256SUMS and source/test lineage before execution.
- New G11 test coverage: 92 named cases; 8 proposed G11 control IDs with executable tests.
- Prior G05 finding count 20: no finding CLOSED VERIFIED solely by this developer self-assessment.

## Decision matrix

| Decision dimension | Local builder status | Owner Windows status | Enterprise status |
|---|---|---|---|
| Source integrity and lineage | PASS (builder packaging verification) | PENDING | Source chain only |
| New signed fixture call gateway | LAB TEST PASS | PENDING | HOLD |
| G08–G10 regression | LAB TEST PASS | Previously G10 PASS; G11 regression PENDING | HOLD |
| Actual MCP server and process isolation | NOT TESTED | NOT TESTED | HOLD |
| Real identity, HSM/KMS, protected session | NOT TESTED | NOT TESTED | HOLD |
| Canonical CORE DSA/ESA/`D(t)` | NOT TESTED | NOT TESTED | HOLD |
| Independent technical and governance audit | NOT SUPPLIED | NOT SUPPLIED | HOLD |
| Deployment/release | NOT AUTHORIZED | NOT AUTHORIZED | HOLD |

**Overall:** `GATE 11 — OFFLINE LAB SOURCE/TEST PASS; ENTERPRISE ASSURANCE HOLD`. Passing code tests cannot close these blocks.

## Change control

Entire archive is prepared outside `C:\CAI-EXPERT-LAB`. No CORE modification, deployment, installations, Git changes or publications. For any future repository change, define exact destinations, pre/post evidence, reversibility, scope, and separate authorization. Stage proposed integration only after technical/governance reviews; a human owner decision is distinct from an independently verified control.
