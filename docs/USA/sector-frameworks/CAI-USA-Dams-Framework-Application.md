# CAI-USA-Dams-Framework-Application

Cybersecurity Artificial Intelligence Framework – Dams Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Dams sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Dams sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: DHS, with CISA leading the Dams Sector Management Team. Obligations depend on the owner: FERC-licensed non-federal hydropower, hydro units registered in the bulk electric system (NERC CIP), and federal owners (USACE, Bureau of Reclamation, TVA) under FISMA. SCADA controls release gates, valves and generating units. This sector has no profile in docs/USA/sectors (see the Sector Coverage section of docs/USA/sectors/README.md); this document is its only sector-level CAI document.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `dams` |
| Sector name | Dams |
| SRMA as recorded by the engine | CISA (DHS) |
| Consequence level | CATASTROPHIC |
| OT-intensive | Yes |
| AI confidence floor (usa.assurance_floor) | 0.95 |
| Maximum declared drift (usa.robustness) | 0.15 |
| Human oversight (usa.srma_oversight) | Every governed proposal escalates to a human |
| OT safety approval (usa.ot_ics_safety) | Applies to any action on an asset with a Purdue level and to any destructive, containment or eradication action |

## 3. Applicable frameworks

Type: Binding (law or regulation, for the entities in scope), Contractual, Incentive, Voluntary. Status is as verified on 2026-10-16 in the source given.

Table 2 — Frameworks that apply to the sector or to parts of it.

| Framework | Type | Scope in this sector | Status on 2026-10-16 | Source |
|---|---|---|---|---|
| FERC dam safety regulations, 18 CFR Part 12 (Order No. 880) | Binding | FERC-licensed non-federal hydropower projects | Effective 11 April 2022; dam safety, no cybersecurity requirements | https://www.federalregister.gov/documents/2022/01/11/2021-27736/safety-of-water-power-projects-and-project-works |
| FERC Security Program for Hydropower Projects, Revision 3A | Binding in part | FERC-licensed projects | Annual Security Compliance Certification, including cyber asset designation, is an annual requirement; other parts are voluntary. Draft revised cyber guidance (Section 9.0, Docket AD26-6-000) issued for comment on 22 April 2026, comments closed 18 May 2026; no final version found | https://ferc.gov/dam-safety-and-inspections/security-program-hydropower-projects; https://www.federalregister.gov/documents/2026/04/22/2026-07837/notice-of-availability-of-the-draft-section-90-security-program-for-hydropower-guidance-and-request |
| NERC CIP reliability standards (CIP-002 to CIP-015) | Binding | Hydro generator owners and operators with bulk electric system facilities | In force, with versions changing from 2026 to 2029: CIP-002-8 approved on 19 March 2026; CIP-003-11 (low impact systems) approved by Order No. 918 on 19 March 2026; CIP-015-1 (internal network security monitoring, high and medium impact systems) approved by Order No. 907 on 26 June 2025 | https://public-inspection.federalregister.gov/2026-05715.pdf; https://public-inspection.federalregister.gov/2026-05711.pdf; https://public-inspection.federalregister.gov/2025-12309.pdf |
| FISMA, 44 U.S.C. 3551 et seq.; NIST SP 800-53 Rev. 5 | Binding | Federal dam owners and operators | In force | https://csrc.nist.gov/projects/risk-management/fisma-background |
| Dams Sector Cybersecurity Capability Maturity Model (2022) and implementation guide | Voluntary | Dam owners and operators | Current CISA publication | https://www.cisa.gov/sites/default/files/2023-01/dams-c2m2-2022-508.pdf |
| Dams Sector Cybersecurity Framework Implementation Guidance (CISA) | Voluntary | Dam owners and operators | Current CISA publication | https://www.cisa.gov/sites/default/files/publications/Dams_Sector_Cybersecurity_Framework_Implementation_Guidance_FINAL_508.pdf |
| CISA Cross-Sector CPGs 2.0; NIST SP 800-82 Rev. 3 | Voluntary | All | Current | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Control of gates, valves and generating units (SP 800-82, Dams C2M2) | An AI-proposed containment, eradication or destructive action on spillway SCADA at Purdue level 0 to 2 is escalated by the sector OT gate and by safety.ot_ics; it cannot execute without a human. | Implemented |
| Assurance for a CATASTROPHIC-consequence sector | AI proposals below confidence 0.95 or with drift above 0.15 are denied. | Implemented |
| Incident reporting (NERC CIP-008; CIRCIA when final) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Internal network security monitoring (NERC CIP-015) | Not addressed: telemetry is ingested and validated but does not enter decisions (xfail AUD-07). | Not addressed |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `dams-1.json` | A model proposes isolating the SCADA link to spillway gate controllers (Purdue level 1); confidence 0.98. | ISOLATE | CONTAINMENT, Purdue level 1 | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |
| `dams-2.json` | The same proposal with confidence 0.94, below the CATASTROPHIC floor of 0.95. | ISOLATE | CONTAINMENT, Purdue level 1 | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; usa.assurance_floor = DENY; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- Under the April 2024 CIRCIA proposal there is no Dams-specific criterion; dam owners would be covered through the size test or another criterion. The final rule may differ.

## 7. Sources

- CISA Dams Sector: https://www.cisa.gov/dams-sector
- FERC Order No. 880: https://www.federalregister.gov/documents/2022/01/11/2021-27736/safety-of-water-power-projects-and-project-works
- FERC Security Program for Hydropower Projects: https://ferc.gov/dam-safety-and-inspections/security-program-hydropower-projects
- FERC draft Section 9.0 guidance notice: https://www.federalregister.gov/documents/2026/04/22/2026-07837/notice-of-availability-of-the-draft-section-90-security-program-for-hydropower-guidance-and-request
- FERC approval of CIP-002-8: https://public-inspection.federalregister.gov/2026-05715.pdf
- NIST FISMA background: https://csrc.nist.gov/projects/risk-management/fisma-background
- Dams Sector C2M2 (2022): https://www.cisa.gov/sites/default/files/2023-01/dams-c2m2-2022-508.pdf
- FERC Order No. 918: https://public-inspection.federalregister.gov/2026-05711.pdf
- FERC Order No. 907: https://public-inspection.federalregister.gov/2025-12309.pdf
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure
- NIST SP 800-82 Rev. 3, Guide to Operational Technology Security (September 2023): https://csrc.nist.gov/pubs/sp/800/82/r3/final

## Status

Status: Draft – sector framework application, batch 1
End of Document
