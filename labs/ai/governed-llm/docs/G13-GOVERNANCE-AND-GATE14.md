# G13-GOV-001 — Decision, authorization, evidence and GATE14 handoff

## Who authorizes what

- **Owner:** Antonio José Socorro Marín; author of CAI-EXPERT-LAB; AI-assisted experimental package creation disclosed.
- **Development authorization:** user agreed to continue project after G12 Windows lab PASS, previously asked to begin G13 under isolated scope. This permits a disposable offline development artifact, not changes to canonical CAI CORE or Git.
- **Not authorized:** installation, external MCP/LLM systems, real identity/keys, production, Git staging, commit, push or release.
- **Human technical reviewer:** NOT ASSIGNED. **Human governance reviewer:** NOT ASSIGNED. Do not count builder/assistant as independent IV&V.

## Evidence register

| Evidence | Collection | Integrity | Limitation |
| --- | --- | --- | --- |
| G13-E01 | `verification/G13-BUILDER-ACTUAL-RUN.txt` | packaged in SHA256SUMS; runner verifies | builder Linux only; not independent human review |
| G13-E02 | `verification/G13-TEST-TRACEABILITY.csv` | manifest SHA | maps 89 methods; test quality still needs review |
| G13-E03 | `verification/G12-INHERITED-SOURCE-AND-TEST-SHA256.txt` | checks 22 inherited code/tests | does not establish current canonical repository status |
| G13-E04 | owner Windows G13 console result | NOT YET RECEIVED | no Windows PASS claim permitted until observed |
| G13-E05 | signed receipt in OS temp test | ephemeral, lab-only | test keys unencrypted; not durable trusted evidence |

## GATE14 exit criteria (proposed; NOT passed)

1. Independent human technical review of G08–G13 code, signed intent semantics, receipt binding, original source and test logs, negative/adversarial coverage, threat model and known bypasses.
2. Independent human governance review of owner authorization, canonical source precedence, `/legal`, privacy/data handling, regulatory reference applicability and source-to-control-to-test-to-evidence mapping.
3. Reconcile historical 20 GATE05 findings with *current pinned canonical Git revision* (do not assume they are still open/closed).
4. Confirm actual OS process isolation, external MCP / LLM prompt injection threat model and KMS/IdP boundary are either separately tested or registered enterprise blockers.
5. Require human adjudication of open risks and any exception disposition. Without human evidence: **GATE14 HOLD**.
6. After G14, prepare a **read-only** candidate integration/diff proposal for GATE15. Owner must independently authorize a local repository copy, staging, commit and push; no blanket permission implied.

## Decision vocabulary

`LAB PASS` means no observed failures in the stated offline fixture test set. `ENTERPRISE HOLD` means required evidence/capabilities absent. `FAIL` means observed break of an explicit required test or integrity invariant. No outcome is an enterprise compliance certification.
