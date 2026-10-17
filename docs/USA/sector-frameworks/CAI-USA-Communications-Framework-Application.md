# CAI-USA-Communications-Framework-Application

Cybersecurity Artificial Intelligence Framework – Communications Sector Framework Application (USA)
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2026 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

**NOTE**
The normative language of CAI-EXPERT-LAB documentation is English.
This document maps the cybersecurity frameworks that apply to the U.S. Communications sector and the decision-time controls CAI adds to them.
It does not assert compliance, certification, accreditation, or regulatory approval.

## 1. Purpose

This document states which cybersecurity frameworks apply to the Communications sector in the United States as of 2026-10-16, and what CAI adds at decision time: the governance of operational actions, including actions proposed by AI systems, before they are executed. It complements the frozen sector profile in docs/USA/sectors and does not modify it. Method, status values and the cross-sector baseline are in README.md of this directory.

## 2. Sector profile

Sector Risk Management Agency: DHS, with CISA carrying out the role. The FCC regulates carriers. In November 2025 the FCC rescinded its January 2025 declaratory ruling that CALEA section 105 imposes cybersecurity obligations, so, apart from the cybersecurity risk management plan required of submarine cable landing licensees (FCC 25-49), no FCC rule now sets general cybersecurity obligations for carriers; sector obligations are about lawful intercept, customer data, outage reporting and equipment supply chain. The engine marks the sector OT-intensive; that is CAI's own classification, based on the physical-service effect of network control actions, not an official designation.

Table 1 — Engine parameters for this sector (CAI-Engine 0.4.2, `usa_sectors.py` and `usa.py`).

| Parameter | Value |
|---|---|
| Sector key in the engine | `communications` |
| Sector name | Communications |
| SRMA as recorded by the engine | CISA (DHS) |
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
| CALEA, 47 U.S.C. 1001 et seq. | Binding | Telecommunications carriers | In force; FCC declaratory ruling FCC 25-9 on section 105 rescinded by FCC 25-81 (adopted 20 November 2025, 90 FR 58006) | https://www.govinfo.gov/content/pkg/FR-2025-12-15/html/2025-22830.htm |
| CPNI rules, 47 CFR 64.2001 et seq. | Binding | Carriers and interconnected VoIP providers | In force, including the 2023 breach-notification update (FCC 23-111) | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-U |
| Network outage reporting, 47 CFR Part 4 (NORS, DIRS) | Binding | Providers covered by Part 4 | In force; amended by FCC 25-45, effective 16 September 2025 | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-4 |
| Secure and Trusted Communications Networks Act; FCC Covered List | Binding | New FCC equipment authorizations; reimbursed replacement of covered equipment | In force; consumer-grade routers produced abroad added on 23 March 2026 (DA 26-278), except those with a DoW or DHS Conditional Approval | https://docs.fcc.gov/public/attachments/DA-26-278A1.pdf |
| Submarine cable landing license rules (FCC 25-49, 90 FR 48648) | Binding | Submarine cable applicants and licensees | Effective 26 November 2025 (some sections later); licensees certify a cybersecurity and physical security risk management plan | https://www.federalregister.gov/documents/2025/10/27/2025-19658/review-of-submarine-cable-landing-license-rules-and-procedures-to-assess-evolving-national-security |
| U.S. Cyber Trust Mark (IoT labeling) | Voluntary | Consumer IoT products | Program continues; new Lead Administrator selected in April 2026 | https://www.fcc.gov/document/fcc-selects-ioxt-new-cyber-trust-mark-program-lead-administrator |
| Enhanced Visibility and Hardening Guidance for Communications Infrastructure (CISA, NSA, FBI and partners) | Voluntary | Network operators | Published 3 December 2024 | https://cisa.gov/resources-tools/resources/enhanced-visibility-and-hardening-guidance-communications-infrastructure |
| CISA Cross-Sector CPGs 2.0; NIST CSF 2.0 | Voluntary | All | Current | See README.md section 4 |

## 4. What CAI adds

The binding frameworks in Table 2 set what entities must protect, plan, monitor and report; some also control changes before they are made. In the frameworks reviewed here, none sets requirements for operational actions proposed by AI systems. Voluntary guidance has started to address them (README.md section 4). CAI proposes a decision-time control layer for each proposed action. Status: Implemented (engine 0.4.2, with tests), Partial, Specified (CAI-ENG-SEC-001), Described.

Table 3 — Framework obligation areas and the decision-time control CAI adds.

| Obligation area (framework) | What CAI adds at decision time | Status |
|---|---|---|
| Hardening of network equipment (CISA/NSA hardening guidance) | An AI-proposed hardening change is permitted only in HARDEN and escalates to a human, as in every critical infrastructure sector, with reasons recorded. | Implemented |
| Response sequencing during an intrusion | Eradication proposed while the lifecycle is still in DETECT is denied by the state constraint; containment and eradication need human approval. | Implemented |
| Outage and breach reporting (Part 4, CPNI) | Every governed decision is recorded with gate results, reasons, sector, SRMA and approver in a hash-chained log, which gives the decision part of the history an incident report needs. The log is tamper-evident for single records and not signed. | Partial |
| Equipment supply chain (Covered List) | Not addressed: CAI does not check the provenance or authorization of equipment. | Not addressed |
| Decision integrity over time (not addressed by the frameworks) | Revalidation of a pending decision at approval and before dispatch, and environmental state from signed sources, so that a decision approved under one situation is not executed under another. | Specified (SR-06 to SR-11, SR-13); approve() does not revalidate today (xfail T-09) |

## 5. Worked examples

Synthetic proposals evaluated by the engine under the USA jurisdiction. The outcomes below are produced by the engine and checked on every test run by `tests/TEST_SECTOR_EXAMPLES.py`; the example files are in `CAI-Engine/implementation/examples/sectors/`. Gates not listed returned ALLOW.

Table 4 — Worked examples and engine outcomes.

| File | Scenario | Lifecycle state | Action | Outcome | Gates that did not allow |
|---|---|---|---|---|---|
| `communications-1.json` | A model proposes a hardening change on edge routers (disable an exposed management service); confidence 0.95. | HARDEN | HARDENING | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE |
| `communications-2.json` | A model proposes eradication while the lifecycle is still in DETECT. | DETECT | ERADICATION | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; usa.ot_ics_safety = ESCALATE; policy.state_constraint = DENY |

Gate meanings: `usa.nist_ai_rmf`: NIST AI RMF governance recorded (informational); `usa.srma_oversight`: human oversight required for a critical infrastructure sector; `usa.ot_ics_safety`: OT-intensive sector: an action on an asset with a Purdue level, or a destructive, containment or eradication action, needs cyber-physical safety approval; `usa.assurance_floor`: AI confidence below the floor for the sector consequence level; `usa.robustness`: declared model drift above 0.15; `usa.nist_ai_600_1`: generative AI without provenance or explanation (NIST AI 600-1); `policy.state_constraint`: action category checked against the current lifecycle state; `safety.none_triggered`: no CAI safety gate triggered; `safety.ai_explainability`: AI output not explainable: cannot trigger an action; `safety.ot_ics`: containment, eradication or destructive action on an asset at Purdue level 0 to 2: human approval required.

## 6. Gaps and limits

- Environmental state does not enter the decision: accepted telemetry is recorded but not used, and its age is not checked (xfail AUD-07, CAI-USA-NIST-Map section 9).
- Entry conditions, AI confidence, drift and deployment context are declared by the caller, not observed by the engine.
- The engine records decisions; it does not perform any action on sector systems. Adapters that would act are specified (CAI-ENG-SEC-001 Core SR-21), not implemented.
- Approvers are names, not authenticated identities; approvals and evidence are not signed (SR-14, SR-19, SR-20).
- A proposal is evaluated under the USA profile only if it states the USA jurisdiction (or the caller passes it); without it the engine applies the EU profile and no usa.* gate runs.
- The folder of the frozen sector profile is named Communication (see docs/USA/sectors/README.md, Sector Coverage).
- Whether the final CIRCIA rule keeps the communications criteria of the April 2024 proposal is not known until publication.

## 7. Sources

- CISA Communications Sector: https://www.cisa.gov/communications-sector
- FCC 25-81, Order on Reconsideration (90 FR 58006): https://www.govinfo.gov/content/pkg/FR-2025-12-15/html/2025-22830.htm
- 47 CFR Part 64 subpart U: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-U
- 47 CFR Part 4: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-4
- FCC DA 26-278: https://docs.fcc.gov/public/attachments/DA-26-278A1.pdf
- FCC 25-49, submarine cable rules: https://www.federalregister.gov/documents/2025/10/27/2025-19658/review-of-submarine-cable-landing-license-rules-and-procedures-to-assess-evolving-national-security
- FCC Cyber Trust Mark administrator: https://www.fcc.gov/document/fcc-selects-ioxt-new-cyber-trust-mark-program-lead-administrator
- Enhanced Visibility and Hardening Guidance: https://cisa.gov/resources-tools/resources/enhanced-visibility-and-hardening-guidance-communications-infrastructure
- CISA Cross-Sector Cybersecurity Performance Goals 2.0 (11 December 2025): https://www.cisa.gov/news-events/alerts/2025/12/11/cybersecurity-performance-goals-20-critical-infrastructure

## Status

Status: Draft – sector framework application, batch 1
End of Document
