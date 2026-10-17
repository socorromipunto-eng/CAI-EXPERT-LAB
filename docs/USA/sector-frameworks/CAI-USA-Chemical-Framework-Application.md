# CAI-USA-Chemical-Framework-Application

Cybersecurity Artificial Intelligence Framework – Chemical Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Chemical sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Chemical sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: DHS, acting through CISA (CISA Chemical SRMA fact sheet, August 2025). The sector operates processes run by distributed control systems, PLCs, SCADA and safety instrumented systems, which NIST SP 800-82 Rev. 3 covers. Since the statutory authority of CFATS lapsed in July 2023, no federal cybersecurity performance standard applies to most chemical facilities; the USCG cybersecurity rule applies to chemical facilities regulated under the Maritime Transportation Security Act.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `chemical` |
| Sector name | Chemical |
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
| Chemical Facility Anti-Terrorism Standards (CFATS), 6 CFR Part 27, including RBPS 8 (Cyber) | Lapsed (not enforceable) | High-risk chemical facilities | Statutory authority expired on 28 July 2023 and was not reauthorized; CISA cannot enforce the program. The rule text remains in the CFR. | CRS R48878 (10 March 2026): https://www.congress.gov/crs-product/R48878; GAO-26-108127: https://www.gao.gov/products/gao-26-108127 |
| USCG, Cybersecurity in the Marine Transportation System, 33 CFR Part 101 subpart F | Binding | Chemical facilities regulated under MTSA (33 CFR Part 105) | Final rule published 17 January 2025, effective 16 July 2025; cybersecurity assessment and plan due within 24 months of the effective date | https://www.federalregister.gov/documents/2025/01/17/2025-00708/cybersecurity-in-the-marine-transportation-system |
| EPA Risk Management Program, 40 CFR Part 68 | Binding | Facilities above threshold quantities of regulated substances | In force, including the 2024 Safer Communities rule; changes proposed on 24 February 2026 (91 FR 8970), not final. No cyber-specific requirement; control systems enter through hazard review, process hazard analysis and management of change (CAI reading) | https://www.epa.gov/rmp/common-sense-approach-chemical-accident-prevention-proposed-rule |
| OSHA Process Safety Management, 29 CFR 1910.119 | Binding | Processes with highly hazardous chemicals | In force. No cyber-specific provision; control systems enter through process hazard analysis, mechanical integrity and management of change (CAI reading) | https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1910/subpart-H/section-1910.119 |
| CISA ChemLock | Voluntary | Any facility with dangerous chemicals | Active; includes cyber security goals | https://www.cisa.gov/chemlock |
| CISA Cross-Sector CPGs 2.0; NIST SP 800-82 Rev. 3; ISA/IEC 62443 series | Voluntary | All | Current (CPGs 2.0 of December 2025); ISA/IEC 62443 is a consensus standard | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Management of change and process hazard analysis (PSM, RMP) | Any AI-proposed change on an OT system in this sector is escalated to a human before execution, with the gate reasons recorded; hardening is permitted only in HARDEN, containment only in ISOLATE. | Implemented |
| Cybersecurity plan and incident response procedures (USCG rule) | The lifecycle orders response phases and blocks invalid transitions; containment and eradication require human approval. | Partial (facts set by the caller) |
| Cyber performance standard after the CFATS lapse | The CATASTROPHIC confidence floor (0.95) and the drift limit apply to every AI proposal in the sector, and OT safety approval to actions on assets with a Purdue level and to destructive, containment and eradication actions, whether or not a regulation requires them. | Implemented (AI proposals only) |
| Incident analysis and reporting (CIRCIA when final; sector reporting rules) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `chemical-1.json` | A model proposes isolating a compromised process historian (Purdue level 3) during an incident; confidence 0.97. | ISOLATE | CONTAINMENT, Purdue level 3 | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE |
| `chemical-2.json` | The same proposal with confidence 0.93, below the CATASTROPHIC floor of 0.95. | ISOLATE | CONTAINMENT, Purdue level 3 | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; usa.assurance_floor = DENY; usa.ot_ics_safety = ESCALATE |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- The frozen Chemical sector profile in docs/USA/sectors cites none of the frameworks in Table 2; this document is where they are mapped.
- Whether the final CIRCIA rule keeps a chemical criterion tied to CFATS is not known until the rule is published.

## 7. Sources

- CISA Chemical Sector Risk Management Agency fact sheet (August 2025): https://www.cisa.gov/sites/default/files/2025-08/Chemical_Sector_Risk_Management_Agency_Fact_Sheet_508.pdf
- CRS R48878 (10 March 2026): https://www.congress.gov/crs-product/R48878
- GAO-26-108127: https://www.gao.gov/products/gao-26-108127
- USCG final rule, 17 January 2025: https://www.federalregister.gov/documents/2025/01/17/2025-00708/cybersecurity-in-the-marine-transportation-system
- EPA RMP proposed rule (2026): https://www.epa.gov/rmp/common-sense-approach-chemical-accident-prevention-proposed-rule
- OSHA 29 CFR 1910.119: https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1910/subpart-H/section-1910.119
- CISA ChemLock: https://www.cisa.gov/chemlock
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure
- NIST SP 800-82 Rev. 3, Guide to Operational Technology Security (September 2023): https://csrc.nist.gov/pubs/sp/800/82/r3/final

## Status

Status: Draft – sector framework application, batch 1
End of Document
