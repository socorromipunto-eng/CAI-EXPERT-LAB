# PR #3 software closeout — R01–R10

**Date:** 2026-11-19

**Reviewed base:** `80cd71e1620c5c580f6697742f520d329fa13709` (`main`)

**Reviewed PR head:** `b4967e36c12dc4e59df728a12324443643617de4`

**Decision:** `HOLD` for release or operational deployment. This report records scoped software fixes; it is not a compliance assessment or independent audit.

## Scope and historical case separation

This candidate addresses the current R01–R10 findings only. Historical T01–T10 records remain historical and are not renamed, reclassified, or merged with R01–R10. No unrelated local `docs/assurance/` material is included in this package.

## Corrective changes in this candidate

| Finding | Change | Evidence / remaining limit |
|---|---|---|
| F-01: missing sector could remove oversight for OT/destructive actions | USA governed evaluation now escalates when sector context is absent and the action identifies an OT level or destructive effect. | Regression test asserts pending human approval and the named escalation gate. This is a decision control inside the reference engine, not a deployed security boundary or independent source of sector authority. |
| SGH 5.2: pending approval had no timeout | Pending records carry creation time, expiry time, and TTL. Approval rejects and consumes expired records; expiry during revalidation also fails closed. | Deterministic test advances the clock, verifies the expiry event, and verifies no execution event. This does not identify/ authenticate the approver or provide an external actuator boundary. |
| AUD-07 / TAX 8.5: stale telemetry was accepted | Engine ingestion rejects telemetry older than the configured maximum age and timestamps beyond the configured future-skew allowance. Defaults: 300 seconds and 60 seconds. Constructor rejects invalid/non-finite settings. | Freshness tests and full suite. **Accepted telemetry is still not linked as a decision input/evidence reference to governed actions**; that separate integration claim remains open. |
| R06: partial append could leave a torn JSONL record | Append records the original file length and attempts truncate + fsync rollback after a write/fsync error; rollback failure raises a fail-closed evidence error. | Injected disk-full test writes a partial suffix, raises `ENOSPC`, and verifies exact byte-for-byte rollback and valid prior chain. Process/power loss at every instruction boundary and Windows filesystem durability remain untested. |
| Missing vulnerability-reporting policy | Added repository-root `SECURITY.md` with private-reporting instructions, handling scope, no invented SLA, and an explicit requirement to enable/monitor the private channel. | The file does not prove GitHub private vulnerability reporting is enabled or monitored; repository owner must verify the setting and contact route. |
| Workflow supply-chain and CI gate review | Confirmed the current workflow already pins `actions/checkout` and `actions/setup-python` to full commit SHAs, uses read-only contents permission, and disables persisted checkout credentials. Updated the stale expected suite count from `698 passed, 7 xfailed` to `702 passed, 4 xfailed`. | No branch-protection or required-review configuration was changed. The GitHub branch-protection API returned 403 for this integration, so those settings remain unverified. |

## Validation performed in this isolated copy

- Full implementation suite: **702 passed, 4 xfailed**.
- Ruff lint on the six changed Python files: **passed**.
- Python bytecode compilation for `cai_engine` and `tests`: **passed**.
- The 4 expected failures are the three tail-truncation variants and whole-chain rewrite. All require a trusted external checkpoint/signature; a local hash chain cannot establish historical completeness or authenticity.
- The optional MCP dependency was installed for the complete run, so the MCP interface test executed; no tests were skipped.

The candidate passed in an isolated Linux copy. After applying it locally on 2026-11-19, the repository owner reported that Windows Ruff and compileall passed and the full suite reported **702 passed, 4 xfailed**. This is owner-provided terminal evidence, not independent validation. Windows locking and durability beyond the tested failure case remain untested.

## Open decision and assurance items

1. **R07/R08 external evidence trust:** no independent anchor, monotonic checkpoint service, or signed evidence head is configured. Keep `LIMIT` and release `HOLD` until provisioned and independently tested.
2. **R09 execution boundary:** the reference engine records decisions and does not control all alternate client routes or an external actuator. No claim of a deployed security boundary is made.
3. **Evidence-to-decision linkage:** accepted telemetry freshness is checked, but telemetry is not yet bound to the action decision as a required, reviewable evidence reference.
4. **License and operational scope:** retain the license restriction. Production/commercial/operational use requires the copyright holder's prior written authorization under the repository license; a code change cannot grant it.
5. **Repository controls:** `SECURITY.md` and the CI expected count are included in this candidate. The existing workflow already used full-SHA Action pins. GitHub branch-protection/required-review settings could not be read (API 403); they must be verified by the owner in repository settings. The private vulnerability-reporting option and monitored contact route must also be enabled and verified by the owner.
6. **Independent validation and regulatory claims:** no independent technical reviewer, competent regulatory assessment, deployment qualification, or physical/hardware validation was performed. Mapping documents are not certification or legal compliance evidence.

## Change control

The owner applied the candidate in the Windows repository, signed commit b5537a235bd57b0a5952ec226fc2b0e34ea3407a with the configured ED25519 key, and pushed it to PR #3. GitHub read-only verification confirmed the PR remains open and draft against main; it is not merged. No workflow runs or status checks were returned for that commit at inspection time. Updating the PR description was denied by the connected GitHub integration (HTTP 403), so its text still needs owner-side reconciliation.

## Change record and dual-audit boundary

| Field | Record |
|---|---|
| Candidate change ID | `CHG-CAI-ENGINE-R01-R10-2026-11-18` (candidate identifier; owner must confirm against the authoritative register before publication) |
| Category | Engine correction, regression tests, CI count reconciliation, security-reporting documentation |
| Baseline | PR #3 head `b4967e36c12dc4e59df728a12324443643617de4`; base `main` `80cd71e1620c5c580f6697742f520d329fa13709` |
| Affected paths | `CAI-Engine/implementation/cai_engine/{engine.py,evidence.py,governed_agent.py}`; `CAI-Engine/implementation/tests/{test_cai_engine.py,TEST_EVIDENCE_AND_CONTRACTS.py,TEST_SPECIFICATION_MATRIX.py}`; `CAI-Engine/implementation/AUDIT-PR3-SOFTWARE-CLOSEOUT.md`; `.github/workflows/CAI-ENGINE-TESTS.yml`; `SECURITY.md` |
| Human authorization | The owner authorized applying the candidate and signing/pushing it to the existing draft branch. No merge, main-branch change, branch-protection change, or license-rights grant was authorized or performed. |
| AI assistance | ChatGPT prepared the scoped code, tests, workflow count update, and this report. No authorship/coauthor claim is made. The owner must review and record the contribution in the approved project evidence process. |
| Technical review | Isolated Linux validation plus owner-reported Windows Ruff, compileall, and complete suite (702 passed, 4 xfailed). These are not independent IV&V. |
| Governance review | Not performed independently. Owner must reconcile this candidate against CAI Core, legal records, and the authoritative Evolution Traceability Register. |
| Rollback | The PowerShell runner saves the seven replaced files under Downloads before copying; newly created `SECURITY.md` and report can be removed if the owner rejects the candidate. The runner stops on changed target files and does not touch unrelated paths. |
| Publication reference | Signed commit b5537a235bd57b0a5952ec226fc2b0e34ea3407a is on PR #3 draft branch; no merge to main. Release remains HOLD pending external and independent assurance gates. |

### Risk review (devil's advocate / technical destruction)

- A 300-second approval TTL and 300-second telemetry freshness default can reject legitimate delayed workflows. The constructor allows a bounded local configuration, but target-specific limits need owner approval and evidence.
- The missing-sector escalation trusts action metadata to identify an OT/destructive action. It does not create a trusted asset inventory, authenticate context, isolate privileges, or prevent alternate client routes.
- Partial-write rollback covers a caught I/O error, including a simulated disk-full error. A power loss, process kill between write and rollback, storage controller lie, or rollback failure remains a SAFE_HALT/recovery case and requires platform-specific testing.
- The CI count is deliberately exact. Any platform-specific test variation will fail closed and require investigation rather than relaxing the gate.
- The `SECURITY.md` process is only a written process. Until the owner confirms the GitHub setting and monitored contact route, private reporting is not proven available.

No authoritative Evolution Traceability Register entry or independent governance approval was created here; publication remains HOLD until that controlled project step is completed.
