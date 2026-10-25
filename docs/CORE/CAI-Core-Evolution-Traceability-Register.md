CAI-Core-Evolution-Traceability-Register.md

# Cybersecurity Artificial Intelligence Framework – Evolution Traceability Register
Version 0.1 (Draft)  

Document revision: 0.1.1. Framework baseline: CAI Core v0.1 (research preview).
Change ID: CHG-CAI-GOV-RECON-2026-10-23.

Author: Antonio José Socorro Marín  
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)  

Copyright © 2025 Antonio José Socorro Marín.  
All rights reserved.  
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.  

**NOTE**  
The normative language of CAI-EXPERT-LAB documentation is English.  
This document defines mandatory evolution traceability requirements at the Core level and does not assert compliance, certification, accreditation, or regulatory approval.  

## Purpose

The purpose of this document is to define the mandatory Evolution Traceability Register for the Cybersecurity Artificial Intelligence Framework (CAI).

This register establishes a formal, auditable, and non-bypassable mechanism to record, justify, and govern all changes to the CAI framework, including conceptual, semantic, architectural, operational, and governance-related modifications.

The Evolution Traceability Register ensures that CAI evolution is explicit, controlled, reviewable, and defensible over time, preventing silent changes, undocumented reinterpretations, and untraceable drift.

## Scope

This register applies to all CAI Core documents, all Core governance artifacts, the CAI Engine, regional overlays including CAI-USA, sector profiles, extensions, adapters, mappings, and any derived artifacts that claim lineage from CAI.

No change to CAI is considered authoritative unless it is recorded in the Evolution Traceability Register and approved through the Dual Audit Pipeline.

## Traceability Requirement

All framework evolution must be explicitly traceable.

Traceability includes the identification of what changed, why the change was made, who authorized it, which artifacts are affected, and how the change aligns with existing CAI principles and governance rules.

Implicit evolution, silent edits, inferred changes, or undocumented reinterpretation are prohibited.

## Minimum Traceability Elements

Each registered evolution entry must include, at minimum, the following information.

A unique change identifier.  
The date of the change.  
The affected document or artifact.  
The type of change, such as addition, clarification, correction, or deprecation.  
The rationale for the change.  
The governance authority approving the change.  
The technical review confirmation.  
The impact assessment on Core semantics, lifecycle, engine behavior, and sector profiles.  
A reference to the associated Git commit.

## Evolution Categories

CAI recognizes the following evolution categories.

Core semantic evolution affecting lifecycle meaning, principles, or authority.  
Architectural evolution affecting layers, boundaries, or execution semantics.  
Governance evolution affecting rules, controls, or audit mechanisms.  
Standards alignment evolution reflecting updates in referenced standards without altering Core meaning.  
Clarification or correction that does not change authoritative semantics.

Each category must be explicitly identified in the register entry.

## Governance Enforcement

No evolution entry may be added retroactively.

All changes must be recorded prior to or concurrently with publication.

Entries that lack approval, rationale, or traceability references invalidate the associated artifact until remediation is completed.

The Evolution Traceability Register is authoritative and supersedes informal documentation history.

## AI-Assisted Change Handling

Any evolution involving AI-assisted drafting, analysis, or synthesis must be explicitly marked as AI-assisted.

AI involvement does not reduce traceability requirements.

All AI-assisted changes require explicit human governance approval and technical validation before registration.

AI systems are not authorized to create, approve, or modify evolution entries autonomously.

## Relationship to Other Core Artifacts

This register operates in conjunction with CAI-Core-Integrity-and-Self-Defense-Governance.md, CAI-Core-Dual-Audit-Pipeline.md, CAI-Core-Contamination-Prevention-Rules.md, and CAI-Threat-Model-Framework-Integrity.md.

In case of conflict, Core Integrity governance prevails.

## Register Entries

Historical reconciliation record, recorded on 2026-10-15 (CHG-2026-10-15-01).

The register had no entries although the changes below had been published. These entries summarize changes that already exist in the Git history; they are a dated reconciliation, not retroactive approvals. Where no approval was recorded at the time, the entry says so. Each entry is verifiable against the cited commit.

AI tools were used for analysis, verification and preparation of changes. Every change listed was decided by the owner and committed under the owner's identity.

| Change ID | Date | Git commit | Affected artifacts | Category | Rationale | Approval | Technical review | Impact |
|---|---|---|---|---|---|---|---|---|
| Initial commit | 2026-10-11 | 9c28c3c | Whole framework and engine (373 files) | Addition | Initial publication of the framework and reference engine | Owner (author of the commit) | Not recorded | Baseline of record |
| No ID | 2026-10-11 | ed3c264 | README.md | Addition | Repository homepage | Committed by the owner; no separate approval record | Not recorded | None on Core semantics |
| No ID | 2026-10-11 | 3a115dc | eu_ai_act.py, governed_agent.py, REGULATORY-BASIS.md | Standards alignment | EU AI Act amended by Regulation (EU) 2026/1744 | Committed by the owner; no separate approval record | Not recorded | EU overlay and engine dates; no Core change |
| No ID | 2026-10-11 | 0c6fd35 | CAI-Engine tests | Addition | First engine test suite (23 tests) | Committed by the owner; no separate approval record | 23 tests in the commit | Engine verification; no behaviour change |
| No ID | 2026-10-11 | a4684af | METHODOLOGY.md | Addition | Unified methodology document | Committed by the owner; no separate approval record | Not applicable (document) | None on Core semantics |
| No ID | 2026-10-11 | fe1730d | AI-GOVERNANCE.md, CLAUDE.md, AGENTS.md | Governance | AI assistance and repository governance policy, proposed | Proposed; approved later in CHG-2026-10-11-02 | Not applicable (document) | Repository governance |
| CHG-2026-10-11-01 | 2026-10-11 | ce601a7 | mcp_server.py, engine README, tests, REGULATORY-BASIS.md | Correction | Audit ENG-01: AI self-approval tool removed from the MCP server; Art. 5 dates | Owner (commit message) | 24 passed | Engine 0.4.1; human approval only at the CLI |
| CHG-2026-10-11-02 | 2026-10-11 | 1622343 | LICENSE.md, AI-GOVERNANCE.md, CLAUDE.md, AGENTS.md, README.md | Governance | Audit LIC-04: evaluation exception (LICENSE 4A); AI policy approved | Owner, 2026-10-11 (commit message) | Not applicable (documents) | Licence revision 1.0.1 |
| CHG-2026-10-11-03 | 2026-10-11 | bcfabb0 | CAI-Core-Architecture.md, CAI-Core-Operations.md, one lab file | Correction | Audit CORE-04: duplicated copies removed | Owner choice of copy (commit message) | SHA-256 before and after in the commit message | None on Core semantics |
| CHG-2026-10-11-04 | 2026-10-11 | 7cb07f4 | 7 lab folders | Correction | Leading spaces removed from folder names | Committed by the owner; no separate approval record | Not recorded | None |
| CHG-2026-10-12-05 | 2026-10-11 | 5787056 | Core, USA and lab documents | Correction | File names, file-name references and a broken code block | Committed by the owner; no separate approval record | Not recorded | None on Core semantics |
| CHG-2026-10-12-06 | 2026-10-11 | f1e14d1 | tools/, .gitlab-ci.yml | Correction | Build script moved into tools/ | Committed by the owner; no separate approval record | Not recorded | None |
| CHG-2026-10-12-07 | 2026-10-11 | 64df086 | README.md, engine README, pyproject.toml, tests | Addition | Engine packaged and easy to install | Committed by the owner; no separate approval record | 25 passed on Python 3.11 to 3.13 | Engine packaging; no behaviour change |
| CHG-2026-10-12-08 | 2026-10-11 | bf76a46 | Engine sources and README | Clarification | Research-preview status; accurate evidence wording | Committed by the owner; no separate approval record | 25 passed | Engine 0.4.2 wording |
| CHG-2026-10-12-09 | 2026-10-11 | 64c0cc9 | Core Execution Model, Operational State Model, EU documents | Clarification | Owner decisions CORE-01, EU-01, EU-02 | Owner decision (commit message, signed) | Not applicable (documents) | Lifecycle stated as a derived branch; EU overlay marked planned |
| CHG-2026-10-12-10 | 2026-10-11 | b52935e | CAI-Core-Taxonomy.md | Core semantic evolution | CORE-02, CORE-03: DSA, ESA, decision integrity, D(t), context drift defined | Owner approved (commit message, signed) | Not applicable (document) | Taxonomy 0.1 to 0.2; terms already used elsewhere now defined |
| CHG-2026-10-12-11 | 2026-10-12 | 2d4a32f | Engine tests, pyproject.toml, tools/mutation-check.py | Addition | Specification test matrix and evidence contracts | Owner approved (commit message, signed) | 652 passed, 13 xfailed; mutation detection 79.2% | Engine verification; no behaviour change |
| CHG-2026-10-12-12 | 2026-10-13 | ccbc7b7 | README, Core Definition, Core Architecture, METHODOLOGY, engine README, LICENSE, legal notices | Clarification | AUD-01: MITRE D3FEND attributed as the source of the lifecycle stage names | Owner approved (commit message, signed) | 651 passed, 1 skipped, 13 xfailed | Core text states the source of the stage names; no semantic change; licence revision 1.0.2 |
| CHG-2026-10-12-13 | 2026-10-13 | 3e99748 | .github/workflows, README.md | Addition | AUD-09: tests run by GitHub Actions on every push | Owner approved (commit message, signed) | 6 of 6 jobs passed on GitHub | None on Core semantics |
| CHG-2026-10-13-01 | 2026-10-13 | fa6b110 | CAI-Engine/specifications/, README.md | Addition | Engine security specification published (proposed) | Owner approved (commit message, signed) | 652 passed, 13 xfailed | Specification only; engine unchanged |
| CHG-2026-10-15-01 | 2026-10-15 | This commit | CAI-Core-Evolution-Traceability-Register.md | Governance | AUD-18: register reconciled with the Git history | Owner approved (commit message, signed) | Not applicable (document) | Register in use from this entry |
| CHG-2026-10-15-02 | 2026-10-15 | This commit | 12 documents in docs/CORE (list in the commit message); tools/md-structure.py | Clarification or correction | AUD-02: Markdown structure added (headings, lists, line breaks); non-semantic formatting correction | Owner approved (commit message, signed) | Word sequence of each document verified identical before and after by tools/md-structure.py; 652 passed, 13 xfailed | None: no word added, removed or reordered |
| CHG-2026-10-15-03 | 2026-10-15 | This commit | 12 documents in CAI-Engine (list in the commit message) | Clarification or correction | AUD-02: Markdown structure added (headings, lists, line breaks); non-semantic formatting correction | Owner approved (commit message, signed) | Word sequence of each document verified identical before and after by tools/md-structure.py; 652 passed, 13 xfailed | None: no word added, removed or reordered |
| CHG-2026-10-16-01 | 2026-10-16 | This commit | 10 documents in docs/EU (list in the commit message) | Clarification or correction | AUD-02: Markdown structure added (headings, lists, line breaks); non-semantic formatting correction documented as such under CAI-EU-Master-Freeze-v0.1 section 3 | Owner approved (commit message, signed) | Word sequence of each document verified identical before and after by tools/md-structure.py; 652 passed, 13 xfailed | None: no word added, removed or reordered |
| CHG-2026-10-16-02 | 2026-10-16 | This commit | 15 documents in docs/USA (baseline, without sectors/) (list in the commit message) | Clarification or correction | AUD-02: Markdown structure added (headings, lists, line breaks); non-semantic formatting correction permitted by CAI-USA-Master-Freeze-v0.1 (formatting corrections that do not alter meaning) | Owner approved (commit message, signed) | Word sequence of each document verified identical before and after by tools/md-structure.py; 652 passed, 13 xfailed | None: no word added, removed or reordered |
| CHG-2026-10-16-03 | 2026-10-16 | This commit | 126 documents in docs/USA/sectors (list in the commit message) | Clarification or correction | AUD-02: Markdown structure added (headings, lists, line breaks); non-semantic formatting correction | Owner approved (commit message, signed) | Word sequence of each document verified identical before and after by tools/md-structure.py; 652 passed, 13 xfailed | None: no word added, removed or reordered |
| CHG-2026-10-16-04 | 2026-10-16 | This commit | 60 documents in labs/usa (list in the commit message) | Clarification or correction | AUD-02: Markdown structure added (headings, lists, line breaks); non-semantic formatting correction | Owner approved (commit message, signed) | Word sequence of each document verified identical before and after by tools/md-structure.py; 652 passed, 13 xfailed | None: no word added, removed or reordered |
| CHG-2026-10-16-05 | 2026-10-16 | This commit | 1 documents in labs/mexico (list in the commit message) | Clarification or correction | AUD-02: Markdown structure added (headings, lists, line breaks); non-semantic formatting correction | Owner approved (commit message, signed) | Word sequence of each document verified identical before and after by tools/md-structure.py; 652 passed, 13 xfailed | None: no word added, removed or reordered |
| CHG-2026-10-16-06 | 2026-10-16 | This commit | cai_engine (cli, core, engine, eu_ai_act, evidence, gates, usa), three test modules, pyproject.toml, .github/workflows/CAI-ENGINE-TESTS.yml | Clarification or correction | AUD-17: lint findings corrected; ruff rule set pinned in pyproject.toml; lint job added to GitHub Actions | Owner approved (commit message, signed) | ruff 0.16.8: 0 findings; 652 passed, 13 xfailed on Python 3.11, 3.12 and 3.13 | None on engine behaviour: unused imports and one unused variable removed, type annotations modernised, one boolean return simplified |
| CHG-2026-10-16-07 | 2026-10-16 | This commit | CAI-Engine/CAI-Engine-Telemetry-Ingestion-and-Normalization.md (renamed from a name with spaces), labs/mexico/README.md | Clarification or correction | AUD-15: file name without spaces; AUD-16: the missing number 21 in labs/mexico is recorded as not published | Owner approved (commit message, signed) | Renamed file content identical (same git blob); no file referred to the old name; 652 passed, 13 xfailed | Renamed file: none. labs/mexico/README.md: one sentence added; no document renumbered |
| CHG-2026-10-16-08 | 2026-10-16 | This commit | CAI-Core-Reference-Resolution-Record.md (new), docs/CORE/README.md, docs/USA/CAI-USA-CISA-ZT-Map.md, four documents in labs/usa/Government | Clarification or correction | AUD-04: references to documents that do not exist are resolved in a new record without editing frozen documents; one wrong document name corrected; the unpublished Government telemetry lab is marked as not published | Owner approved (commit message, signed) | Every cited CAI document name compared with the repository files; 652 passed, 13 xfailed | No frozen document modified. CAI-USA-CISA-ZT-Map: one document name corrected in two places. Government labs: "(not published)" added to four references |
| CHG-2026-10-16-09 | 2026-10-16 | This commit | docs/USA/CAI-USA-NIST-Map.md (new), docs/CORE/CAI-Core-Reference-Resolution-Record.md | Addition | AUD-03 phase 1: item-by-item map of CAI to NIST SP 800-53 Rev. 5 (28 selected controls), CSF 2.0 (106 subcategories), AI RMF 1.0 (72 subcategories) and SP 800-207 (7 tenets and logical components), each with status and repository evidence | Owner approved (commit message, signed) | Identifiers and statements checked against the NIST OSCAL catalogs (SP 800-53 5.2.0, CSF 2.0 1.2.0) and NIST publications; every cited test exists; independent review before commit; 652 passed, 13 xfailed | No existing document changed in meaning; the record entry for CAI-USA-NIST-Map now points to the written document |
| CHG-2026-10-16-10 | 2026-10-16 | This commit | 27 documents in labs/mexico, README.md, docs/USA/sectors/README.md | Clarification or correction | AUD-10: framework name unified in labs/mexico; AUD-11: sector coverage stated without changing frozen sector profiles; AUD-13: three overstated statements corrected | Owner approved (commit message, signed) | 27 occurrences of the old expansion replaced, 0 left; sector list checked against usa_sectors.py; 652 passed, 13 xfailed | labs/mexico: only the expansion of CAI changes, plus two sentences of the README replaced; README.md: two statements narrowed to what the engine does; docs/USA/sectors/README.md: one section added. No frozen document modified |
| CHG-2026-10-16-11 | 2026-10-16 | This commit | docs/USA/sector-frameworks/ (README and five sector documents, new), CAI-Engine/implementation/examples/sectors/ (10 examples, new), tests/TEST_SECTOR_EXAMPLES.py (new), .github/workflows/CAI-ENGINE-TESTS.yml, docs/USA/sectors/README.md | Addition | AUD-05 batch 1: frameworks that apply to the Chemical, Commercial Facilities, Communications, Critical Manufacturing and Dams sectors, the decision-time controls CAI adds, and worked examples checked by tests | Owner approved (commit message, signed) | Regulatory facts checked against official sources on 2026-10-16; independent review before commit; example outcomes and document tables checked by tests; 664 passed, 13 xfailed; CI gate raised from 652 to 664 | No frozen document modified; engine unchanged |
| CHG-2026-10-16-12 | 2026-10-16 | This commit | docs/USA/sector-frameworks/ (five new sector documents; README; the five batch 1 documents corrected), CAI-Engine/implementation/examples/sectors/ (10 new examples), tests/TEST_SECTOR_EXAMPLES.py, .github/workflows/CAI-ENGINE-TESTS.yml | Addition | AUD-05 batch 2: Defense Industrial Base, Emergency Services, Energy, Financial Services, Food and Agriculture; correction of the OT gate wording in batch 1 | Owner approved (commit message, signed) | Regulatory facts checked against official sources on 2026-10-16; independent review before commit; documents checked against the examples (state, outcome, gates); 674 passed, 13 xfailed; CI gate raised from 664 to 674 | No frozen document modified; engine unchanged; batch 1 documents: description of when the OT gates apply corrected to match the code |

From CHG-2026-10-15-01 onward, each change adds its entry in the same commit that makes the change.


## Owner-adjudicated reconciliation — CHG-CAI-GOV-RECON-2026-10-23

This is a contemporaneous local change record, not a retroactive approval of
earlier changes. The historical entries and freeze statement below are retained.

| Element | Recorded value |
| --- | --- |
| Change ID | CHG-CAI-GOV-RECON-2026-10-23 |
| Recorded project date | 2026-10-23, client project date (Etc/GMT+5) |
| Human adjudication source | The project owner's message “Aprbado” approving the three reconciliation criteria after the Cleanup 1.1.1 applied checkpoint in the project conversation |
| Scope approved | Conflict handling between integrity and contamination; research-preview completeness wording; citation guidance aligned with existing LICENSE.md permissions/restrictions |
| Affected documents | CAI-Core-Integrity-and-Self-Defense-Governance.md; CAI-Core-Contamination-Prevention-Rules.md; CAI-Core-Completeness-and-Scope.md; legal/CAI-Attribution-and-Citation-Guidelines.md; this register |
| Category | Bounded governance reconciliation and correction of completeness/attribution wording |
| Source baseline | Cleanup 1.1.1 locally applied, as reported by the owner; branch review/chg-cai-gllm-gov-001 and HEAD 4b13e165182f106563d686c2d4e2a67cdec4f4c7 are the installer locks |
| Document revisions | Core documents/register: revision 0.1.1 under framework baseline v0.1; citation guide: version 1.2; no framework or engine release increment |
| Technical review | Separate technical criteria and document/installer fixture evidence in CAI-Governance-Reconciliation-1.0.0; actual installation outcome is established by the run's result.json and postimage hashes |
| Governance review | Owner adjudicated the criteria; assistant reviewed source alignment and bounded scope. These checks are not independent IV&V or a claim of completed publication review |
| AI assistance | ChatGPT prepared wording, traceability, tests and controlled installer; no AI author/coauthor or approval authority is created |
| Evidence package | CAI-Governance-Reconciliation-1.0.0: manifest.json, REVIEW.patch, review records, fixture results and run receipts; no historical result is rewritten |
| CORE impact | A direct integrity/contamination conflict places the affected change on HOLD for the designated human authority; no inferred precedence. Completeness remains under review |
| Implementation / legal impact | Lifecycle, engine, thresholds, jurisdiction profiles and LICENSE.md unchanged; no new permission, certification or implementation guarantee |
| Commit reference | PENDING — no commit is created by this installation; the owner-authorized publication process must supply its commit reference before authoritative publication |
| Acceptance boundary | Approval of these criteria authorizes this bounded local reconciliation, not publication, promotion to 1.0 or completion of independent assurance. Final promotion remains HOLD |

The historical freeze is not a blanket authorization to revise other CORE
artifacts. This entry records only the specific owner-adjudicated reconciliation
above, preserves the v0.1 research-preview baseline, and does not unlock unrelated
semantics, regional overlays or future changes. The seven known engine expected
failures remain open. The full local GOV-001 content has not been independently
captured in this preparation; this remains a promotion-review limitation.

Status  

Status: Draft – Evolution Traceability Register Established  

This document establishes the mandatory and authoritative mechanism for governing the evolution of the CAI framework and is required for all future changes.  
Freeze CAI Core v0.1 – Integrity, Governance, and Evolution Locked  
End of Document