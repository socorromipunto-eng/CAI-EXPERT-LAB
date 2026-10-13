# CAI Engine — MCP Security Specification: EU Jurisdiction Profile

| Field | Value |
|---|---|
| Document ID | CAI-ENG-SEC-001-EU |
| Version | 0.4 |
| Status | PROPOSED — requires owner approval before any implementation |
| Classification | Public (repository document) |
| Project | CAI-EXPERT-LAB / CAI-Engine |
| Phase | Proposed specification for cai-engine 0.5.0; owner approval pending (gate G0) |
| Core specification | CAI-ENG-SEC-001 v0.8 (profile interface SR-26, core gates SR-27) |
| Companion profile | CAI-ENG-SEC-001-USA (equal rank) |
| Baseline | Git commit b52935e (`cai_engine/eu_ai_act.py`) |
| Owner | Antonio José Socorro Marín |
| Prepared by | Antonio José Socorro Marín |
| Date | 2026-10-13 |

Copyright © 2026 Antonio José Socorro Marín. All rights reserved. Use is governed by the legal documents in the `/legal` directory of this repository.

## Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-12 | First version: 9 findings, 10 requirements, 12 tests. |
| 0.2 | 2026-10-12 | Revision after review: target-based Annex III(2) rule labelled CAI policy; Art. 6(3)/6(4) assessment reference; corrected EU-F-03 (Art. 12 and Art. 50 gate outputs); Art. 50 provider and deployer duties separated; limited-risk confidence floor removed (the core floor of 0.80 already applies); parity with the USA profile: model-version binding and substantial modification, two-person verification for remote biometric identification (Art. 14(5)), drift-triggered revalidation, post-action verification for high-risk decisions; retention enforced through the manifest field; post-quantum dates labelled CAI policy and aligned on 1 January 2031; public-authority date reworded. 9 findings, 14 requirements, 16 tests. |
| 0.3 | 2026-10-12 | Consistency corrections: two-person rule labelled CAI policy aligned to Art. 14(5); `classical_suite_end` used; EU-F-10 added (Art. 111(2) wording in `REGULATORY-BASIS.md`); EU-AT-13 moved to G8; observation wording. 10 findings, 14 requirements, 16 tests. |
| 0.4 | 2026-10-13 | Published in the repository (CHG-2026-10-13-01): header block completed (Phase, Owner, Prepared by); core reference updated to v0.8. Regulatory dates of §3 checked on 2026-10-13 against published summaries of Regulation (EU) 2026/1744 (published 24 July 2026, in force 27 July 2026); no change needed. No requirement, finding or test changed. |

---

## 1. Purpose and relationship to the core

This profile defines how the CAI Engine evaluates AI-assisted security decisions on targets registered under the profile identifier `EU`. It implements the core profile interface (CAI-ENG-SEC-001 SR-26): it adds classification rules, gates, thresholds, approval minimums, retention and a post-quantum timeline, and never relaxes a core control or a core gate (SR-27).

The profile expresses **alignment** with the instruments in §3. Gate results state `alignment` or `supports`; they never state that an obligation is satisfied or that a system is compliant (core SR-26.4). Legal classification is a human judgment recorded by registry and catalogue authorities in signed sources; the engine applies it faithfully and does not provide legal advice. Where this profile applies a rule more broadly than the Regulation, the rule is labelled **CAI policy**.

## 2. Scope

In scope: classification under Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744; gates derived from Articles 5, 6 and Annex III, 9 to 15, 19, 26 and 50; model-version binding; post-action verification; evidence retention; the post-quantum timeline.

Out of scope: conformity assessment, CE marking, registration in the EU database, post-market monitoring systems (Art. 72), serious-incident reporting (Art. 73), obligations of general-purpose AI model providers (Arts. 53 and 55), NIS2 reporting and Cyber Resilience Act product obligations.

## 3. References

- Regulation (EU) 2024/1689 (Artificial Intelligence Act), as amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI), in force 27 July 2026.
- Directive (EU) 2022/2555 (NIS2), for the `nis2_entity` context field only.
- NIS Cooperation Group, A Coordinated Implementation Roadmap for the Transition to Post-Quantum Cryptography (June 2025).
- CAI-EXPERT-LAB `REGULATORY-BASIS.md` (verified 2026-10-11) and `docs/EU`.

Application dates (from `REGULATORY-BASIS.md`; re-verified at each gate release):

| Obligation | Applies from |
|---|---|
| Prohibited practices (Art. 5) | 2 Feb 2025 |
| Art. 5 prohibitions added by Regulation (EU) 2026/1744 | 2 Dec 2026 |
| Transparency (Art. 50) | 2 Aug 2026 (Art. 50(2) grace for legacy generative AI until 2 Dec 2026) |
| High-risk, Annex III stand-alone systems | 2 Dec 2027 |
| High-risk, Annex I product-embedded systems | 2 Aug 2028 |
| High-risk systems placed on the market before 2 Aug 2026 and intended for use by public authorities (Art. 111(2)) | 2 Aug 2030 (effect of the Omnibus on this provision to be verified) |

The engine applies this profile's gates as CAI policy from release, including before legal application; every gate record carries `legal_application_date`.

## 4. Registry fields (targets)

For each registry entry listing `EU`, the registry authority signs:

| Field | Values | Purpose |
|---|---|---|
| `eu_critical_infrastructure_type` | `critical_digital_infrastructure`, `road_traffic`, `water_supply`, `gas_supply`, `heating_supply`, `electricity_supply`, `none` | The categories named in Annex III point 2 |
| `eu_safety_component_basis` | Reference (at most 256 characters) | How the safety-component definition, as amended by Regulation (EU) 2026/1744, was applied |
| `eu_remote_biometric_identification` | Boolean | The target is used for remote biometric identification (Annex III point 1(a)) |
| `nis2_entity` | `essential`, `important`, `none` | Context only |

## 5. Registration fields (AI systems)

For each AI system operating under `EU`, the catalogue authority signs:

| Field | Values | Article |
|---|---|---|
| `eu_role` | `provider`, `deployer`, `provider_and_deployer` | Art. 3 |
| `eu_prohibited_practice` | `none`, or one of `art5_1_a` to `art5_1_h`, `art5_omnibus_ncii`, `art5_omnibus_csam` | Art. 5 |
| `eu_annex_iii_areas` | Subset of `biometrics`, `critical_infrastructure`, `education`, `employment`, `essential_services`, `law_enforcement`, `migration_border`, `justice_democracy` (intended purpose) | Art. 6(2), Annex III points 1 to 8 |
| `eu_art6_3_assessment_ref` | Reference with digest, required when the authority judges that an Annex III use is not high-risk | Art. 6(3), 6(4) |
| `interacts_with_persons`, `generates_synthetic_content` | Boolean | Art. 50 |
| `eu_transparency_measures` | Boolean: the provider design measures of Art. 50(1) and (2) and, where the deployer duties of Art. 50(3) and (4) apply, the deployer information measures are in place | Art. 50 |
| `eu_high_risk_documentation` | References with digests: risk-management system, data governance, technical documentation, instructions for use, declared accuracy metrics | Arts. 9, 10, 11, 13, 15 |
| `model_version` | Registered model version identifier | Art. 3(23), Art. 43(4) (substantial modification) |
| `eu_substantial_modification_ref` | Reference to the assessment made when `model_version` changed | Art. 43(4) |

## 6. Classification (EU-SR-01)

1. `UNACCEPTABLE` if `eu_prohibited_practice ≠ none`.
2. Otherwise `HIGH` if `eu_annex_iii_areas` is not empty (legal classification of the intended purpose by the catalogue authority).
3. Otherwise `HIGH` as **CAI policy aligned to Annex III point 2** if any target has `safety_component = true` and `eu_critical_infrastructure_type ≠ none`: an AI system acting on a safety component of critical infrastructure is treated as high-risk for that decision, whatever its registered intended purpose.
4. Otherwise `LIMITED` if `interacts_with_persons` or `generates_synthetic_content`.
5. Otherwise `MINIMAL`.

An authority that judges an Annex III use not high-risk under Art. 6(3) records the assessment in `eu_art6_3_assessment_ref`; without it, a registration that describes an Annex III use but lists no area is invalid. The engine does not evaluate Art. 6(3) itself.

## 7. Requirements

**EU-SR-01 Classification** — §6, from signed fields only.

**EU-SR-02 Art. 5** — `UNACCEPTABLE` gives DENY (`EU_ART5`) for every operation, including observation.

**EU-SR-03 Art. 14 human oversight** — `HIGH` gives ESCALATE (`EU_ART14`) for every operational operation. Observation-only operations under `HIGH` are not escalated by this gate and are recorded with the classification; other gates still apply.

**EU-SR-04 Art. 15 accuracy and robustness** — under `HIGH`: confidence below 0.90 gives DENY (`EU_ART15_ACCURACY`); declared model drift above 0.15 gives DENY (`EU_ART15_ROBUSTNESS`). Both inputs are client-declared and can only deny.

**EU-SR-05 Art. 13 transparency to deployers** — under `HIGH`, the core explainability gate (CORE_AI_EXPLAINABILITY) applies with the reason code `EU_ART13` added.

**EU-SR-06 High-risk documentation** — under `HIGH`, an operational operation is BLOCKED (`EU_HIGH_RISK_DOCUMENTATION_MISSING`) unless all references of `eu_high_risk_documentation` are present and signed. The engine checks presence and signature, not adequacy.

**EU-SR-07 Art. 50 transparency** — under `LIMITED`, `eu_transparency_measures = false` gives ESCALATE (`EU_ART50`). No limited-risk confidence floor is defined; the core floor (0.80) applies.

**EU-SR-08 Record-keeping and retention (Arts. 12, 19, 26(6))** — every EU decision record carries the classification, gate results and `legal_application_date`, and its record-keeping relationship is `supports`. For deployments that include EU targets, a manifest with `retention_min_days` below 183 is refused, at manifest load and at every registry reload (core SR-06.5). The engine has no deletion path; retention of archives is otherwise a deployment process control.

**EU-SR-09 Post-quantum timeline (CAI policy)** — EU deployments use the core `hybrid` suite. The profile sets `classical_suite_end` to 1 January 2031: from that date the `classical` suite is refused in every profile for deployments that include EU targets. This extends to every EU deployment of the engine the roadmap's statement that quantum-vulnerable public-key mechanisms shall not be used stand-alone after the end of 2030, which the roadmap addresses to high-risk use cases. `crypto-inventory` (core §12.3) supports the roadmap's 2026 inventory milestone.

**EU-SR-10 Labels and dates** — every EU gate result carries the article reference, `relationship` (`alignment` or `supports`) and `legal_application_date`; no result uses the words compliant, satisfied or conformant.

**EU-SR-11 Model version and substantial modification** — in profile P, a proposal whose declared `model_version` differs from the registered one is BLOCKED (`EU_MODEL_VERSION_MISMATCH`); a registration change of `model_version` without `eu_substantial_modification_ref` is invalid.

**EU-SR-12 Two-person verification (CAI policy aligned to Art. 14(5))** — Art. 14(5) requires separate verification by two natural persons of actions or decisions based on an identification by a remote biometric identification system, with derogations for law enforcement, migration and border control. As CAI policy, the profile extends a two-approval minimum to operational security operations on targets with `eu_remote_biometric_identification = true` under `HIGH`.

**EU-SR-13 Drift-triggered revalidation (CAI policy aligned to Art. 15)** — an EU_ART15_ROBUSTNESS denial records `REVALIDATION_REQUIRED_BY_DRIFT` for the AI system; until a newer signed registration is loaded, the system may submit observation-only operations only.

**EU-SR-14 Post-action verification (CAI policy)** — for `HIGH` decisions, an EXECUTED decision that does not reach RESULT_VERIFIED within the configured window (default 24 hours) produces an `EU_POST_ACTION_UNVERIFIED` evidence record when the window expires.

## 8. Thresholds

| Threshold | Value | Source |
|---|---|---|
| High-risk minimum confidence | 0.90 | CAI policy aligned to Art. 15 (baseline `HIGH_MIN_CONFIDENCE`) |
| Maximum declared model drift (high-risk) | 0.15 | CAI policy aligned to Art. 15 (baseline `MAX_DRIFT`) |
| Minimum approvals, remote biometric identification targets | 2 | CAI policy aligned to Art. 14(5) |
| Post-action verification window | 24 hours | CAI policy |
| Minimum retention | 183 days | Arts. 19(1) and 26(6) (at least six months) |

The baseline limited-risk floor of 0.70 is not carried over: it is below the core floor and would have no effect.

## 9. Post-quantum migration (EU)

| Roadmap milestone (NIS Cooperation Group) | Requirement in this profile |
|---|---|
| By end of 2026: national stakeholders identified, cryptographic inventories and dependency maps, awareness programmes | `crypto-inventory` from G3 |
| By end of 2030: quantum-safe upgrade path for high-risk use cases; quantum-vulnerable public-key mechanisms not used stand-alone | Hybrid suite mandatory in profile P from release; `classical` refused in all profiles for EU deployments from 1 January 2031 (CAI policy) |
| By end of 2035: medium-risk use cases | Met by the hybrid suite; transition to `pq-only` to be evaluated before 2035 |

## 10. Baseline findings (commit b52935e)

| ID | Finding | Evidence | Severity |
|---|---|---|---|
| EU-F-01 | Annex III covers 4 of 8 areas. | `ANNEX_III` in `eu_ai_act.py`, declared a subset in its comment. | Medium |
| EU-F-02 | The critical-infrastructure set differs from Annex III point 2 (it includes healthcare, banking, financial market, transport in general and communications). Stricter, but the traceability label is inaccurate. | `CRITICAL_SECTORS`. | Medium |
| EU-F-03 | Gate outputs imply satisfaction: the Art. 12 gate returns ALLOW ("decision recorded in hash-chained evidence log (Art. 12)") under a code comment stating record-keeping "is satisfied", and the Art. 50 gate returns ALLOW with "transparency satisfied". | `eu_gates()`; Art. 50 output executed. | Medium |
| EU-F-04 | Arts. 9 to 11 are listed as obligations but not checked. | `HIGH_RISK_OBLIGATIONS` used only as labels. | Medium |
| EU-F-05 | Provider and deployer roles are not modelled. | No role field. | Low |
| EU-F-06 | Legal application dates are not represented. | No date fields. | Low |
| EU-F-07 | Classification inputs and `human_disclosed` are client-declared. | Core F-01, F-15. | Critical |
| EU-F-08 | Art. 6(3) and 6(4) are not modelled. | No assessment reference. | Low |
| EU-F-09 | Model version is not bound to a registration; substantial modification is not represented. | `model_version` client-declared. | Medium |
| EU-F-10 | `REGULATORY-BASIS.md` describes the 2 Aug 2030 date as applying to "public-authority systems"; Art. 111(2) concerns high-risk systems placed on the market before 2 Aug 2026 and intended for use by public authorities. | Repository document. | Low |

## 11. Acceptance tests

All tests use path A with signed test sources and run on Linux and Windows.

| Test | Gate | Requirement | Expected result |
|---|---|---|---|
| EU-AT-01 | G4 | EU-SR-02 | `eu_prohibited_practice = art5_1_a`: BLOCKED (EU_ART5) for operational and observation operations. |
| EU-AT-02 | G4 | EU-SR-02 | `art5_omnibus_ncii`, `art5_omnibus_csam` accepted; any other identifier makes the registration invalid. |
| EU-AT-03 | G4 | EU-SR-01, EU-SR-03 | Registration with `critical_infrastructure` in `eu_annex_iii_areas`, documentation present, confidence 0.97, explanation present, operational operation: PENDING_APPROVAL (EU_ART14). |
| EU-AT-04 | G4 | EU-SR-01 | Registration without Annex III areas, target `safety_component = true`, `electricity_supply`: HIGH with label "CAI policy aligned to Annex III point 2". |
| EU-AT-05 | G4 | EU-SR-04 | As EU-AT-03 with confidence 0.89: BLOCKED (EU_ART15_ACCURACY); with declared drift 0.16: BLOCKED (EU_ART15_ROBUSTNESS). |
| EU-AT-06 | G4 | EU-SR-05 | As EU-AT-03 with registration `explainable = false`, or empty explanation: BLOCKED with CORE_AI_EXPLAINABILITY and EU_ART13. |
| EU-AT-07 | G4 | EU-SR-06 | As EU-AT-03 with one documentation reference missing: BLOCKED (EU_HIGH_RISK_DOCUMENTATION_MISSING); observation on the same target: AUTHORIZED. |
| EU-AT-08 | G4 | EU-SR-01 | Each of the 8 Annex III areas gives HIGH (closes EU-F-01); free-text infrastructure type: entry invalid (closes EU-F-02); Annex III use without areas and without `eu_art6_3_assessment_ref`: registration invalid (closes EU-F-08). |
| EU-AT-09 | G4 | EU-SR-07 | LIMITED with `eu_transparency_measures = false`: escalation (EU_ART50); with `true` and confidence 0.80: no EU escalation; confidence 0.79: BLOCKED by the core floor. |
| EU-AT-10 | G4 | EU-SR-01 | MINIMAL: no EU gate; core gates still apply. |
| EU-AT-11 | G4 | EU-SR-08, EU-SR-10 | Every EU gate result carries article, relationship and `legal_application_date`; text scan finds no compliant, satisfied or conformant (closes EU-F-03, EU-F-06). |
| EU-AT-12 | G4 | EU-SR-08, EU-SR-09 | Manifest with `retention_min_days = 182` for an EU deployment: refused. Clock at 1 January 2031: `classical` suite refused in profile D for an EU deployment; on 31 December 2030: accepted. |
| EU-AT-13 | G8 | EU-SR-11 | Profile P: declared `model_version` differing from the registration: BLOCKED (EU_MODEL_VERSION_MISMATCH); registration changing `model_version` without `eu_substantial_modification_ref`: invalid (closes EU-F-09). |
| EU-AT-14 | G5 | EU-SR-12 | Remote biometric identification target under HIGH: one approval insufficient; two distinct principals: AUTHORIZED. |
| EU-AT-15 | G4 | EU-SR-13 | After an EU_ART15_ROBUSTNESS denial: REVALIDATION_REQUIRED_BY_DRIFT recorded; operational proposals from that system BLOCKED, observation allowed, until a newer signed registration is loaded. |
| EU-AT-16 | G7 | EU-SR-14 | HIGH decision EXECUTED without RESULT_VERIFIED after the window: EU_POST_ACTION_UNVERIFIED evidence record written at expiry. |

EU-F-10 is closed by the correction of `REGULATORY-BASIS.md` in G4, verified in its release review.

## 12. Traceability

| Requirement | Instrument | Findings | Tests |
|---|---|---|---|
| EU-SR-01 | Art. 6(2), 6(3), 6(4), Annex III | EU-F-01, EU-F-02, EU-F-07, EU-F-08 | EU-AT-03, EU-AT-04, EU-AT-08, EU-AT-10 |
| EU-SR-02 | Art. 5 and Regulation (EU) 2026/1744 additions | EU-F-07 | EU-AT-01, EU-AT-02 |
| EU-SR-03 | Art. 14 | — | EU-AT-03 |
| EU-SR-04 | Art. 15 | — | EU-AT-05 |
| EU-SR-05 | Art. 13 | — | EU-AT-06 |
| EU-SR-06 | Arts. 9, 10, 11, 13, 15 | EU-F-04 | EU-AT-07 |
| EU-SR-07 | Art. 50 | EU-F-07 | EU-AT-09 |
| EU-SR-08 | Arts. 12, 19, 26(6) | EU-F-03 | EU-AT-11, EU-AT-12 |
| EU-SR-09 | NIS Cooperation Group roadmap (CAI policy) | — | EU-AT-12 |
| EU-SR-10 | Core SR-26.4 | EU-F-03, EU-F-06 | EU-AT-11 |
| EU-SR-11 | Arts. 3(23), 43(4) | EU-F-09 | EU-AT-13 |
| EU-SR-12 | Art. 14(5) (CAI policy extension) | — | EU-AT-14 |
| EU-SR-13 | Art. 15 (CAI policy) | — | EU-AT-15 |
| EU-SR-14 | CAI policy | — | EU-AT-16 |

## 13. Residual risks

- Classification depends on the correctness of signed registry and registration data; a wrong legal judgment is applied faithfully.
- The engine checks the presence of documentation references, not their adequacy.
- Thresholds other than retention are CAI policy, not values set by the Regulation.
- Obligations of general-purpose AI model providers used by AI clients are outside this profile.

## 14. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Owner | Antonio José Socorro Marín | Pending | |
