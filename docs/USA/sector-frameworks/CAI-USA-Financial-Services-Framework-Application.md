# CAI-USA-Financial-Services-Framework-Application

Cybersecurity Artificial Intelligence Framework – Financial Services Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Financial Services sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Financial Services sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: the Department of the Treasury, through its Office of Cybersecurity and Critical Infrastructure Protection (OCCIP). Banking, securities and state regulators impose safeguarding and incident-notification rules. In April 2026 the banking agencies replaced their 2011 model risk management guidance with SR 26-2, which states that generative and agentic AI models are outside its scope: controls for them are left to institutions' own risk-management practices. Operational technology plays a smaller role than in other sectors.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `financial_services` |
| Sector name | Financial Services |
| SRMA as recorded by the engine | Department of the Treasury |
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
| Interagency Guidelines Establishing Information Security Standards (GLBA), 12 CFR Part 30 Appendix B and counterparts | Binding | Banks | In force, including the response program and customer notice (Supplement A) | https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20B%20to%20Part%2030 |
| Computer-security incident notification rule, 12 CFR Part 53 and counterparts | Binding | Banking organizations and their service providers | In force; notify the primary federal regulator within 36 hours | https://www.ecfr.gov/current/title-12/chapter-I/part-53 |
| NCUA cyber incident notification, 12 CFR 748.1(c) | Binding | Federally insured credit unions | In force; notify NCUA within 72 hours | https://www.ecfr.gov/current/title-12/chapter-VII/subchapter-A/part-748/section-748.1 |
| SEC Regulation S-P amendments (2024) | Binding | Broker-dealers, investment companies, investment advisers, transfer agents | Compliance from 3 December 2025 (larger entities) and 3 June 2026 (smaller); customer notice within 30 days; service providers notify within 72 hours | https://www.federalregister.gov/documents/2024/06/03/2024-11116/regulation-s-p-privacy-of-consumer-financial-information-and-safeguarding-customer-information |
| SEC cybersecurity disclosure rules (Form 8-K Item 1.05; Regulation S-K Item 106) | Binding | Public companies | In force; material incident disclosed within 4 business days of the materiality determination; under review after 2025-2026 petitions and comments | https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/cybersecurity-risk-management-strategy-governance-incident-disclosure |
| SEC Regulation SCI, 17 CFR 242.1000 to 242.1007 | Binding | SCI entities (exchanges, clearing agencies and others) | In force; the 2023 proposal to expand it was withdrawn on 17 June 2025 | https://www.federalregister.gov/documents/2025/06/17/2025-11110/withdrawal-of-proposed-regulatory-actions |
| NYDFS Cybersecurity Regulation, 23 NYCRR Part 500 | Binding (New York State) | Entities licensed by NYDFS | Second amendment fully phased in on 1 November 2025; incidents reported within 72 hours and extortion payments within 24 hours (section 500.17) | https://www.dfs.ny.gov/industry_guidance/cybersecurity/implementation_timeline_covered_entities |
| FTC Safeguards Rule, 16 CFR Part 314 | Binding | Non-bank financial institutions | In force; FTC notification within 30 days for 500 or more consumers | https://www.govinfo.gov/content/pkg/FR-2023-11-13/html/2023-24412.htm |
| SR 26-2, model risk management guidance (Fed, OCC, FDIC) | Supervisory guidance | Banking organizations, mainly above $30 billion in assets | Issued 17 April 2026; supersedes SR 11-7; generative and agentic AI models are outside its scope | https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm |
| Treasury, Managing AI-Specific Cybersecurity Risks in the Financial Services Sector | Voluntary | Financial institutions | Published 27 March 2024 | https://home.treasury.gov/news/press-releases/jy2212 |
| Financial Services Sector Specific Goals (FS-SSG) ver. 2.0 | Voluntary | Financial institutions | August 2026; led by the FSSCC, with Treasury and CISA | https://home.treasury.gov/system/files/216/financial-services-sector-specific-goals-082426.pdf |
| FFIEC IT Examination Handbook; NIST CSF 2.0 | Voluntary (examiner guidance) | Financial institutions | Current; the FFIEC Cybersecurity Assessment Tool was retired on 31 August 2025 | https://ithandbook.ffiec.gov/it-booklets/information-security |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Governance of generative and agentic AI actions (outside the scope of SR 26-2) | Each action proposed by an AI system is evaluated before execution: confidence floor 0.90, drift limit 0.15, generative AI without provenance or explanation denied, human approval for every proposal. | Implemented |
| Privileged access changes (Interagency Guidelines, NYDFS access privileges) | An action the caller marks as affecting privileged accounts requires human approval; the engine does not detect privileged impact itself and writes no separate gate record for it. | Partial |
| Incident notification within 36 hours, 72 hours or 4 business days | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Model validation and ongoing monitoring of AI models (SR 26-2 for non-generative models) | Confidence and drift are recorded and gated per decision, but they are declared by the AI client; CAI does not validate models. | Partial |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `financial_services-1.json` | A model proposes disabling a compromised privileged service account at a bank; confidence 0.95. | ISOLATE | CONTAINMENT | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE |
| `financial_services-2.json` | The same proposal from a model whose declared drift is 0.25. | ISOLATE | CONTAINMENT | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; usa.robustness = DENY |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- The engine marks the sector as not OT-intensive, consistent with official sector descriptions.
- Which financial-services entities the final CIRCIA rule will cover is not known until it is published.

## 7. Sources

- CISA Financial Services Sector: https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors/financial-services-sector
- 12 CFR Part 30 Appendix B: https://www.ecfr.gov/current/title-12/chapter-I/part-30/appendix-Appendix%20B%20to%20Part%2030
- 12 CFR Part 53: https://www.ecfr.gov/current/title-12/chapter-I/part-53
- 12 CFR 748.1: https://www.ecfr.gov/current/title-12/chapter-VII/subchapter-A/part-748/section-748.1
- SEC Regulation S-P (2024): https://www.federalregister.gov/documents/2024/06/03/2024-11116/regulation-s-p-privacy-of-consumer-financial-information-and-safeguarding-customer-information
- SEC cybersecurity disclosure compliance guide: https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/cybersecurity-risk-management-strategy-governance-incident-disclosure
- SEC withdrawal of proposed rules (17 June 2025): https://www.federalregister.gov/documents/2025/06/17/2025-11110/withdrawal-of-proposed-regulatory-actions
- NYDFS implementation timeline: https://www.dfs.ny.gov/industry_guidance/cybersecurity/implementation_timeline_covered_entities
- SR 26-2: https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- Treasury AI cybersecurity report: https://home.treasury.gov/news/press-releases/jy2212
- FS-SSG ver. 2.0: https://home.treasury.gov/system/files/216/financial-services-sector-specific-goals-082426.pdf
- FFIEC IT Handbook: https://ithandbook.ffiec.gov/it-booklets/information-security
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure

## Status

Status: Draft – sector framework application, batch 2
End of Document
