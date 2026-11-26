# CAI-EXPERT-LAB Assurance Remediation — Execution Baseline

**Assessment date:** 2026-11-26
**Repository:** `socorromipunto-eng/CAI-EXPERT-LAB`
**Scope:** Post-merge state after PR #3
**Decision:** `HOLD` for operational use, production release, and compliance claims.

## 1. Verified post-merge baseline

| Evidence | Observed result |
|---|---|
| PR | #3 is merged and closed. |
| Merge commit | `95db83a6f155b68dc0c1ff783731c0086a9fbfde`. |
| PR source head | `f63e4d55a5175cabd47050d138e159284615b5e6`. |
| GitHub Actions run | Run `45838505301` completed successfully. |
| CI jobs | 7/7 succeeded: Ruff plus Ubuntu/Windows on Python 3.11, 3.12, and 3.13. |
| Test results | Each of the six matrix jobs reported `714 passed, 4 xfailed`. |
| PR reviews | The GitHub review-list API returned no submitted reviews. This does not establish whether informal review occurred. |
| Changed paths | 32 files were included in PR #3. `docs/assurance/` was not in the PR changed-file list. Current local status is not available in this assessment. |

CI proves the configured checks passed for the merged source head. It does not close the four expected failures or establish operational security, legal authorization, independent review, or deployment qualification.

## 2. Current findings and acceptance evidence

### EVID-01 — Evidence completeness and authenticity

**Status:** `OPEN / LIMIT`
**Observed:** The test suite retains three strict expected failures for evidence-tail truncation and one for rewriting the complete local chain. The current evidence log is locally hash-chained; a local writer can rewrite the chain and its local snapshot.
**Required architecture:** A checkpoint/signature trust domain independent of the engine host, with monotonically increasing sequence/checkpoint state, append-only retention, offline verification, and documented key rotation/recovery. The provider and deployment account have not been selected in this record.
**Acceptance evidence:** Negative tests for suffix truncation, full-chain rewrite, replay/rollback, duplicate/out-of-order checkpoints, invalid signatures, key rotation, and anchor outage/recovery; externally stored checkpoint evidence; independent review. Retire the four `xfail` markers only when those tests pass against the actual trust boundary.

### SEC-01 — Deployed security boundary and actuator control

**Status:** `OPEN`
**Observed:** The MCP interface describes itself as a local decision interface; it does not authenticate the approver, constrain alternate client routes, or control an external actuator. A caller-supplied approval name is attribution, not authentication.
**Required architecture:** Identify the target host/service, identity provider, authorization source, IPC/network boundary, privilege separation, and target-side adapter. The target must enforce the decision and prevent ungoverned alternate routes.
**Acceptance evidence:** Threat model and approved deployment diagram; least-privilege service identity; authenticated caller and approver; server-side authority/asset context; negative tests for bypass, replay, impersonation, alternate paths, outage, and recovery; target-side enforcement evidence; owner-approved non-production validation.

### TEL-01 — Telemetry-to-decision evidence linkage

**Status:** `OPEN`
**Observed:** `ingest` records accepted telemetry and freshness is checked, but governed decisions do not require a verifiable reference to the accepted telemetry they depend on.
**Required contract:** Define which decision types require telemetry; identify each event by immutable event ID and digest; bind the accepted event references into the decision/evidence record; validate source identity, timestamp, freshness, replay/sequence, and missing/conflicting data.
**Acceptance evidence:** Positive and negative tests for missing, stale, future-dated, replayed, forged-source, duplicate, conflicting, and tampered events; decision records that can be independently traced to their input event digests. The policy defining telemetry-required decisions needs owner approval before implementation.

### GH-01 — Effective repository controls

**Status:** `NOT VERIFIED`
**Observed:** `SECURITY.md` exists and explicitly says its presence does not prove private vulnerability reporting is enabled or monitored. Branch protection, required reviews, bypass rights, and private reporting settings were not readable through the current integration.
**Acceptance evidence:** Owner-collected settings evidence for protected `main`, required successful CI checks, required independent approval, stale-review dismissal, restricted bypass/force-push, signed-commit policy if required, and enabled/monitored private vulnerability reporting. Preserve the settings snapshot and responsible contact/rotation evidence.

### LEG-01 / IVV-01 — License, independent review, and deployment qualification

**Status:** `OPEN`
**Observed:** The repository license requires prior written authorization for the intended operational/production/commercial scope. No such authorization, independent technical/regulatory review, or deployment qualification was present in the examined PR evidence.
**Acceptance evidence:** Written scope-specific authorization by the rights holder; named independent reviewers with documented scope and independence; findings and dispositions; target-environment qualification evidence. Author self-review and CI cannot satisfy independent review.

### DOC-01 — Post-merge record reconciliation

**Status:** `OPEN — DOCUMENTATION CHANGE REQUIRED`
**Observed:** The closeout report records the 2026-11-19 snapshot (PR head `b4967e3`, 702 passed/4 xfailed, PR open/draft). The sector review record documents the proposed patch at baseline `13770201...`. Preserve these as historical records; they are not an as-built record of the merged state.
**Required update:** Add a dated, append-only post-merge reconciliation recording merge commit `95db83a...`, PR head `f63e4d5...`, workflow run `45838505301`, 7/7 successful jobs, six results of 714 passed/4 xfailed, zero submitted reviews, remaining open findings above, and the `HOLD` decision. Do not rewrite the historical baseline or claim the residual findings are closed.

## 3. Change-control sequence

1. Create a new branch from the current `main` and add `DOC-01` as an append-only record. Review the exact diff, sign the commit, and open a new PR.
2. Approve the telemetry decision contract and target architecture before changing decision semantics or claiming a security boundary.
3. Select and provision the independent evidence-anchor trust domain; implement and adversarially test it before removing evidence `xfail` cases.
4. Implement the deployment boundary and target-side adapter only for an identified, owner-authorized non-production target; test bypass and failure paths.
5. Capture GitHub repository-settings evidence and written license authorization. Request independent technical and regulatory reviewers; do not self-certify.
6. Re-run the full CI matrix on each code change. Keep release status `HOLD` until every applicable acceptance item has evidence and independent disposition.

## 4. Unverified items

- Cryptographic verification of the GitHub-generated merge commit was not exposed by the repository connector; do not infer its signature state from the signed source-branch commits.
- Effective GitHub branch rules and private vulnerability reporting were not verified.
- Current local working-tree state, including any untracked `docs/assurance/` material, was not available.
- No anchor provider, deployment target, operational scope, license authorization document, or independent reviewer was identified in the inspected evidence.
