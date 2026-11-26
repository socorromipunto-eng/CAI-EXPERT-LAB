# Technical audit reconciliation and correction package

**Assessment:** CAI-TRIAGE-2026-11-26
**Repository:** socorromipunto-eng/CAI-EXPERT-LAB
**Baseline:** main at 95db83a6f155b68dc0c1ff783731c0086a9fbfde (owner-reported)
**Decision:** HOLD for operational, production, commercial, compliance, or sector-effectiveness claims.

## Evidence boundary

Compared the supplied H-01–H-10 audit with current main files fetched read-only on 2026-11-26. The audit author, independence, qualifications, test environment, and evidence custody were not provided. Its “NASA-style third-party” designation is therefore unverified; this report does not claim independent IV&V or NASA process compliance. Owner-provided Windows CI results are attributed, not re-run here. The Windows checkout, GitHub settings, license authorization, signing key, deployment target, and external anchor were not accessible.

## H-01–H-10 adjudication

| Finding | Current status | Correction / evidence |
|---|---|---|
| H-01 Approver authentication | OPEN; audit's engineering concern is valid. A caller-supplied approver name is attribution, not identity. | Require owner-approved identity authority, credential lifecycle/revocation, authorization, signed approval envelope, replay defense, service-boundary tests, and key custody before any deployment claim. EU AI Act Art. 14 applicability depends on system/use classification and roles; it does not mandate Ed25519 or mTLS. Legal violation is not established from this audit text alone. |
| H-02 Evidence-chain truncation/rewrite | OPEN; four strict xfails remain: three tail-truncation cases and one full-chain rewrite. | Local chain only checks records present. Closure needs an independently administered anchor/write domain, monotonic signed checkpoints, retention, outage/recovery, key rotation, offline verification, and truncation/rewrite/replay/partial-write/rollback tests. A local mock is not closure. |
| H-03 Approval expiry/fact freshness | PARTLY STALE. Pending approvals have expiry and approval-time state/policy revalidation; fact freshness across incidents remains open. | Correct docs to distinguish these controls. Future facts contract needs source identity, timestamp, incident ID, max age, replay sequence, and explicit stale/missing/conflict behavior. |
| H-04 MCP architecture | OPEN. Proposed MCP design is not an enforced boundary. | Keep evaluation-only. A flag/banner is not identity or isolation. Closure requires target-specific threat model, privileged service boundary, authenticated IPC/API, server-side authority, isolation, target-side enforcement, and bypass tests. |
| H-05 Seven xfails | STALE. At the reviewed baseline, the workflow expected 714 passed and 4 xfailed (718 collected). This candidate adds two passing profile-quality/SRMA checks, so its CI gate is 716 passed and 4 xfailed (720 collected). | Correct README count and identify the four truncation/rewrite cases. The candidate count is an expected gate, not a test result until Windows and GitHub Actions pass. |
| H-06 Alternate routes | OPEN for deployment. Engine has no actuator and only governs submitted calls. | In lab, assert no external effect. Deployment closure requires OS/network privilege separation and target-side enforcement; documentation alone cannot enforce it. |
| H-07 Missing sector | Stale as a test-gap. Current source has 16 sector keys, 16 profiles, two examples per key, and a missing-sector escalation regression in its tested scenario. Profile depth/source applicability remains weak. | Correct README claim and add a structural source/applicability gate. This does not validate taxonomy, source currency, asset classification, or effectiveness. |
| H-08 Version decoupling | Observation, not proven defect. Framework, engine, and security spec are separately versioned. | Keep separation. Build a compatibility matrix only after supported combinations and owner/versioning authority are defined. |
| H-09 Main badge | Disclosed: README says badge reports main. | PR checks are review-specific; dynamic badge is optional and not an assurance fix. |
| H-10 Mapping versus compliance | Correctly disclosed in repository. | Preserve the disclaimer in new material and release notes. |

## Sector-quality correction

The 16 files are not equal in depth. Ten already have sector-specific framework tables and direct links but still need current primary-source and entity-scope review. Six—Government Facilities, Healthcare, IT, Nuclear, Transportation, Water—had no direct URLs in their source-basis sections. The correction adds official references, a use statement, and a scope limit to each. A new structural test requires all 16 profiles to contain a government source URL, applicability language, and an explicit non-claim. This is a documentation-quality gate, not legal validation.

CISA IRPF v1.2 (February 2024), p. 54 lists GSA as Government Facilities SRMA and DOT as Transportation Systems SRMA. The registry's current “CISA and GSA” and “TSA and U.S. Coast Guard” values are corrected and pinned by tests. The registry is directory metadata, not authority over individual assets or modes.

| Sector | Added primary references | Scope limitation recorded |
|---|---|---|
| Government Facilities | CISA IRPF v1.2; GSA MV-2022-06; GSA Smart Buildings directive | GSA leasing/program scope is not government-wide. |
| Healthcare and Public Health | HHS HPH Cybersecurity Performance Goals; HICP | HPH CPGs are voluntary; HIPAA applicability requires covered-entity/business-associate and data-scope analysis. |
| Information Technology | NIST SP 800-218 v1.1 Final; v1.2 Initial Public Draft; SP 800-161 Rev. 1 Update 1 | Draft is not final; frameworks do not prove product conformity. |
| Nuclear | 10 CFR 73.54; NRC RG 5.71 Rev. 1 | Not every nuclear material, waste, DOE, or contractor system is in scope. |
| Transportation | CISA IRPF v1.2; TSA directives index | No claim that an individual directive is current or applies to a target. |
| Water | EPA AWIA/SDWA §1433 and cybersecurity assessment page | The over-3,300 population RRA/ERP requirement is for community drinking-water systems, not all wastewater entities. |

## Acceptance and change boundary

The guarded runner must use a new worktree from the expected origin/main SHA; verify source blob IDs and absence of new targets; preserve all existing user changes; pass diff check, Ruff, compileall, complete pytest, the new profile-quality test, and SRMA mapping tests. It must not install dependencies, stage, sign, commit, push, create/update PR, merge, or modify main. The owner reviews the diff and signs any commit locally.

## Residual evidence gates

| Gate | State | Closure evidence |
|---|---|---|
| Authenticated approval | OPEN | Approved identity/authorization architecture, trusted provider/key lifecycle, and invalid/expired/revoked/replay tests. |
| Complete/authentic evidence | OPEN | Independent anchor domain, signed monotonic checkpoints, recovery, offline verifier, adversarial tests, operating evidence. |
| MCP and alternate-route enforcement | OPEN | Named target, privilege-separated service, authenticated IPC/API, target enforcement and bypass tests. |
| Fact freshness/incident binding | OPEN | Approved contract, trusted provenance source, age/incident/replay checks and negative tests. |
| GitHub security settings | NOT VERIFIED | Direct ruleset, bypass, review/check, private-reporting, and monitored-owner evidence. |
| License authorization | OPEN / NOT PROVIDED | Retained written authorization for exact intended operational/commercial/production scope. |
| Independent review | NOT PERFORMED / NOT EVIDENCED | Qualified independent reviewers, independence declaration, pinned scope, reproducible evidence and dispositions. |
| Deployment qualification | NOT PERFORMED | Target hazard/threat case, authorized integration/failure tests, operator/recovery procedures and independent validation. |

**Release remains HOLD.** Passing software tests cannot close these gates.

## Sources

- CISA IRPF v1.2, February 2024, p. 54: https://www.cisa.gov/sites/default/files/2024-02/Infrastructure%20Resilience%20Planning%20Framework%20v1.2_JAN2024_508c.pdf
- HHS HPH CPGs: https://hhscyber.hhs.gov/cybersecurity-performance-goals.html
- NIST SSDF status register: https://csrc.nist.gov/projects/ssdf/publications
- NRC cybersecurity scope: https://www.nrc.gov/facilities-safety/cybersecurity
- EPA AWIA §2013 / SDWA §1433: https://www.epa.gov/waterresilience/awia-section-2013
- EU AI Act, Regulation (EU) 2024/1689, Article 14: https://eur-lex.europa.eu/eli/reg/2024/1689/oj

This is a reviewable local correction candidate, not an applied or signed repository change.
