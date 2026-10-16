# CAI-USA-Critical-Manufacturing-Framework-Application

Cybersecurity Artificial Intelligence Framework – Critical Manufacturing Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Critical Manufacturing sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Critical Manufacturing sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: DHS (CISA). Core industries listed by CISA: Primary Metals; Machinery; Electrical Equipment, Appliance and Component; Transportation Equipment. No regulation covers the whole sector; defense suppliers and vehicle manufacturers have specific obligations. Production runs on industrial control systems (NIST SP 800-82 Rev. 3).

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `critical_manufacturing` |
| Sector name | Critical Manufacturing |
| SRMA as recorded by the engine | CISA (DHS) |
| Consequence level | HIGH |
| OT-intensive | Yes |
| AI confidence floor (usa.assurance_floor) | 0.90 |
| Maximum declared drift (usa.robustness) | 0.15 |
| Human oversight (usa.srma_oversight) | Every governed proposal escalates to a human |
| OT safety approval (usa.ot_ics_safety) | Applies to OT-level, destructive, containment and eradication actions |

## 3. Applicable frameworks

Type: Binding (law or regulation, for the entities in scope), Contractual, Incentive, Voluntary. Status is as verified on 2026-10-16 in the source given.

Table 2 — Frameworks that apply to the sector or to parts of it.

| Framework | Type | Scope in this sector | Status on 2026-10-16 | Source |
|---|---|---|---|---|
| DFARS 252.204-7012 | Binding | Defense suppliers handling covered defense information (CUI) | In force; requires NIST SP 800-171 Rev. 2 and cyber incident reporting to DoD within 72 hours | https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012 |
| CMMC program rule, 32 CFR Part 170; DFARS CMMC contract rule (DFARS Case 2019-D041) | Binding | DoD contractors and subcontractors | Program rule effective 16 December 2024; contract rule published 10 September 2025 (90 FR 43560), effective 10 November 2025 (Phase 1, self-assessments); Phase 2 (third-party assessments) suspended by DoD on 13 July 2026, as reported by the SBA Office of Advocacy | https://www.govinfo.gov/content/pkg/FR-2025-09-10/html/2025-17359.htm; https://advocacy.sba.gov/?p=36257 |
| BIS connected-vehicle rule, 15 CFR Part 791 subpart D | Binding | Passenger vehicles under 10,001 lb with connected hardware or software | Effective 17 March 2025; software prohibitions from model year 2027, hardware from model year 2030. A supply-chain rule, not a controls rule | https://www.federalregister.gov/documents/2025/01/16/2025-00592/securing-the-information-and-communications-technology-and-services-supply-chain-connected-vehicles |
| FAR CUI clause (FAR 52.240-7, proposed) | Proposed | Federal contractors handling CUI | Proposed within the Revolutionary FAR Overhaul (91 FR 37550, 23 June 2026); not final | https://www.federalregister.gov/documents/2026/06/23/2026-12559/federal-acquisition-regulation-revolutionary-federal-acquisition-regulation-overhaul-parts-1-2-4-33 |
| NHTSA Cybersecurity Best Practices for the Safety of Modern Vehicles (2022) | Voluntary | Vehicle manufacturers | Non-binding | https://www.nhtsa.gov/press-releases/nhtsa-updates-cybersecurity-best-practices-new-vehicles |
| UN Regulation No. 155 (vehicle cybersecurity management system) | Binding outside the U.S. | U.S. manufacturers exporting to markets that apply it | Not U.S. law | https://treaties.un.org/doc/Publication/CN/2022/CN.366.2022-Eng.pdf |
| NIST CSF 2.0 Manufacturing Profile (NIST IR 8183 Rev. 2) | Voluntary | Manufacturers | Initial public draft of 29 September 2025; no final version found | https://csrc.nist.gov/News/2025/csf-2-0-manufacturing-profile-initial-draft |
| CISA Cross-Sector CPGs 2.0; NIST SP 800-82 Rev. 3; ISA/IEC 62443 series | Voluntary | All | Current; ISA/IEC 62443 is a consensus standard | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. None of them sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Safe operation of production OT (SP 800-82, ISA/IEC 62443) | An AI-proposed action on a PLC cell at Purdue level 0 to 2 is escalated twice, by the sector OT gate and by the CAI gate safety.ot_ics, and cannot execute without a human. | Implemented |
| Generative AI in engineering and operations (NIST AI 600-1) | A generative AI proposal without provenance or explanation is denied. | Implemented |
| Cyber incident reporting within 72 hours (DFARS 252.204-7012) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Protection of CUI (NIST SP 800-171, CMMC) | Not addressed: CAI does not implement CUI safeguarding requirements. | Not addressed |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `critical_manufacturing-1.json` | A model proposes isolating a PLC cell (Purdue level 1) on a production line; confidence 0.96. | ISOLATE | CONTAINMENT, Purdue level 1 | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |
| `critical_manufacturing-2.json` | A generative AI assistant proposes the same action without provenance. | ISOLATE | CONTAINMENT, Purdue level 1 | BLOCKED (DENY) | usa.nist_ai_600_1 = DENY; usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: OT-level, destructive, containment or eradication action needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- The CMMC phase-in after the July 2026 suspension and the outcome of the DoD reform review were not published by 2026-10-16.

## 7. Sources

- CISA Critical Manufacturing Sector: https://www.cisa.gov/critical-manufacturing-sector
- DFARS 252.204-7012 (eCFR): https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012
- DFARS CMMC rule (90 FR 43560): https://www.govinfo.gov/content/pkg/FR-2025-09-10/html/2025-17359.htm
- SBA Office of Advocacy on the CMMC Phase 2 suspension: https://advocacy.sba.gov/?p=36257
- BIS connected vehicles rule: https://www.federalregister.gov/documents/2025/01/16/2025-00592/securing-the-information-and-communications-technology-and-services-supply-chain-connected-vehicles
- FAR overhaul proposed rule (91 FR 37550): https://www.federalregister.gov/documents/2026/06/23/2026-12559/federal-acquisition-regulation-revolutionary-federal-acquisition-regulation-overhaul-parts-1-2-4-33
- NHTSA best practices: https://www.nhtsa.gov/press-releases/nhtsa-updates-cybersecurity-best-practices-new-vehicles
- NIST IR 8183 Rev. 2 draft: https://csrc.nist.gov/News/2025/csf-2-0-manufacturing-profile-initial-draft
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure
- NIST SP 800-82 Rev. 3, Guide to Operational Technology Security (September 2023): https://csrc.nist.gov/pubs/sp/800/82/r3/final

## Status

Status: Draft – sector framework application, batch 1
End of Document
