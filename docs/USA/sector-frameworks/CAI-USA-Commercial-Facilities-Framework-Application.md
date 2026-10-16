# CAI-USA-Commercial-Facilities-Framework-Application

Cybersecurity Artificial Intelligence Framework – Commercial Facilities Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Commercial Facilities sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Commercial Facilities sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: DHS (CISA). Subsectors listed by CISA: Entertainment and Media, Gaming, Lodging, Outdoor Events, Public Assembly, Real Estate, Retail, Sports Leagues. There is no sector-wide cybersecurity regulation. Building automation and control systems (HVAC, lighting, access control, fire alarms, energy management) bring operational technology into the sector (NIST, August 2026). This sector has no profile in docs/USA/sectors (see the Sector Coverage section of docs/USA/sectors/README.md); this document is its only sector-level CAI document.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `commercial_facilities` |
| Sector name | Commercial Facilities |
| SRMA as recorded by the engine | CISA (DHS) |
| Consequence level | MODERATE |
| OT-intensive | No |
| AI confidence floor (usa.assurance_floor) | 0.80 |
| Maximum declared drift (usa.robustness) | 0.15 |
| Human oversight (usa.srma_oversight) | Every governed proposal escalates to a human |
| OT safety approval (usa.ot_ics_safety) | Not applied: the sector is not marked OT-intensive; the CAI gate safety.ot_ics still applies to containment, eradication or destructive actions on assets at Purdue level 0 to 2 |

## 3. Applicable frameworks

Type: Binding (law or regulation, for the entities in scope), Contractual, Incentive, Voluntary. Status is as verified on 2026-10-16 in the source given.

Table 2 — Frameworks that apply to the sector or to parts of it.

| Framework | Type | Scope in this sector | Status on 2026-10-16 | Source |
|---|---|---|---|---|
| FTC Act section 5, 15 U.S.C. 45 | Binding | Most businesses that handle consumer data (unfair or deceptive data-security practices) | In force | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section45 |
| FTC Safeguards Rule, 16 CFR Part 314 | Binding | Only entities that are financial institutions under GLBA (for example, operators that extend credit themselves) | In force; notification to the FTC within 30 days of an event involving 500 or more consumers, effective 13 May 2024 | https://www.govinfo.gov/content/pkg/FR-2023-11-13/html/2023-24412.htm |
| State data-breach notification laws | Binding | Entities holding personal information of state residents | In force in every state; triggers and deadlines differ and are not mapped here | — |
| PCI DSS v4.0.1 | Contractual | Merchants that accept payment cards | Imposed through card-brand and acquirer contracts; not a law | PCI Security Standards Council |
| SAFETY Act (DHS) | Incentive | Providers of qualified anti-terrorism technologies, including cybersecurity and venue security | Liability protection, not a security requirement | https://www.safetyact.gov/about/benefits |
| NIST tips on building automation and control systems (blog post and infographic) | Voluntary | Facilities with BACS | Published 19 August 2026; not a numbered NIST publication | https://www.nist.gov/blogs/cybersecurity-insights/nist-releases-tips-tactics-building-automation-control-system |
| CISA Cross-Sector CPGs 2.0; NIST CSF 2.0 | Voluntary | All | Current | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. None of them sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Reasonable data-security practices (FTC Act section 5, Safeguards Rule) | AI-proposed security actions are gated and recorded with reasons and a named approver, which documents how security decisions were made. | Partial |
| Building automation as OT (NIST BACS guidance) | Containment, eradication or destructive actions on assets at Purdue level 0 to 2 need human approval (CAI gate safety.ot_ics). The sector is not marked OT-intensive in the engine, so the sector OT gate does not apply. | Partial |
| Proportionate assurance for a MODERATE-consequence sector | Confidence floor 0.80 and drift limit 0.15 for AI proposals; every proposal still escalates to a human because the sector is critical infrastructure. | Implemented |
| Incident analysis and reporting (CIRCIA when final; sector reporting rules) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `commercial_facilities-1.json` | A model proposes isolating the building automation VLAN of a stadium after anomalous BACnet traffic; confidence 0.92. | ISOLATE | CONTAINMENT | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE |
| `commercial_facilities-2.json` | The same proposal from a model whose declared drift is 0.20, above the maximum of 0.15. | ISOLATE | CONTAINMENT | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; usa.robustness = DENY |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: OT-level, destructive, containment or eradication action needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- The engine marks the sector as not OT-intensive although building automation is OT; whether to change that parameter is an open design decision.
- Under the April 2024 CIRCIA proposal no sector-specific criterion names Commercial Facilities; entities would be covered only through the size test or another criterion. The final rule may differ.

## 7. Sources

- CISA Commercial Facilities Sector: https://www.cisa.gov/commercial-facilities-sector
- FTC Safeguards Rule amendment (88 FR 77499): https://www.govinfo.gov/content/pkg/FR-2023-11-13/html/2023-24412.htm
- SAFETY Act: https://www.safetyact.gov/about/benefits
- NIST, building automation and control systems (19 August 2026): https://www.nist.gov/blogs/cybersecurity-insights/nist-releases-tips-tactics-building-automation-control-system
- CIRCIA proposed rule covered-entity infographic: https://www.cisa.gov/sites/default/files/2024-05/24-0630-Covered-Entity-Infographic-04242024-508c.pdf
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure

## Status

Status: Draft – sector framework application, batch 1
End of Document
