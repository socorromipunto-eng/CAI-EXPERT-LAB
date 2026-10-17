# CAI-USA-Defense-Industrial-Base-Framework-Application

Cybersecurity Artificial Intelligence Framework – Defense Industrial Base Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Defense Industrial Base sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Defense Industrial Base sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: the Department of Defense (now styled Department of War in official pages). The sector covers more than 100,000 companies and their subcontractors that design, produce, deliver and maintain military weapons systems, subsystems and components (CISA). Obligations come mainly through contract clauses (DFARS, FAR) and, for cleared contractors, the NISPOM. Production lines run on industrial control systems; the DoD DIB Cybersecurity Strategy 2024 sets an objective on the cyber resiliency of critical DIB production capabilities.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `defense_industrial_base` |
| Sector name | Defense Industrial Base |
| SRMA as recorded by the engine | Department of Defense |
| Consequence level | HIGH |
| OT-intensive | Yes |
| AI confidence floor (usa.assurance_floor) | 0.90 |
| Maximum declared drift (usa.robustness) | 0.15 |
| Human oversight (usa.srma_oversight) | Every governed proposal escalates to a human |
| OT safety approval (usa.ot_ics_safety) | Applies to any action on an asset with a Purdue level and to any destructive, containment or eradication action |

## 3. Applicable frameworks

Type: Binding (law or regulation, for the entities in scope), Contractual, Incentive, Voluntary. Status is as verified on 2026-10-16 in the source given.

Table 2 — Frameworks that apply to the sector or to parts of it.

| Framework | Type | Scope in this sector | Status on 2026-10-16 | Source |
|---|---|---|---|---|
| DFARS 252.204-7012, Safeguarding Covered Defense Information and Cyber Incident Reporting | Binding (contract) | Contractors with covered defense information | In force (May 2024 clause): NIST SP 800-171 in effect when the solicitation is issued or as authorized by the contracting officer (DoD applies Rev. 2 through a class deviation); cyber incident report within 72 hours of discovery through dibnet.dod.mil | https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting |
| DFARS 252.204-7019, -7020 (NIST SP 800-171 DoD assessments) and -7021 (CMMC) | Binding (contract) | DoD contractors and subcontractors | In force; assessment scores in SPRS; -7021 (November 2025) requires CMMC status and an annual affirmation | https://www.acquisition.gov/dfars/252.204-7021-contractor-compliance-cybersecurity-maturity-model-certification-level-requirements |
| CMMC program (32 CFR Part 170) and phase-in | Binding (contract) | DoD contractors and subcontractors | Phase 1 (self-assessments) in effect since 10 November 2025; Phase 2 (third-party assessments, planned for 10 November 2026 under 32 CFR 170) suspended on 13 July 2026 pending a reform review by a task force with a 60-day mandate; no decision found by 2026-10-16 | https://www.war.gov/News/News-Stories/Article/Article/4542849/war-department-changes-cybersecurity-maturity-model-certification-requirements/ |
| FAR 52.204-21, Basic Safeguarding of Covered Contractor Information Systems | Binding (contract) | Federal contractors with federal contract information | In force (15 basic safeguarding requirements) | https://www.acquisition.gov/far/52.204-21 |
| FAR 52.204-25 (Section 889), prohibition on certain telecommunications and video surveillance equipment | Binding (contract) | Federal contractors | In force; report covered equipment within 1 business day | https://www.acquisition.gov/far/52.204-25 |
| NISPOM, 32 CFR Part 117 | Binding | Cleared contractors; section 117.8(f) applies to cleared defense contractors | In force; cyber incidents on classified systems are reported immediately to the DoD Cognizant Security Office (section 117.8(f)) | https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-D/part-117 |
| DIB Cybersecurity Program, 32 CFR Part 236 | Voluntary | Eligible cleared defense contractors | In force as a voluntary information-sharing program | https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-M/part-236 |
| NSA Cybersecurity Collaboration Center DIB services | Voluntary | Companies with an active DoD contract or access to non-public DoD information | Free services (protective DNS, attack surface management, threat intelligence) | https://www.nsa.gov/about/cybersecurity-collaboration-center/dib-cybersecurity-services/ |
| DoD DIB Cybersecurity Strategy (FY2024 to FY2027) | Policy | DoD and the DIB | Published March 2024 | https://dodcio.defense.gov/Portals/0/Documents/Library/DIB-CS-Strategy.pdf |
| NSPM-11, Artificial Intelligence in the National Security Enterprise | Policy | National security agencies; contractors through contracts | Signed 5 June 2026; replaces NSM-25 and orders an update of DoD Directive 3000.09 | https://www.whitehouse.gov/presidential-actions/2026/06/national-security-presidential-memorandum-nspm-11/ |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Resiliency of critical production capabilities (DIB Cybersecurity Strategy, objective 3.1) | An AI-proposed containment, eradication or destructive action on a production controller at Purdue level 0 to 2 is escalated by the sector OT gate and by safety.ot_ics and cannot execute without a human. | Implemented |
| Assurance for AI proposals in operations (no binding framework reviewed sets runtime gates) | AI proposals below confidence 0.90 or with drift above 0.15 are denied; generative AI without provenance or explanation is denied; every proposal escalates to a human. | Implemented |
| Cyber incident reporting within 72 hours (DFARS 252.204-7012) and immediate reporting (NISPOM) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Protection of covered defense information (NIST SP 800-171, CMMC) | Not addressed: CAI does not implement CUI safeguarding requirements. | Not addressed |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `defense_industrial_base-1.json` | A model proposes isolating a compromised production-line controller (Purdue level 2) at a defense supplier; confidence 0.93. | ISOLATE | CONTAINMENT, Purdue level 2 | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |
| `defense_industrial_base-2.json` | The same proposal with confidence 0.88, below the HIGH floor of 0.90. | ISOLATE | CONTAINMENT, Purdue level 2 | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; usa.assurance_floor = DENY; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- Under the April 2024 CIRCIA proposal, an entity required to report under DFARS 252.204-7012 is a covered entity (proposed section 226.2(b)(4)); the final rule may differ.
- The CMMC phase-in after the July 2026 suspension was not decided by 2026-10-16.

## 7. Sources

- CISA Defense Industrial Base Sector: https://www.cisa.gov/defense-industrial-base-sector
- DFARS 252.204-7012: https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting
- DFARS 252.204-7021: https://www.acquisition.gov/dfars/252.204-7021-contractor-compliance-cybersecurity-maturity-model-certification-level-requirements
- Department of War, CMMC changes (July 2026): https://www.war.gov/News/News-Stories/Article/Article/4542849/war-department-changes-cybersecurity-maturity-model-certification-requirements/
- FAR 52.204-21: https://www.acquisition.gov/far/52.204-21
- FAR 52.204-25: https://www.acquisition.gov/far/52.204-25
- 32 CFR Part 117: https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-D/part-117
- 32 CFR Part 236: https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-M/part-236
- NSA DIB cybersecurity services: https://www.nsa.gov/about/cybersecurity-collaboration-center/dib-cybersecurity-services/
- DIB Cybersecurity Strategy 2024: https://dodcio.defense.gov/Portals/0/Documents/Library/DIB-CS-Strategy.pdf
- NSPM-11: https://www.whitehouse.gov/presidential-actions/2026/06/national-security-presidential-memorandum-nspm-11/
- CIRCIA proposed rule covered-entity infographic: https://www.cisa.gov/sites/default/files/2024-05/24-0630-Covered-Entity-Infographic-04242024-508c.pdf
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure
- NIST SP 800-82 Rev. 3, Guide to Operational Technology Security (September 2023): https://csrc.nist.gov/pubs/sp/800/82/r3/final

## Status

Status: Draft – sector framework application, batch 2
End of Document
