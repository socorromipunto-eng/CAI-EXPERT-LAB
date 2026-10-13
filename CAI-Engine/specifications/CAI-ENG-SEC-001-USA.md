# CAI Engine — MCP Security Specification: USA Jurisdiction Profile

| Field | Value |
|---|---|
| Document ID | CAI-ENG-SEC-001-USA |
| Version | 0.4 |
| Status | PROPOSED — requires owner approval before any implementation |
| Classification | Public (repository document) |
| Project | CAI-EXPERT-LAB / CAI-Engine |
| Phase | Proposed specification for cai-engine 0.5.0; owner approval pending (gate G0) |
| Core specification | CAI-ENG-SEC-001 v0.8 (profile interface SR-26, core gates SR-27) |
| Companion profile | CAI-ENG-SEC-001-EU (equal rank) |
| Baseline | Git commit b52935e (`cai_engine/usa.py`, `usa_sectors.py`, `nist_ai_rmf.py`) |
| Owner | Antonio José Socorro Marín |
| Prepared by | Antonio José Socorro Marín |
| Date | 2026-10-13 |

Copyright © 2026 Antonio José Socorro Marín. All rights reserved. Use is governed by the legal documents in the `/legal` directory of this repository.

## Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-12 | First version: 9 findings, 11 requirements, 14 tests. |
| 0.2 | 2026-10-12 | Revision after review: Transportation SRMA corrected (DHS and DOT) and recorded as a baseline data error; NSM-22 review under Executive Order 14239 recorded; NIST IR 8547 summary corrected; CNSA 2.0 deployments declared unsupported in 0.5.0; assurance-gate mapping relabelled as CAI interpretation of the USA baseline; gate failures open a review; drift triggers revalidation; model version bound to the registration; provenance gate relabelled as a presence check; floors at or below the core floor removed; retention, labels and post-quantum requirements with tests; tests moved to the gates where their prerequisites exist. 10 findings, 15 requirements, 18 tests. |
| 0.3 | 2026-10-12 | Consistency corrections: `classical_suite_end` from the core interface; retention re-checked at registry reload; USA-AT-04 moved to G8; USA-AT-09 asserts the profile reason code; USA-SR-08 wording; observation wording. 10 findings, 15 requirements, 18 tests. |
| 0.4 | 2026-10-13 | Published in the repository (CHG-2026-10-13-01): header block completed (Phase, Owner, Prepared by); core reference updated to v0.8; firmware-signing note no longer names a specific embedded platform. Executive Order 14239 §3(b) checked on 2026-10-13 against the Daily Compilation of Presidential Documents (DCPD-202500374); NIST IR 8547 still an initial public draft. No requirement, finding or test changed. |

---

## 1. Purpose and relationship to the core

This profile defines how the CAI Engine evaluates AI-assisted security decisions on targets registered under the profile identifier `USA`. It implements the core profile interface (CAI-ENG-SEC-001 SR-26) and never relaxes a core control or a core gate (SR-27).

The U.S. setting has no single horizontal AI statute. The profile is therefore organized around critical-infrastructure sectors and their Sector Risk Management Agencies (SRMAs), voluntary NIST frameworks, and the lifecycle and assurance gates of the CAI USA baseline (`docs/USA/CAI-USA-AI-Governance-and-Assurance.md`). Gate results state `alignment` or `supports`; they never state compliance with any statute, rule, framework or SRMA directive (core SR-26.4). Rules that go beyond an instrument are labelled **CAI policy**.

## 2. Scope

In scope: sector classification of targets; the AI-system lifecycle; the four operational assurance gates of the CAI USA baseline, as interpreted in §7; consequence-scaled thresholds and approvals; SRMA and OT/ICS escalation; generative-AI provenance presence checks; NIST AI RMF traceability; retention; the post-quantum timeline.

Out of scope: sector-specific regulatory reporting; federal-agency AI governance requirements; certification under any framework; deployments for national security systems (`nss = true`, core SR-25.8).

## 3. References

- National Security Memorandum on Critical Infrastructure Security and Resilience (NSM-22), 30 April 2024, which superseded PPD-21; sixteen sectors and their SRMAs. Executive Order 14239 (18 March 2025), §3(b), ordered a review of NSM-22 for possible revision; the outcome of that review MUST be verified and recorded before G4 is released.
- NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0), 2023.
- NIST AI 600-1, Generative Artificial Intelligence Profile, 2024.
- NIST CSF 2.0 (CSWP 29), NIST SP 800-53 Rev. 5 (including AU-11 audit record retention), NIST SP 800-82 Rev. 3, CISA Zero Trust Maturity Model 2.0.
- NSA Commercial National Security Algorithm Suite 2.0 (CNSA 2.0) and its FAQ.
- NIST IR 8547, Transition to Post-Quantum Cryptography Standards (initial public draft, November 2024; final status to be confirmed at each gate release).
- CAI-EXPERT-LAB `REGULATORY-BASIS.md` and `docs/USA`, including CAI-USA-AI-Governance-and-Assurance (lifecycle and assurance gates).

Policy instruments in this list can change by executive action; their status is re-verified and recorded in the release notes of each gate.

## 4. Registry fields (targets) and sector model

For each registry entry listing `USA`, the registry authority signs:

| Field | Values |
|---|---|
| `usa_sector` | One of the sixteen identifiers below, or `none` |
| `usa_ot_asset` | Boolean: the target is an OT/ICS asset, regardless of sector |

Sector table (signed catalogue parameter, core SR-26.3):

| Identifier | Sector | SRMA | Consequence | OT-intensive |
|---|---|---|---|---|
| `chemical` | Chemical | CISA (DHS) | CATASTROPHIC | yes |
| `commercial_facilities` | Commercial Facilities | CISA (DHS) | MODERATE | no |
| `communications` | Communications | CISA (DHS) | HIGH | yes |
| `critical_manufacturing` | Critical Manufacturing | CISA (DHS) | HIGH | yes |
| `dams` | Dams | CISA (DHS) | CATASTROPHIC | yes |
| `defense_industrial_base` | Defense Industrial Base | Department of Defense | HIGH | yes |
| `emergency_services` | Emergency Services | CISA (DHS) | HIGH | no |
| `energy` | Energy | Department of Energy | CATASTROPHIC | yes |
| `financial_services` | Financial Services | Department of the Treasury | HIGH | no |
| `food_agriculture` | Food and Agriculture | USDA and HHS (FDA) | HIGH | yes |
| `government_facilities` | Government Facilities | CISA (DHS) and GSA | HIGH | no |
| `healthcare` | Healthcare and Public Health | Department of Health and Human Services | HIGH | no |
| `information_technology` | Information Technology | CISA (DHS) | HIGH | no |
| `nuclear` | Nuclear Reactors, Materials, and Waste | CISA (DHS) | CATASTROPHIC | yes |
| `transportation` | Transportation Systems | DHS (TSA, U.S. Coast Guard) and Department of Transportation | CATASTROPHIC | yes |
| `water` | Water and Wastewater Systems | Environmental Protection Agency | CATASTROPHIC | yes |

Sectors and SRMAs follow NSM-22 as listed by CISA; they are re-verified with the NSM-22 status before G4. Consequence and OT intensity are **CAI policy values**, not values stated by NSM-22; they are signed by the catalogue authority. Aliases are not resolved: a value outside the table makes the entry invalid.

## 5. Registration fields (AI systems)

For each AI system operating under `USA`, the catalogue authority signs:

| Field | Values | Source |
|---|---|---|
| `usa_prohibited_use` | `none` or a reason code | Unlawful or prohibited use designated by the deployment owner |
| `lifecycle_status` | `REGISTERED`, `VALIDATED`, `DEPLOYED`, `OPERATING`, `MONITORING`, `REVALIDATION`, `DECOMMISSIONED` | CAI USA baseline lifecycle |
| `validation_ref`, `validated_at`, `revalidation_due` | Reference with digest; dates | CAI USA baseline validation and revalidation |
| `model_version` | Registered version identifier | CAI USA baseline registration (no hot-swapping of models) |
| `risk_classification`, `authorized_automation_level` | CAI USA baseline registration fields | CAI USA baseline registration |
| `genai`, `provenance_required` | Boolean | NIST AI 600-1 |
| `rmf_profile_ref` | Reference to the deployment's AI RMF profile (MAP and MEASURE records) | NIST AI 100-1 |

## 6. Classification (USA-SR-01)

1. `CRITICAL_INFRASTRUCTURE` when `usa_sector ≠ none`, with consequence and OT intensity from the signed table.
2. `NON_CRITICAL` when `usa_sector = none`, which the registry authority states explicitly. A target without a valid entry is unclassified (core SR-10), never `NON_CRITICAL`.

## 7. Requirements

The CAI USA baseline defines four operational assurance gates. This profile interprets them for the engine as follows (CAI interpretation; the baseline's own wording is in its document): pre-inference — registration, lifecycle and model-version validity; inference — confidence, drift, explainability and provenance; action — automation authorization through SRMA, OT and approval rules; post-action — verification of the result.

**USA-SR-01 Classification** — §6, from signed fields only.

**USA-SR-02 Prohibited use** — `usa_prohibited_use ≠ none` gives DENY (`USA_PROHIBITED_USE`) for every operation.

**USA-SR-03 Pre-inference: lifecycle** — operational proposals are admitted only from systems in `DEPLOYED` or `OPERATING`. Systems in `REGISTERED`, `VALIDATED`, `MONITORING` or `REVALIDATION` may submit observation-only operations. A passed `revalidation_due`, or a drift-triggered revalidation (USA-SR-12), is treated as `REVALIDATION`. `DECOMMISSIONED` gives BLOCKED for every operation.

**USA-SR-04 Pre-inference: model version** — in profile P, a proposal whose declared `model_version` differs from the registered one is BLOCKED (`USA_MODEL_VERSION_MISMATCH`).

**USA-SR-05 Inference: assurance floor** — minimum confidence by consequence: CATASTROPHIC 0.95, HIGH 0.90; MODERATE and `NON_CRITICAL` use the core floor (0.80). Below the floor: DENY (`USA_ASSURANCE_FLOOR`). Declared drift above 0.15: DENY (`USA_ROBUSTNESS`). The core explainability gate applies with reason code `USA_EXPLAINABILITY` added for `CRITICAL_INFRASTRUCTURE`.

**USA-SR-06 Inference: generative-AI provenance presence** — when `genai` and `provenance_required` are true, a proposal without declared provenance information gives DENY (`USA_PROVENANCE_ABSENT`). This is a presence check of client-declared provenance, labelled `supports` NIST AI 600-1; it does not verify provenance. The core explainability gate also applies to generative systems.

**USA-SR-07 Action: SRMA oversight** — `CRITICAL_INFRASTRUCTURE` with an operational operation gives ESCALATE (`USA_SRMA_OVERSIGHT`); the approval request names the SRMA. Observation-only operations are not escalated by this gate and are recorded; other gates still apply.

**USA-SR-08 Action: OT/ICS safety** — an operational operation on a target with `usa_ot_asset = true`, or a destructive operation on an OT-intensive sector target, gives ESCALATE (`USA_OT_SAFETY`), independently of whether CORE_OT_SAFETY also triggers.

**USA-SR-09 Action: consequence-scaled approvals** — the profile's minimum for operational operations on CATASTROPHIC-consequence targets is two approvals from distinct principals.

**USA-SR-10 Post-action verification** — for `CRITICAL_INFRASTRUCTURE`, an EXECUTED decision that does not reach RESULT_VERIFIED within the window (default 24 hours) produces a `USA_POST_ACTION_UNVERIFIED` evidence record when the window expires.

**USA-SR-11 Gate failure review** — the CAI USA baseline requires human review when a gate fails. Every USA gate DENY records `USA_GATE_FAILURE_REVIEW` with the reason code; the review is closed by an approver-signed statement (core SR-23.3 mechanism).

**USA-SR-12 Drift-triggered revalidation** — a `USA_ROBUSTNESS` denial records `REVALIDATION_REQUIRED_BY_DRIFT` for the AI system; until a newer signed registration with a later `validated_at` is loaded, the system is treated as `REVALIDATION`.

**USA-SR-13 NIST AI RMF traceability** — each USA decision record carries a GOVERN, MAP, MEASURE and MANAGE trace referencing `rmf_profile_ref`, the classification, the measured inputs and the decision. The trace is labelled `supports`; it is not a gate and never states that the system is governed under or conforms to the framework.

**USA-SR-14 Retention and labels** — for deployments that include USA targets, a manifest with `retention_min_days` below 365 is refused at manifest load and at every registry reload (CAI policy; NIST SP 800-53 AU-11 leaves the period to the organization). Every USA gate result carries the instrument, `relationship` (`alignment` or `supports`) and the instrument status recorded at release; no result uses the words compliant, conformant or "governed under".

**USA-SR-15 Post-quantum timeline** — USA deployments use the core `hybrid` suite. NIST IR 8547 (initial public draft) proposes deprecating 112-bit classical public-key algorithms after 2030 and disallowing all quantum-vulnerable public-key algorithms, including 128-bit ones such as Ed25519, after 2035. The profile therefore sets `classical_suite_end` (core SR-26.1) to 1 January 2036 for USA deployments (refusing the `classical` suite in every profile from that date) and records the final IR 8547 dates when published. National security systems are not supported in 0.5.0 (core SR-25.8).

## 8. Thresholds

| Threshold | Value | Source |
|---|---|---|
| Assurance floor CATASTROPHIC / HIGH | 0.95 / 0.90 | CAI policy aligned to NIST AI RMF MEASURE (baseline `CONFIDENCE_FLOOR`) |
| Assurance floor MODERATE / NON_CRITICAL | Core floor 0.80 | Baseline values 0.80 / 0.70 are at or below the core floor and are not defined |
| Maximum declared drift | 0.15 | CAI policy (baseline `MAX_DRIFT`) |
| Minimum approvals, CATASTROPHIC | 2 | CAI policy |
| Post-action verification window | 24 hours | CAI policy |
| Minimum retention | 365 days | CAI policy |

All are signed catalogue parameters.

## 9. Post-quantum migration (USA)

| Instrument | Content relevant to the engine | Requirement in this profile |
|---|---|---|
| NIST IR 8547 (draft) | 112-bit classical algorithms deprecated after 2030; all quantum-vulnerable public-key algorithms disallowed after 2035 | Hybrid suite from release; `classical` refused for USA deployments from 1 January 2036, earlier if the final IR sets earlier dates |
| CNSA 2.0 (NSA) | ML-DSA-87, ML-KEM-1024, SHA-384/512, LMS/XMSS for software and firmware signing; exclusive use of these in the final phase | Not supported in 0.5.0 (`nss = true` refused); a future release needs a `pq-only` suite or a CNSA-listed classical component |

Firmware signing is outside this engine and follows its own specification.

## 10. Baseline findings (commit b52935e)

| ID | Finding | Evidence | Severity |
|---|---|---|---|
| USA-F-01 | An unknown or unresolvable sector is treated as `NON_CRITICAL` with the 0.70 floor. | `classify()`; executed: "enrgy" and "electric_grid" give NON_CRITICAL 0.70, "energy" gives CATASTROPHIC 0.95. | High |
| USA-F-02 | Free-text sectors are resolved through aliases; a variant outside the table downgrades the classification. | `ALIASES`, `resolve()`. | Medium |
| USA-F-03 | The `usa.nist_ai_rmf` gate returns ALLOW with "governed under NIST AI RMF". | `usa_gates()`. | Medium |
| USA-F-04 | SRMA oversight escalates every critical-infrastructure decision, including observation. | `usa_gates()`. | Medium |
| USA-F-05 | `genai` and provenance are client-declared. | Core F-15. | High |
| USA-F-06 | Consequence levels and OT intensity are CAI policy values presented as sector attributes, without signature. | `SECTORS`. | Medium |
| USA-F-07 | The lifecycle and assurance gates of the CAI USA baseline are not enforced (no lifecycle, no model-version binding, no review on gate failure, no drift-triggered revalidation, no post-action check). | Code and baseline document. | High |
| USA-F-08 | OT escalation in the USA layer requires an OT-intensive sector. | `usa_gates()`. | Low |
| USA-F-09 | `REGULATORY-BASIS.md` records NSM-22 as current without noting the review ordered by Executive Order 14239. | Repository document. | Medium |
| USA-F-10 | The Transportation Systems SRMA is recorded as "TSA and U.S. Coast Guard (DHS)"; CISA lists DHS and the Department of Transportation. | `usa_sectors.py`. | Low |

## 11. Acceptance tests

All tests use path A with signed test sources and run on Linux and Windows.

| Test | Gate | Requirement | Expected result |
|---|---|---|---|
| USA-AT-01 | G4 | USA-SR-02 | `usa_prohibited_use` set: BLOCKED for operational and observation operations. |
| USA-AT-02 | G4 | USA-SR-03 | Lifecycle REGISTERED, VALIDATED, MONITORING or REVALIDATION: operational BLOCKED, observation AUTHORIZED; DECOMMISSIONED: all BLOCKED; DEPLOYED or OPERATING: evaluated normally. |
| USA-AT-03 | G4 | USA-SR-03 | `revalidation_due` in the past: treated as REVALIDATION. |
| USA-AT-04 | G8 | USA-SR-04 | Profile P: declared `model_version` differing from the registration: BLOCKED (USA_MODEL_VERSION_MISMATCH). |
| USA-AT-05 | G4 | USA-SR-05 | `energy` target, confidence 0.94: BLOCKED; 0.95: floor passed. HIGH-consequence 0.89: BLOCKED; 0.90: passed. MODERATE or NON_CRITICAL 0.79: BLOCKED by the core floor. |
| USA-AT-06 | G4 | USA-SR-05 | Declared drift 0.16: BLOCKED (USA_ROBUSTNESS); critical-infrastructure target with registration `explainable = false`: BLOCKED with CORE_AI_EXPLAINABILITY and USA_EXPLAINABILITY. |
| USA-AT-07 | G4 | USA-SR-06 | `genai` with `provenance_required` and no provenance: BLOCKED (USA_PROVENANCE_ABSENT); result labelled `supports`. |
| USA-AT-08 | G4 | USA-SR-07 | Critical-infrastructure target, operational operation: escalation USA_SRMA_OVERSIGHT; observation: AUTHORIZED (closes USA-F-04). |
| USA-AT-09 | G4 | USA-SR-08 | `usa_ot_asset = true` in `commercial_facilities`, operational operation: escalation with reason code USA_OT_SAFETY (closes USA-F-08); destructive operation on a `water` target: reason code USA_OT_SAFETY present (CORE_OPERATIONAL_IMPACT may also be present). |
| USA-AT-10 | G5 | USA-SR-07, USA-SR-09 | Approval request for a critical-infrastructure decision names the SRMA; CATASTROPHIC target: one approval insufficient, two distinct principals accepted. |
| USA-AT-11 | G7 | USA-SR-10 | Critical-infrastructure decision EXECUTED without RESULT_VERIFIED after the window: USA_POST_ACTION_UNVERIFIED evidence record written at expiry. |
| USA-AT-12 | G4 | USA-SR-01 | Sector value outside the table (including a former alias such as `electricity`): entry invalid; target without an entry handled as unclassified (closes USA-F-01, USA-F-02). |
| USA-AT-13 | G4 | USA-SR-13 | Every USA decision record carries the four-function trace referencing `rmf_profile_ref`; no gate named after the RMF (closes USA-F-03). |
| USA-AT-14 | G4 | USA-SR-01 | Sector table altered without a valid catalogue signature: catalogue invalid (closes USA-F-06, signature part). |
| USA-AT-15 | G5 | USA-SR-01 | Signed change of a consequence level while decisions are pending: recorded and triggers revalidation (closes USA-F-06, revalidation part). |
| USA-AT-16 | G5 | USA-SR-11, USA-SR-12 | A USA gate DENY records USA_GATE_FAILURE_REVIEW, closed by an approver statement; a USA_ROBUSTNESS denial records REVALIDATION_REQUIRED_BY_DRIFT and the system is treated as REVALIDATION until a newer registration (closes USA-F-07). |
| USA-AT-17 | G4 | USA-SR-14 | Manifest with `retention_min_days = 364` for a USA deployment: refused; every USA gate result carries instrument, relationship and status; text scan finds no compliant, conformant or "governed under". |
| USA-AT-18 | G4 | USA-SR-15 | Clock at 1 January 2036: `classical` suite refused in profile D for a USA deployment; on 31 December 2035: accepted; `nss = true`: engine refuses to start; `crypto-inventory` lists every key, algorithm, suite and purpose. |

USA-F-09 and USA-F-10 are closed by corrections to `REGULATORY-BASIS.md` and `usa_sectors.py` in G4, verified in its release review.

## 12. Traceability

| Requirement | Instrument or source | Findings | Tests |
|---|---|---|---|
| USA-SR-01 | NSM-22 sectors and SRMAs; CAI policy for consequence and OT | USA-F-01, USA-F-02, USA-F-06, USA-F-10 | USA-AT-12, USA-AT-14, USA-AT-15 |
| USA-SR-02 | Deployment owner's designation | — | USA-AT-01 |
| USA-SR-03, USA-SR-04 | CAI USA baseline registration and lifecycle | USA-F-07 | USA-AT-02 to USA-AT-04 |
| USA-SR-05 | NIST AI RMF MEASURE; CAI USA baseline | — | USA-AT-05, USA-AT-06 |
| USA-SR-06 | NIST AI 600-1 (presence check) | USA-F-05 | USA-AT-07 |
| USA-SR-07 | NSM-22 SRMA roles | USA-F-04 | USA-AT-08, USA-AT-10 |
| USA-SR-08 | NIST SP 800-82 Rev. 3 | USA-F-08 | USA-AT-09 |
| USA-SR-09 | CAI policy | — | USA-AT-10 |
| USA-SR-10 | CAI USA baseline post-action gate | USA-F-07 | USA-AT-11 |
| USA-SR-11, USA-SR-12 | CAI USA baseline (review on gate failure; drift suspends automation) | USA-F-07 | USA-AT-16 |
| USA-SR-13 | NIST AI RMF functions | USA-F-03 | USA-AT-13 |
| USA-SR-14 | NIST SP 800-53 AU-11 (CAI policy period); core SR-26.4 | USA-F-03, USA-F-09 | USA-AT-17 |
| USA-SR-15 | NIST IR 8547 (draft); CNSA 2.0 | — | USA-AT-18 |

## 13. Residual risks

- Classification depends on signed registry and registration data; the engine applies it faithfully, including any error.
- Consequence levels, OT intensity, thresholds and the retention period are CAI policy.
- NSM-22 may be revised following Executive Order 14239; CNSA 2.0 dates and the final NIST IR 8547 must be confirmed from primary sources at each release.
- Lifecycle status and validation are attested by the catalogue authority; the engine does not verify the underlying validation work.

## 14. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Owner | Antonio José Socorro Marín | Pending | |
