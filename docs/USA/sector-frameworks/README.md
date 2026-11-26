# CAI-USA Sector Framework Application

Cybersecurity Artificial Intelligence Framework – Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This directory maps, sector by sector, the cybersecurity frameworks that apply in the United States and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

The frozen profiles under docs/USA/sectors remain unchanged. This directory now has a draft application profile for each of the 16 NSM-22 sectors and a separate aviation reference profile (aviation is part of Transportation Systems, not a seventeenth NSM-22 sector). These documents are engineering review aids, not determinations of which laws, regulations, or contracts apply to a particular entity. Each profile:

1. states the sector's regulator, Sector Risk Management Agency and the engine parameters CAI applies to it;
2. lists the frameworks that apply, with their type (binding, contractual, incentive, voluntary), scope, status on the date of verification and official source;
3. states what CAI adds to those frameworks at decision time, and how much of it is implemented;
4. shows worked examples whose outcomes are produced by the engine and checked by the test suite;
5. states the gaps.

The documents do not modify the frozen profiles. Their existence closes only a documentation-presence gap; it does not establish complete sector analysis, implementation, control effectiveness, or compliance.

## 2. What CAI adds to sector frameworks

Binding sector frameworks say what an entity must protect, plan, monitor and report, and some control changes before they are made (for example management of change under OSHA PSM, 29 CFR 1910.119(l)). In the binding frameworks reviewed in this directory, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to: the joint guidance Principles for the Secure Integration of Artificial Intelligence in Operational Technology (December 2025, co-authored by CISA) asks, among other things, to keep operators in decisions on critical OT actions. CAI proposes a decision-time control layer that enforces this kind of principle for each proposed action:

Table 1 — Decision-time controls CAI applies in every sector.

| Control | Engine element | Status |
|---|---|---|
| Reference decision thresholds and caller-declared model metadata | `usa.py` gates `usa.assurance_floor`, `usa.robustness`, `usa.nist_ai_600_1` | Present in reference logic; threshold calibration, trusted provenance, and effectiveness are not established |
| Human review signal for proposals classified as critical infrastructure | `usa.srma_oversight`; MCP server has no approval tool | Present in reference decision path; sector, target, and approver are not independently authenticated |
| Cyber-physical escalation based on sector/action labels and declared Purdue level | `usa.ot_ics_safety`, `safety.ot_ics` | Present in reference logic; no trusted asset inventory, safety case, or external enforcement boundary |
| Lifecycle discipline: each action category is permitted only in its lifecycle state (for example, eradication only in EVICT) | `policy.state_constraint` | Implemented |
| Local decision record with gate results and reasons | `evidence.py` | Local hash-chain only; completeness and authenticity need independent anchoring |
| Decision integrity over time: revalidation at approval and before dispatch; environmental state from signed sources | CAI-ENG-SEC-001 Core SR-06 to SR-11, SR-13 | Specified |

Status values are those of CAI-USA-NIST-Map section 3.

## 3. Method

- The previous legal/status research snapshot is dated 2026-10-16. It is not a current legal applicability opinion. Before publication or use, recheck the current primary source, effective date, covered entity/asset, contract scope, and reviewer disposition; mark unknown applicability `NOT VERIFIED`. Statements marked "CAI reading" are project interpretations.
- Engine parameters in each document are read from `CAI-Engine/implementation/cai_engine/usa_sectors.py` and `usa.py`.
- Worked examples are JSON files in `CAI-Engine/implementation/examples/sectors/`. Each holds a synthetic proposal, the lifecycle state in which it is evaluated and the expected engine outcome. `tests/TEST_SECTOR_EXAMPLES.py` evaluates every example on each test run and fails if an outcome changes; it also checks that the lifecycle state, outcome and gates written in each sector document equal those in the example file. To run them: `python -m pytest -q tests/TEST_SECTOR_EXAMPLES.py` from `CAI-Engine/implementation`.
- Regulations change. Each document states its verification date; a status change is recorded by updating the document in a registered change.

## 4. Cross-sector baseline (status on 2026-10-16)

Table 2 — Frameworks and policies that apply across sectors.

| Item | Status | Source |
|---|---|---|
| NSM-22, Critical Infrastructure Security and Resilience (30 April 2024) | Replaced PPD-21. Executive Order 14239 (18 March 2025), section 3(b), ordered a review of critical infrastructure policy, including NSM-22. No replacement was found as of 2026-10-16; NSPM-12 (12 June 2026) rescinds NSD-42 and NSM-8, not NSM-22. Treated as in force and under review. | https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/national-security-memorandum-critical-infrastructure-security-and-resilience; https://www.federalregister.gov/documents/full_text/html/2025/03/21/2025-04973.html; https://www.whitehouse.gov/presidential-actions/2026/06/national-security-presidential-memorandum-nspm-12/ |
| CIRCIA, 6 U.S.C. 681 et seq. | Proposed rule published 4 April 2024 (89 FR 23644): covered entities would report substantial cyber incidents within 72 hours and ransom payments within 24 hours. The final rule (RIN 1670-AA04) was under OIRA review from 1 October 2026 and not published as of 2026-10-16. | https://www.govinfo.gov/content/pkg/FR-2024-04-04/pdf/2024-06526.pdf; https://www.reginfo.gov/public/do/eoDetails?rrid=1550967 |
| CISA Cross-Sector Cybersecurity Performance Goals 2.0 | Published 11 December 2025; voluntary; covers IT and OT | https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure |
| NIST Cybersecurity Framework 2.0 (CSWP 29) | Published 26 February 2024; voluntary; mapped item by item in CAI-USA-NIST-Map | https://www.nist.gov/cyberframework |
| NIST SP 800-82 Rev. 3, Guide to Operational Technology Security | Published September 2023; Rev. 4 initial public draft released 21 September 2026, comments until 30 November 2026 | https://csrc.nist.gov/pubs/sp/800/82/r3/final; https://csrc.nist.gov/pubs/sp/800/82/r4/ipd |
| Principles for the Secure Integration of Artificial Intelligence in Operational Technology (joint guidance, CISA and partners) | Published 3 December 2025; voluntary; addresses AI in OT, including keeping operators in decisions on critical OT actions | https://www.cyber.gov.au/sites/default/files/2025-12/principles-for-the-secure-integration-of-artificial-intelligence-in-operational-technology.pdf |

## 5. Documents

Table 3 — Sector documents in this directory.

| Sector (NSM-22) | Document | Status |
|---|---|---|
| Chemical | CAI-USA-Chemical-Framework-Application.md | Batch 1 |
| Commercial Facilities | CAI-USA-Commercial-Facilities-Framework-Application.md | Batch 1 |
| Communications | CAI-USA-Communications-Framework-Application.md | Batch 1 |
| Critical Manufacturing | CAI-USA-Critical-Manufacturing-Framework-Application.md | Batch 1 |
| Dams | CAI-USA-Dams-Framework-Application.md | Batch 1 |
| Defense Industrial Base | CAI-USA-Defense-Industrial-Base-Framework-Application.md | Batch 2 |
| Emergency Services | CAI-USA-Emergency-Services-Framework-Application.md | Batch 2 |
| Energy | CAI-USA-Energy-Framework-Application.md | Batch 2 |
| Financial Services | CAI-USA-Financial-Services-Framework-Application.md | Batch 2 |
| Food and Agriculture | CAI-USA-Food-and-Agriculture-Framework-Application.md | Batch 2 |
| Government Facilities | CAI-USA-Government-Facilities-Framework-Application.md | Batch 3 (draft) |
| Healthcare and Public Health | CAI-USA-Healthcare-Framework-Application.md | Batch 3 (draft) |
| Information Technology | CAI-USA-Information-Technology-Framework-Application.md | Batch 3 (draft) |
| Nuclear Reactors, Materials, and Waste | CAI-USA-Nuclear-Framework-Application.md | Batch 3 (draft) |
| Transportation Systems | CAI-USA-Transportation-Framework-Application.md | Batch 3 (draft) |
| Water and Wastewater Systems | CAI-USA-Water-Framework-Application.md | Batch 3 (draft) |

## 6. Relationship to Other CAI Documents

- CAI-USA-Definition
- CAI-USA-NIST-Map
- docs/USA/sectors (frozen sector profiles) and its README, section Sector Coverage
- CAI-Engine/specifications/CAI-ENG-SEC-001-Core.md and CAI-ENG-SEC-001-USA.md

## Status

Status: Draft – 16/16 NSM-22 profile documents; source applicability, sector evidence, and implementation validation remain open
End of Document
