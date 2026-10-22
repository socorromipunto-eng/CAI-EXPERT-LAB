# CHG-CAI-GLLM-GOV-001 - G15 provenance and assurance reconciliation

**Status:** PROPOSED / HOLD - owner review and dual audit pending.\
**Record date:** 2026-10-21 (new reconciliation record; not a backdated approval).\
**Project owner and human decision authority:** Antonio José Socorro Marín.\
**Drafting assistance:** AI-assisted; no independent human IV&V is claimed.\
**Baseline repository:** `socorromipunto-eng/CAI-EXPERT-LAB`, `main`, commit `d61966bc3058e8ad7ab40b0a16c83529232b8309`.\
**Change category:** Additive historical reconciliation / documentation only.\
**Authorized boundary:** Create this one local document for review. No staging, commit, push, publication, history rewrite, CORE edit, Engine edit, licensing change, or production action is authorized by this record.

## 1. Purpose and authority

This record reconciles the original GATE13 offline-package statements with subsequent owner-reported Windows checks, authorized GATE15 local integration and GitHub publication, and subsequent recovery of repository-local SSH signing configuration. It does not retroactively change the original package's authorization or evidence.

CAI-EXPERT-LAB is governed by its **own canonical CAI CORE** and approved repository policies, including `AI-GOVERNANCE.md`, `/legal`, `docs/CORE/CAI-Core-Integrity-and-Self-Defense-Governance.md`, `docs/CORE/CAI-Core-Dual-Audit-Pipeline.md`, `docs/CORE/CAI-Core-Standards-Evolution-and-Governance.md`, and the traceability register. This document cannot amend or override those sources. The core is decision-centric, using DSA, ESA, continuous validation, execution-boundary admissibility, traceability, and contamination protection. The seven-stage defensive lifecycle is a **derived operational branch**, not the definition of the core.

## 2. Chronology and observed-versus-reported evidence

| ID | Event or assertion | Evidence basis | Disposition / limitation |
| --- | --- | --- | --- |
| G15-R01 | GATE13 package originally stated `BUILDER OFFLINE LAB PASS; OWNER WINDOWS PENDING; ENTERPRISE ASSURANCE HOLD` and did not authorize Git operations. | `labs/ai/governed-llm/README.md` and `docs/G13-DECISION-AND-COMMIT-BOUNDARY.md` at pinned HEAD | Accurate **as-of-package** snapshot; retain historical text. |
| G15-R02 | GATE13 owner Windows offline suite reported 413/413; later consolidated G14-G16 offline suite reported 456/456. | Owner-provided console outcomes in project conversation | **OWNER-REPORTED**, not an independently collected or human-IV&V-certified transcript. Preserve raw logs and hashes separately when available. |
| G15-R03 | Owner subsequently authorized scoped copy, stage, local commit, and push as distinct boundaries. | Conversation authorizations and runner outcomes; must be archived as evidence for independent audit | Later authorizations do **not** retroactively change package-build authorization. |
| G15-R04 | GitHub `main` advanced from `ccc5d0a6d21ec9a214cfd15b6918797a5c4f5e71` to `d61966bc3058e8ad7ab40b0a16c83529232b8309`: 76 added files, 6,893 additions, zero deletions. | GitHub commit API and owner-controlled PowerShell push transcript | **PUBLISHED** within scope; not enterprise release or CORE promotion. |
| G15-R05 | Published G15 commit `d61966bc...` is `unsigned`; its parent `ccc5d0a6...` is GitHub-verified SSH-signed. | GitHub commit verification records | **PROVENANCE EXCEPTION / HOLD** for unsigned G15 commit; preserve both commits unchanged. |
| G15-R06 | Owner's existing `cai_signing_ed25519` Ed25519 key signed an ephemeral challenge; previous signed commit verified locally; `commit.gpgsign=true`, `gpg.format=ssh` configured locally. | Owner-provided PowerShell recovery transcript reporting `CAI_SIGNING_RECOVERY=PASS` | **LOCAL CONFIGURATION RECOVERY PASS**; not retroactive signing of G15 or server-enforced branch policy. Private key/passphrase not collected. |

## 3. External references: alignment, not subordination

CAI combines external bodies' work through explicitly scoped mappings. References do **not** independently redefine CAI CORE or establish a universal compliance claim.

| Reference family | Distinct role in CAI | Applicability / verification boundary |
| --- | --- | --- |
| **NIST** CSF, SP 800-53, SP 800-171/171A, AI RMF | Risk governance, control objectives, assessment evidence, AI risk | Version, audience, and contractual/regulatory applicability require official-source confirmation per use case. |
| **CISA** CPGs, Zero Trust, Secure by Design, ICS guidance | Operational prioritization, cyber resilience and sector/OT defense | Guidance is not automatically a mandatory legal control for all deployments. |
| **NASA** systems engineering, software assurance and IV&V | Requirements quality, traceability, safety review, evidence discipline, independent evaluation model | NASA requirements bind only when program/contract applicability is established; AI/builder self-review is not independent IV&V. |
| **MITRE** ATT&CK / D3FEND | Threat behavior mapping and defensive-technique taxonomy | Taxonomy is **not** CAI governance authority. Existing repository wording attributing the seven-stage *order* to MITRE requires a separate source-attribution review; no silent semantic correction here. |
| **ISO/IEC** 27001 and **IEC** 62443 | Security-management and industrial-control-system assurance references | Select editions and requirements according to product/sector/jurisdiction; alignment is not certification. |
| **CMMC** and sector/regional frameworks | Scoped contractual or regulatory overlay where actually applicable | Do not inherit obligations outside the affected contract, system or jurisdiction. |
| **Aviation/aerospace sources**, when a real use case demands them | Safety, airworthiness and sector engineering overlay | Authority, document edition and applicability are **NOT VERIFIED** here; no aviation certification is asserted. |

The repository's `METHODOLOGY.md` and `REGULATORY-BASIS.md` provide existing mappings. They must not substitute for verifying current official standards, amendments, dates, or applicability at a future normative review. External changes trigger governed review, not automatic modification of core semantics.

## 4. Assurance and security boundaries

**Demonstrated/reported within the lab boundary:** offline fixture tests, bounded local-file effect and inspection, signature/receipt tests and adversarial fixture cases as documented by the published G08-G13 artifact. Exact owner Windows execution counts are owner-reported here; not independently recollected.

**Not established by these results:** real LLM prompt-injection resilience, external MCP deployments, production OS/container isolation, IdP/MFA, KMS/HSM custody, durable distributed fencing, immutable enterprise evidence, live OT safety, supply-chain qualification, independent human technical/governance IV&V, regulatory certification, or production approval.

Current dispositions are separate:

- `G15_LOCAL_INTEGRATION_AND_REMOTE_PUBLICATION=PASS` (for the precisely authorized 76-file scope).
- `G15_PUBLISHED_COMMIT_SIGNATURE=HOLD` (original published commit is unsigned; no retroactive claim).
- `G15_FUTURE_LOCAL_SIGNING_RECOVERY=PASS` (owner-reported successful configuration and challenge).
- `G14_INDEPENDENT_HUMAN_IVV=HOLD` (no independent human approval evidence).
- `G16_ENTERPRISE_PRODUCTION_RELEASE=HOLD`.

## 5. Required audit and disposition

**Technical audit - PENDING:** verify this document against pinned Git objects, owner-supplied Windows raw logs and hashes where available, the exact 76-file manifest, signing fingerprint and original GitHub verification; review MITRE taxonomy attribution without editing canonical sources.

**Governance audit - PENDING:** confirm source-of-truth hierarchy, separate historical and later authorization boundaries, AI assistance disclosure, legal/IP language, external-reference applicability, no compliance overclaims, and no implied independent review.

**Human readability, devil's advocate, technical destruction, and independent human reviewer:** NOT COMPLETED / NOT ASSIGNED unless later evidenced. A technical writer's or AI's self-review cannot close these obligations.

**Residual risks:** unsigned G15 commit; local Git configuration alone is not remote enforcement; historical docs reflect their package-build state; external-source taxonomy attribution pending review; enterprise controls and independent IV&V unverified.

**Decision:** `PROPOSED / HOLD`. Owner-authorized local document creation does not authorize staging, committing, publishing, updating historical records, rewriting Git history, modifying `/legal`, or promoting the G13 lab into enterprise production.

## 6. Controlled next boundary

After the owner reviews this document, separately adjudicate technical/governance audit findings and decide whether to authorize staging of this **one exact file**. A later signed commit and push would each require their **own** explicit approval and integrity verification. Preserve the original unsigned commit and all historical lab documents. No `--amend`, `--force`, rebase, or retroactive approval entries.

**Proposed evidence key:** `CHG-CAI-GLLM-GOV-001` (this record's SHA-256 to be captured at creation; not a fabricated pre-existing digest).\
**Framework semantic change:** NONE.\
**Affected existing paths:** NONE.\
**Human approval to promote:** PENDING.
