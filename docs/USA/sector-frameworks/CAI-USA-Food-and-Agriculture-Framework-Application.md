# CAI-USA-Food-and-Agriculture-Framework-Application

Cybersecurity Artificial Intelligence Framework – Food and Agriculture Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Food and Agriculture sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Food and Agriculture sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agencies: USDA and HHS, with FDA acting for HHS. The sector is almost entirely privately owned (CISA). No binding federal rule addresses cybersecurity in this sector; food-defense and traceability rules govern physical adulteration and records. Food processing runs on industrial control systems, and precision agriculture adds connected equipment; CISA guidance covers OT remote access and OT backups, and the FBI has reported ransomware against agricultural cooperatives timed to planting and harvest.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `food_agriculture` |
| Sector name | Food and Agriculture |
| SRMA as recorded by the engine | USDA and HHS (FDA) |
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
| FSMA Intentional Adulteration rule, 21 CFR Part 121 | Binding (not a cybersecurity rule) | Food facilities, except very small businesses | In force; the vulnerability assessment addresses physical contamination and inside attackers; it does not mention cyber or information systems | https://www.ecfr.gov/current/title-21/part-121 |
| FDA Food Traceability Rule, 21 CFR Part 1 subpart S | Binding (not a cybersecurity rule) | Entities handling foods on the Food Traceability List | Enforcement barred before 20 July 2028 by statute; records in a sortable electronic spreadsheet within 24 hours on request | https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods |
| CISA Food and Agriculture Cybersecurity Checklist and Resources | Voluntary | All sector entities | Current CISA publication; includes OT remote-access hardening and OT backups | https://www.cisa.gov/resources-tools/resources/food-and-agriculture-cybersecurity-checklist-and-resources |
| FBI Private Industry Notification 20220420-001, ransomware against agricultural cooperatives | Advisory | Agricultural cooperatives | Published 20 April 2022 | https://ic3.gov/CSA/2022/220420-2.pdf |
| USDA Artificial Intelligence Strategy (FY2026 to FY2027) | Policy | USDA | Published September 2025; covers USDA's own use of AI, not guidance for industry | https://www.usda.gov/sites/default/files/documents/usda-ai-strategy-2025.pdf |
| CISA Cross-Sector CPGs 2.0; NIST CSF 2.0; NIST SP 800-82 Rev. 3 | Voluntary | All | Current | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Safe operation of processing-line OT (CISA checklist; SP 800-82) | An AI-proposed containment, eradication or destructive action on a line HMI or controller at Purdue level 0 to 2 is escalated by the sector OT gate and by safety.ot_ics and cannot execute without a human. | Implemented |
| Generative AI assistants in operations (no sector rule; NIST AI 600-1) | Generative AI without provenance or explanation is denied; every proposal escalates to a human; confidence floor 0.90. | Implemented |
| Integrity of traceability records (Food Traceability Rule) | Not addressed: CAI does not protect food traceability records; its evidence log covers governed decisions only. | Not addressed |
| Ransomware response timed to planting and harvest (FBI PIN) | Response phases are ordered by the lifecycle and containment needs human approval. | Partial (facts set by the caller) |
| Incident analysis and reporting (CIRCIA when final; sector reporting rules) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `food_agriculture-1.json` | A model proposes isolating the HMI of a food-processing line (Purdue level 2); confidence 0.94. | ISOLATE | CONTAINMENT, Purdue level 2 | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; safety.ot_ics = ESCALATE |
| `food_agriculture-2.json` | A generative AI assistant proposes the same action without an explanation and declares its output not explainable. | ISOLATE | CONTAINMENT, Purdue level 2 | BLOCKED (DENY) | usa.nist_ai_600_1 = DENY; usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; safety.ai_explainability = DENY; safety.ot_ics = ESCALATE |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- Under the April 2024 CIRCIA proposal there is no sector-specific criterion for Food and Agriculture; entities would be covered through the size test. The final rule may differ.

## 7. Sources

- CISA Food and Agriculture Sector: https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors/food-and-agriculture-sector
- 21 CFR Part 121: https://www.ecfr.gov/current/title-21/part-121
- FDA Food Traceability Rule: https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods
- FDA notice of public meeting on traceability (9 October 2026): https://www.govinfo.gov/content/pkg/FR-2026-10-09/pdf/2026-20720.pdf
- CISA Food and Agriculture checklist: https://www.cisa.gov/resources-tools/resources/food-and-agriculture-cybersecurity-checklist-and-resources
- FBI PIN 20220420-001: https://ic3.gov/CSA/2022/220420-2.pdf
- USDA AI Strategy: https://www.usda.gov/sites/default/files/documents/usda-ai-strategy-2025.pdf
- CIRCIA proposed rule covered-entity infographic: https://www.cisa.gov/sites/default/files/2024-05/24-0630-Covered-Entity-Infographic-04242024-508c.pdf
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure
- NIST SP 800-82 Rev. 3, Guide to Operational Technology Security (September 2023): https://csrc.nist.gov/pubs/sp/800/82/r3/final

## Status

Status: Draft – sector framework application, batch 2
End of Document
