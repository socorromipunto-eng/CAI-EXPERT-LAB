# CAI-USA-Energy-Framework-Application

Cybersecurity Artificial Intelligence Framework – Energy Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Energy sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Energy sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: the Department of Energy, led by the Office of Cybersecurity, Energy Security, and Emergency Response (CESER). Electricity is regulated by mandatory NERC CIP reliability standards approved by FERC; pipelines by TSA security directives; energy facilities on waterways by the USCG. Grid operations run on energy management systems and SCADA. DOE CESER and NERC have published official studies of AI in real-time energy operations.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `energy` |
| Sector name | Energy |
| SRMA as recorded by the engine | Department of Energy |
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
| NERC CIP reliability standards (CIP-002 to CIP-015) | Binding | Registered entities with bulk electric system cyber systems | In force. Recent changes: virtualization revisions to 11 standards approved by FERC Order No. 919 (effective 26 May 2026, compliance about two years later); CIP-003-11 (low impact) by Order No. 918; CIP-015-1 (internal network security monitoring) by Order No. 907; Order No. 912 (effective 24 November 2025) directs new supply chain standards | https://www.federalregister.gov/documents/2026/03/24/2026-05716/order-no-919-virtualization-reliability-standards |
| NERC CIP-008 (incident reporting) and EOP-004 (event reporting) | Binding | Registered entities | In force; CIP-008 requires notification of a reportable cyber security incident to the E-ISAC and NCCIC (now part of CISA) within 1 hour | https://www.nerc.com/globalassets/standards/reliability-standards/cip/cip-008-6.pdf |
| DOE Form DOE-417, Electric Emergency Incident and Disturbance Report | Binding | Electric utilities, balancing authorities and others | In force; 1-hour alert for reportable cyber security incidents; OMB approval to 31 May 2027 | https://doe417.pnnl.gov/files/DOE417_Form_Instructions.pdf |
| TSA Security Directives Pipeline-2021-01 and -02 series | Binding | Designated hazardous liquid and natural gas pipeline owners and operators | The TSA index lists 2021-01E and 2021-02F (3 May 2025); the directives are renewed periodically and later versions may exist | https://www.tsa.gov/sd-and-ea |
| TSA proposed rule, Enhancing Surface Cyber Risk Management | Proposed | Pipelines and rail | Proposed 7 November 2024 (89 FR 88488); listed as a long-term action, final date to be determined | https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202604&RIN=1652-AA74 |
| USCG, Cybersecurity in the Marine Transportation System, 33 CFR Part 101 subpart F | Binding | Energy facilities regulated under MTSA | Effective 16 July 2025; cybersecurity plan due 16 July 2027 | https://www.news.uscg.mil/maritime-commons/Article/4247529/final-rule-cybersecurity-in-the-marine-transportation-system-implementation-tim/ |
| DOE Cybersecurity Capability Maturity Model (C2M2) v2.1 | Voluntary | Energy companies | Version 2.1 (June 2022) is the latest | https://www.energy.gov/ceser/cybersecurity-capability-maturity-model-c2m2 |
| NIST IR 7628 Rev. 1, Guidelines for Smart Grid Cybersecurity | Voluntary | Smart grid | Final, September 2014 | https://csrc.nist.gov/pubs/ir/7628/r1/final |
| DOE CESER, Potential Benefits and Risks of AI for Critical Energy Infrastructure | Voluntary | Energy sector | Summary report, 26 April 2024 | https://www.energy.gov/ceser/articles/doe-delivers-initial-risk-assessment-artificial-intelligence-critical-energy |
| NERC white paper, AI and ML in Real-Time System Operations (Rev. 1) | Voluntary | Bulk power system operators | November 2024 | https://www.nerc.com/pa/rrm/bpsa/Documents/Whitepaper-AI%20and%20ML%20in%20Real-Time%20System%20Operations.pdf |
| CISA Cross-Sector CPGs 2.0; NIST SP 800-82 Rev. 3 | Voluntary | All | Current | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| AI in real-time grid operations (DOE CESER report; NERC white paper) | An AI-proposed containment, eradication or destructive action on EMS or SCADA at Purdue level 0 to 2 is escalated by the sector OT gate and by safety.ot_ics; proposals below confidence 0.95 or with drift above 0.15 are denied. | Implemented |
| Change control before acting on BES cyber systems (CIP-010 configuration change management) | Every governed proposal that is not denied waits for a named human; each action category is permitted only in its lifecycle state, so eradication is denied while the lifecycle is in ISOLATE. | Implemented |
| Incident reporting within 1 hour (CIP-008, DOE-417) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Internal network security monitoring (CIP-015) | Not addressed: telemetry is ingested and validated but does not enter decisions (xfail AUD-07). | Not addressed |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `energy-1.json` | A model proposes isolating an energy management system link to substation RTUs (Purdue level 2); confidence 0.97. | ISOLATE | CONTAINMENT, Purdue level 2 | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |
| `energy-2.json` | A model proposes eradication while the lifecycle is in ISOLATE. | ISOLATE | ERADICATION | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; policy.state_constraint = DENY |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- Under the April 2024 CIRCIA proposal, bulk electric and distribution entities required to report to NERC or DOE would be covered, and pipelines through the TSA criterion; the final rule may differ.

## 7. Sources

- DOE CESER: https://www.energy.gov/ceser/office-cybersecurity-energy-security-and-emergency-response
- FERC Order No. 919: https://www.federalregister.gov/documents/2026/03/24/2026-05716/order-no-919-virtualization-reliability-standards
- FERC Order No. 912: https://www.federalregister.gov/documents/2025/09/23/2025-18394/supply-chain-risk-management-reliability-standards-revisions-equipment-and-services-produced-or
- NERC CIP-008-6: https://www.nerc.com/globalassets/standards/reliability-standards/cip/cip-008-6.pdf
- DOE-417 instructions: https://doe417.pnnl.gov/files/DOE417_Form_Instructions.pdf
- TSA security directives: https://www.tsa.gov/sd-and-ea
- TSA proposed rule (RIN 1652-AA74): https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202604&RIN=1652-AA74
- USCG implementation timeline: https://www.news.uscg.mil/maritime-commons/Article/4247529/final-rule-cybersecurity-in-the-marine-transportation-system-implementation-tim/
- DOE C2M2: https://www.energy.gov/ceser/cybersecurity-capability-maturity-model-c2m2
- NIST IR 7628 Rev. 1: https://csrc.nist.gov/pubs/ir/7628/r1/final
- DOE CESER AI risk assessment: https://www.energy.gov/ceser/articles/doe-delivers-initial-risk-assessment-artificial-intelligence-critical-energy
- NERC AI and ML white paper: https://www.nerc.com/pa/rrm/bpsa/Documents/Whitepaper-AI%20and%20ML%20in%20Real-Time%20System%20Operations.pdf
- CIRCIA proposed rule covered-entity infographic: https://www.cisa.gov/sites/default/files/2024-05/24-0630-Covered-Entity-Infographic-04242024-508c.pdf
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure
- NIST SP 800-82 Rev. 3, Guide to Operational Technology Security (September 2023): https://csrc.nist.gov/pubs/sp/800/82/r3/final

## Status

Status: Draft – sector framework application, batch 2
End of Document
