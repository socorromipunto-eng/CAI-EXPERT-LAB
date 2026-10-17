# CAI-USA-Emergency-Services-Framework-Application

Cybersecurity Artificial Intelligence Framework – Emergency Services Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Emergency Services sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Emergency Services sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: DHS (CISA). Disciplines listed by CISA: Emergency Management, Emergency Medical Services, Fire and Rescue Services, Law Enforcement, and Public Works; CISA's 2023 cyber risk assessment adds Public Safety Communications and Coordination. There is no sector-wide cybersecurity regulation; obligations come from the FBI CJIS Security Policy, FCC 911 rules for 911 service providers, and HIPAA for EMS providers that are covered entities. CISA names control systems, computer-aided dispatch and land mobile radio as sector cyber infrastructure.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `emergency_services` |
| Sector name | Emergency Services |
| SRMA as recorded by the engine | CISA (DHS) |
| Consequence level | HIGH |
| OT-intensive | No |
| AI confidence floor (usa.assurance_floor) | 0.90 |
| Maximum declared drift (usa.robustness) | 0.15 |
| Human oversight (usa.srma_oversight) | Every governed proposal escalates to a human |
| OT safety approval (usa.ot_ics_safety) | Not applied: the sector is not marked OT-intensive; the CAI gate safety.ot_ics still applies to containment, eradication or destructive actions on assets at Purdue level 0 to 2 |

## 3. Applicable frameworks

Type: Binding (law or regulation, for the entities in scope), Contractual, Incentive, Voluntary. Status is as verified on 2026-10-16 in the source given.

Table 2 — Frameworks that apply to the sector or to parts of it.

| Framework | Type | Scope in this sector | Status on 2026-10-16 | Source |
|---|---|---|---|---|
| FBI CJIS Security Policy v6.1 | Binding (access condition) | Agencies and vendors accessing criminal justice information | Version 6.1 dated 25 June 2026 | https://le.fbi.gov/cjis-division/cjis-security-policy-resource-center |
| FCC 911 reliability, 47 CFR 9.19 | Binding | Covered 911 service providers (not PSAPs) | In force; NG911 Second Report and Order (FCC 26-39) extends the definition to ESInet, NGCS and IP transport providers, effective 10 August 2026, with some compliance dates deferred | https://www.federalregister.gov/documents/2026/07/10/2026-13998/facilitating-implementation-of-next-generation-911-services-ng911-improving-911-reliability |
| FCC 911 outage notification, 47 CFR 4.9(h) | Binding | Providers serving 911 special facilities | In force; notify the affected 911 special facility within 30 minutes of discovering an outage | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-4/section-4.9 |
| FCC NG911 transition order (FCC 24-78) | Binding | Originating service providers | Effective 25 November 2024; obligations run from a valid request by a 911 authority | https://www.federalregister.gov/documents/2024/09/24/2024-18603/facilitating-implementation-of-next-generation-911-services-ng911-location-based-routing-for |
| HIPAA Security Rule | Binding | EMS providers that are HIPAA covered entities | In force | https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html |
| Cyber Risks to Next Generation 911 (DHS OEC) | Voluntary | PSAPs and 911 authorities | 2016 publication, still listed on 911.gov | https://www.911.gov/assets/OEC_NG911_Cybersecurity_Primer_041216_508_compliant.pdf |
| SAFECOM/NCSWIC, Artificial Intelligence in Emergency Communications Centers (infographic) | Voluntary | Emergency communications centers | Current CISA publication; treats AI as decision support for call triage, translation, transcription and quality assurance | https://www.cisa.gov/news-events/news/safecom-and-national-council-statewide-interoperability-coordinators-ncswic-develop-artificial |
| CISA Cross-Sector CPGs 2.0; NIST CSF 2.0 | Voluntary | All | Current | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| AI as decision support in emergency communications (SAFECOM/NCSWIC) | An AI proposal cannot act by itself: every proposal escalates to a human, and an output the AI client declares not explainable is denied. | Implemented |
| Containment of compromised dispatch and PSAP systems (CISA sector cyber risk assessment) | Containment is permitted only in ISOLATE and needs human approval, with reasons recorded. | Implemented |
| 911 outage notification and reporting (47 CFR 4.9; CIRCIA when final) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| CJIS access and authentication requirements | Not addressed: CAI does not implement CJIS identity, encryption or audit requirements. | Not addressed |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `emergency_services-1.json` | A model proposes isolating a compromised computer-aided dispatch workstation; confidence 0.94. | ISOLATE | CONTAINMENT | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE |
| `emergency_services-2.json` | The same proposal from a model that gives no explanation. | ISOLATE | CONTAINMENT | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; safety.ai_explainability = DENY |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- The engine marks the sector as not OT-intensive although CISA names control systems and radio infrastructure; the sector OT gate therefore does not apply. Whether to change that parameter is an open design decision.
- Under the April 2024 CIRCIA proposal, providers of emergency services to a population of 50,000 or more would be covered; the final rule may differ.

## 7. Sources

- CISA Emergency Services Sector: https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors/emergency-services-sector
- CISA Emergency Services Sector Cyber Risk Assessment (November 2023): https://www.cisa.gov/sites/default/files/2023-12/ess-cyber-risk-assessment_112023_508.pdf
- FBI CJIS Security Policy resource center: https://le.fbi.gov/cjis-division/cjis-security-policy-resource-center
- FCC 26-39 (91 FR 42794): https://www.federalregister.gov/documents/2026/07/10/2026-13998/facilitating-implementation-of-next-generation-911-services-ng911-improving-911-reliability
- 47 CFR 4.9: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-4/section-4.9
- FCC 24-78: https://www.federalregister.gov/documents/2024/09/24/2024-18603/facilitating-implementation-of-next-generation-911-services-ng911-location-based-routing-for
- HHS, HIPAA covered entities: https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html
- SAFECOM/NCSWIC AI in emergency communications centers: https://www.cisa.gov/news-events/news/safecom-and-national-council-statewide-interoperability-coordinators-ncswic-develop-artificial
- CIRCIA proposed rule overview: https://www.cisa.gov/sites/default/files/2024-05/CIRCIA%20NPRM%20Overview%20May_508cL.pdf
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure

## Status

Status: Draft – sector framework application, batch 2
End of Document
