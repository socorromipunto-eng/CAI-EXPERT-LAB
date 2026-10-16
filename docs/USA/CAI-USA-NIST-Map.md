# CAI-USA-NIST-Map

Cybersecurity Artificial Intelligence Framework – NIST Control and Outcome Map (USA)  
Version 0.1 (Draft)

Author: Antonio José Socorro Marín  
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)  

Copyright © 2026 Antonio José Socorro Marín.  
All rights reserved.  
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.  

**NOTE**  
The normative language of CAI-EXPERT-LAB documentation is English.  
This document maps CAI to NIST controls and outcomes item by item and states, for each item, what CAI implements, specifies or only describes.  
It does not assert compliance, certification, accreditation, or regulatory approval.  

## 1. Purpose

CAI-USA-Definition section 4 states that CAI aligns operationally with NIST publications. This document makes that statement checkable. For each NIST control, subcategory or tenet it gives a status, the CAI element concerned and the evidence in this repository, or states that CAI does not address it.

This document is phase 1 of the external-control mapping (repository audit finding AUD-03). It covers NIST SP 800-53 Rev. 5, NIST CSF 2.0, NIST AI RMF 1.0 and NIST SP 800-207. The CISA, CMMC, OT and NASA references follow in later phases.

## 2. Sources

Every identifier and every quoted statement comes from the official source below, retrieved on 2026-10-16.

- NIST SP 800-53 Rev. 5, OSCAL catalog version 5.2.0 (last modified 2026-05-11), `nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json` in https://github.com/usnistgov/oscal-content. Control identifiers and titles in section 5.
- NIST Cybersecurity Framework 2.0 (NIST CSWP 29), OSCAL catalog version 1.2.0 (last modified 2026-05-11), `nist.gov/CSF/v2.0/json/NIST_CSF_v2.0_catalog.json` in the same repository. The 106 subcategories that are not withdrawn, with their statement text, in section 6.
- NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0), January 2023: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf; core subcategories as published at https://airc.nist.gov/airmf-resources/airmf/5-sec-core/. The 72 subcategories in section 7.
- NIST SP 800-207, Zero Trust Architecture, August 2020: https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf, section 2.1 (tenets) and section 3 (logical components). Section 8.

## 3. Method

Evidence base: commit 64a5ecd, CAI-Engine 0.4.2 (`CAI-Engine/implementation/cai_engine`), its tests, and the security specification `CAI-Engine/specifications/CAI-ENG-SEC-001-Core.md` (v0.8) with the USA profile (v0.4).

Status values:

- Implemented: done by the engine (or, for development and change controls, by the repository process), and exercised by a test in the repository.
- Partial: part of the item is implemented and tested; the limit is stated.
- Specified: required by CAI-ENG-SEC-001 (requirement or section given); not implemented in engine 0.4.2.
- Described: present only in CAI documents.
- Not addressed: CAI does not cover the item.

Evidence references: `test_cai_engine.py::name`, `TSM::name` (tests/TEST_SPECIFICATION_MATRIX.py) and `TEC::name` (tests/TEST_EVIDENCE_AND_CONTRACTS.py). "xfail" names a known gap that the test suite records as an expected failure (`xfail(strict=True)`), so that fixing the gap makes the suite fail until the status here is updated.

Two limits apply to every row. The engine records decisions; it performs no action on any system, because the adapters that would act are specified (SR-21) and not implemented. Most inputs (entry-condition facts, AI confidence, drift, deployment context) are declared by the caller, not observed by the engine.

## 4. Summary

Table 1 — Number of mapped items by status.

| Framework | Items | Implemented | Partial | Specified | Described | Not addressed |
|---|---|---|---|---|---|---|
| NIST SP 800-53 Rev. 5 (selected controls, section 5) | 28 | 1 | 15 | 10 | 2 | 0 |
| NIST CSF 2.0 (all subcategories) | 106 | 1 | 23 | 4 | 2 | 76 |
| NIST AI RMF 1.0 (all subcategories) | 72 | 0 | 14 | 4 | 2 | 52 |
| NIST SP 800-207 (tenets and logical components) | 8 | 0 | 5 | 1 | 0 | 2 |

No item is Implemented without a test in the repository that exercises it. Most CSF 2.0 and AI RMF outcomes are organizational; CAI does not address them, and this map says so instead of claiming them.

## 5. NIST SP 800-53 Rev. 5

Selection rule: the controls that the engine, the security specification or the CAI change process touch, plus the controls cited in CAI-ENG-SEC-001. A control not listed is not addressed by CAI. CAI is not a system security plan and does not implement control baselines.

Table 2 — Selected SP 800-53 Rev. 5 controls.

| Control | Title | Status | CAI element | Evidence | Limit or gap |
|---|---|---|---|---|---|
| AC-3 | Access Enforcement | Partial | Policy gate `policy.state_constraint` (gates.py) denies any action category not permitted in the current lifecycle state. | TSM::test_policy_state_constraint; test_cai_engine.py::test_policy_blocks_eradication_in_model | Authorizes action categories, not subjects: the engine does not identify who submits a proposal. |
| AC-5 | Separation of Duties | Partial | AI clients and human approvers use different channels: the MCP server has no approval tool; approve() refuses an empty approver name. Role and key separation are specified (SR-15; CAI-ENG-SEC-001 Core section 6.3). | test_cai_engine.py::test_mcp_server_exposes_no_approval_tool; TSM::test_mcp_exposes_no_approval_tool | The approver name is free text and is not authenticated; deny() accepts an empty name; pending approvals never expire (xfail SGH 5.2). |
| AC-6 | Least Privilege | Specified | Privilege separation of the engine service (CAI-ENG-SEC-001 Core section 6.5, profile P). | — | Not implemented in engine 0.4.2. |
| AU-2 | Event Logging | Partial | Event types logged: ENGINE_INIT, FACT_SET, TELEMETRY_ACCEPTED/REJECTED, ACTION_*, HUMAN_APPROVAL/DENIAL, STATE_TRANSITION, TRANSITION_BLOCKED, GOVERNED_DECISION_*. | TEC::test_init_event, test_fact_event, test_telemetry_events, test_transition_events_and_results, test_proposal_events, test_pending_approve_and_deny_events, test_governed_events | Refused requests (invalid category, unknown state, unknown action id, missing approver) are not logged; init() deletes an existing log (xfail F-03). |
| AU-3 | Content of Audit Records | Partial | Each record holds sequence number, timestamp, event type, payload (gate results, reasons, regulatory block, approver). | TEC::test_every_record_has_exactly_the_documented_fields | The source of a FACT_SET (who asserted the fact) is not recorded. |
| AU-4 | Audit Log Storage Capacity | Specified | Cited in CAI-ENG-SEC-001 Core section 3. The specification has no capacity requirement; the closest is SAFE_HALT on any evidence write failure (SR-17), which is this map's reading. | — | Not implemented. |
| AU-5 | Response to Audit Logging Process Failures | Specified | Evidence before effect and SAFE_HALT on evidence write failure (CAI-ENG-SEC-001 Core SR-16, SR-17). | — | approve() saves state before writing evidence; a failure in between leaves them inconsistent (audit AUD-14). |
| AU-6 | Audit Record Review, Analysis, and Reporting | Partial | `report()` produces a Markdown report of every record; `verify()` checks the chain. | TEC::test_report_lists_every_record, test_verify_contract | No analysis or correlation of records. |
| AU-8 | Time Stamps | Partial | Records carry a local `time.time()` timestamp. | TEC::test_timestamps_never_go_backwards | No time source synchronization or trusted time stamp; an RFC 3161 token in anchor records is optional (CAI-ENG-SEC-001 Core section 8.4). |
| AU-9 | Protection of Audit Information | Partial | SHA-256 hash chain: editing, deleting, swapping a record is detected by `verify()`. | TSM::test_editing_any_record_is_detected, test_deleting_any_non_final_record_is_detected, test_swapping_adjacent_records_is_detected | Truncating the last records and rewriting the whole chain are not detected (xfail NEW-06, T-08); init() truncates an existing log (xfail F-03). |
| AU-9(3) | Cryptographic Protection | Specified | Signed checkpoints and anchors (CAI-ENG-SEC-001 Core SR-19, SR-20, section 10). | — | Chain is not signed. |
| AU-10 | Non-repudiation | Specified | Signed approval statements (SR-14, section 8.1). | — | Approvals are not signed; the approver can repudiate. |
| AU-11 | Audit Record Retention | Specified | Minimum retention in the trust manifest (USA profile USA-SR-14). | — | No retention control. |
| AU-12 | Audit Record Generation | Partial | A record is generated for every state-changing engine operation listed under AU-2. | TEC::test_sequence_numbers_are_contiguous_from_one, test_report_lists_every_record | Read-only operations and refused requests generate no record. |
| CA-7 | Continuous Monitoring | Described | Continuous monitoring is described in CAI-Core-Operations and the USA baseline. | — | Not implemented. |
| CM-3 | Configuration Change Control | Partial | Changes to CAI itself: numbered CHG commits, signed, one entry per change in CAI-Core-Evolution-Traceability-Register, tests and lint on every push and pull request to main. | .github/workflows/CAI-ENGINE-TESTS.yml; docs/CORE/CAI-Core-Evolution-Traceability-Register.md | Applies to the CAI repository, not to systems the engine governs. |
| CM-5 | Access Restrictions for Change | Specified | Protected paths and code integrity (CAI-ENG-SEC-001 Core section 6.4). | — | Not implemented. |
| IA-2 | Identification and Authentication (Organizational Users) | Specified | Approver authentication by signature with hardware-backed keys (SR-14). | — | Not implemented. |
| IA-5 | Authenticator Management | Specified | Key management by purpose and rotation (CAI-ENG-SEC-001 Core section 6.3, SR-23). | — | Not implemented. |
| IR-4 | Incident Handling | Partial | The lifecycle MODEL to RESTORE orders response phases; containment, eradication and recovery categories are permitted only in ISOLATE, EVICT and RESTORE; transitions require entry conditions. | TSM::test_transition_matrix, test_entry_condition_missing_blocks, test_policy_state_constraint; test_cai_engine.py::test_full_lifecycle_to_evict | Entry conditions are booleans set by the caller (`set_fact`); the engine records decisions but performs no action. |
| RA-3 | Risk Assessment | Described | Threat models: USA baseline and sector Threat-and-Assumption models; engine threat model in CAI-ENG-SEC-001 Core section 5. | — | No risk assessment is computed. |
| SA-11 | Developer Testing and Evaluation | Implemented | Developer testing of the engine: 665 test cases (652 pass; 13 xfail cases cover 10 known gaps), GitHub Actions on Linux and Windows with Python 3.11 to 3.13, pinned lint. A mutation check was run once; it is not part of CI. | tests/; .github/workflows/CAI-ENGINE-TESTS.yml; tools/mutation-check.py (79.2% recorded in the register entry CHG-2026-10-12-11) | Mutation detection is not re-measured on each change. |
| SC-12 | Cryptographic Key Establishment and Management | Specified | Key establishment and management (CAI-ENG-SEC-001 Core section 6.3, SR-25). | — | Not implemented. |
| SC-13 | Cryptographic Protection | Partial | SHA-256 for the evidence chain. | TSM::test_clean_log_verifies | No signatures; Ed25519, ML-DSA (FIPS 204) and SHA-384 are specified (SR-25), not implemented. |
| SI-4 | System Monitoring | Partial | Telemetry events are accepted and validated; monitoring and detection logic are described in the CAI documents only. | test_cai_engine.py::test_good_telemetry_accepted | Accepted telemetry is not used by any decision (xfail AUD-07). |
| SI-7 | Software, Firmware, and Information Integrity | Partial | Integrity of evidence information is verifiable (`verify()`). | TSM::test_editing_any_record_is_detected | Software integrity of the engine is specified (CAI-ENG-SEC-001 Core section 6.4, item 3), not implemented. |
| SI-10 | Information Input Validation | Partial | Telemetry validation (source, domain, confidence range, provenance, timestamp); action category validation. | TSM::test_invalid_telemetry_is_rejected, test_each_valid_domain_is_accepted; TEC::test_invalid_category_is_refused_with_the_allowed_list | A NaN confidence passes every threshold and a boolean is accepted as confidence (xfail F-02, F-02b); telemetry age is not checked. |
| SI-17 | Fail-safe Procedures | Partial | Fail-safe combination: DENY wins over ESCALATE over ALLOW; low-confidence or non-explainable AI output is denied. | TSM::test_summarize_is_conservative, test_ai_confidence_floor, test_non_explainable_ai_output_is_denied | NaN confidence is not treated as failure (xfail F-02). |

## 6. NIST CSF 2.0

All 106 subcategories, with the statement text of the official catalog.

Table 3 — CSF 2.0 subcategories.

| ID | Subcategory | Status | CAI element and evidence |
|---|---|---|---|
| GV.OC-01 | The organizational mission is understood and informs cybersecurity risk management | Not addressed | — |
| GV.OC-02 | Internal and external stakeholders are understood, and their needs and expectations regarding cybersecurity risk management are understood and considered | Not addressed | — |
| GV.OC-03 | Legal, regulatory, and contractual requirements regarding cybersecurity - including privacy and civil liberties obligations - are understood and managed | Partial | Jurisdiction layer classifies each AI proposal under the EU AI Act or the USA baseline and records the regulatory block (eu_ai_act.py, usa.py). TEC::test_eu_governed_record, test_usa_governed_record. An unknown jurisdiction is evaluated as EU (xfail JUR). |
| GV.OC-04 | Critical objectives, capabilities, and services that external stakeholders depend on or expect from the organization are understood and communicated | Not addressed | — |
| GV.OC-05 | Outcomes, capabilities, and services that the organization depends on are understood and communicated | Not addressed | — |
| GV.OV-01 | Cybersecurity risk management strategy outcomes are reviewed to inform and adjust strategy and direction | Not addressed | — |
| GV.OV-02 | The cybersecurity risk management strategy is reviewed and adjusted to ensure coverage of organizational requirements and risks | Not addressed | — |
| GV.OV-03 | Organizational cybersecurity risk management performance is evaluated and reviewed for adjustments needed | Not addressed | — |
| GV.PO-01 | Policy for managing cybersecurity risks is established based on organizational context, cybersecurity strategy, and priorities and is communicated and enforced | Not addressed | — |
| GV.PO-02 | Policy for managing cybersecurity risks is reviewed, updated, communicated, and enforced to reflect changes in requirements, threats, technology, and organizational mission | Partial | The engine enforces a fixed policy (per-state action categories, gates). Policy review and update follow the CAI change process (register). |
| GV.RM-01 | Risk management objectives are established and agreed to by organizational stakeholders | Not addressed | — |
| GV.RM-02 | Risk appetite and risk tolerance statements are established, communicated, and maintained | Partial | Tolerance is encoded as thresholds: AI confidence floor 0.80, blast radius 25, Purdue levels 0 to 2, USA floors by consequence. Engineering defaults, not set by an organization. |
| GV.RM-03 | Cybersecurity risk management activities and outcomes are included in enterprise risk management processes | Not addressed | — |
| GV.RM-04 | Strategic direction that describes appropriate risk response options is established and communicated | Not addressed | — |
| GV.RM-05 | Lines of communication across the organization are established for cybersecurity risks, including risks from suppliers and other third parties | Not addressed | — |
| GV.RM-06 | A standardized method for calculating, documenting, categorizing, and prioritizing cybersecurity risks is established and communicated | Partial | Standard categorization of AI use: EU risk tiers and USA consequence classes per NSM-22 sector. TSM::test_eu_tiers, test_usa_assurance_floor_per_sector. |
| GV.RM-07 | Strategic opportunities (i.e., positive risks) are characterized and are included in organizational cybersecurity risk discussions | Not addressed | — |
| GV.RR-01 | Organizational leadership is responsible and accountable for cybersecurity risk and fosters a culture that is risk-aware, ethical, and continually improving | Not addressed | — |
| GV.RR-02 | Roles, responsibilities, and authorities related to cybersecurity risk management are established, communicated, understood, and enforced | Partial | Human authority is required for every ESCALATE decision; approval needs a named approver; AI cannot approve. Approver not authenticated; pending approvals never expire (xfail SGH 5.2). |
| GV.RR-03 | Adequate resources are allocated commensurate with the cybersecurity risk strategy, roles, responsibilities, and policies | Not addressed | — |
| GV.RR-04 | Cybersecurity is included in human resources practices | Not addressed | — |
| GV.SC-01 | A cybersecurity supply chain risk management program, strategy, objectives, policies, and processes are established and agreed to by organizational stakeholders | Not addressed | — |
| GV.SC-02 | Cybersecurity roles and responsibilities for suppliers, customers, and partners are established, communicated, and coordinated internally and externally | Not addressed | — |
| GV.SC-03 | Cybersecurity supply chain risk management is integrated into cybersecurity and enterprise risk management, risk assessment, and improvement processes | Not addressed | — |
| GV.SC-04 | Suppliers are known and prioritized by criticality | Not addressed | — |
| GV.SC-05 | Requirements to address cybersecurity risks in supply chains are established, prioritized, and integrated into contracts and other types of agreements with suppliers and other relevant third parties | Not addressed | — |
| GV.SC-06 | Planning and due diligence are performed to reduce risks before entering into formal supplier or other third-party relationships | Not addressed | — |
| GV.SC-07 | The risks posed by a supplier, their products and services, and other third parties are understood, recorded, prioritized, assessed, responded to, and monitored over the course of the relationship | Not addressed | — |
| GV.SC-08 | Relevant suppliers and other third parties are included in incident planning, response, and recovery activities | Not addressed | — |
| GV.SC-09 | Supply chain security practices are integrated into cybersecurity and enterprise risk management programs, and their performance is monitored throughout the technology product and service life cycle | Not addressed | — |
| GV.SC-10 | Cybersecurity supply chain risk management plans include provisions for activities that occur after the conclusion of a partnership or service agreement | Not addressed | — |
| ID.AM-01 | Inventories of hardware managed by the organization are maintained | Not addressed | — |
| ID.AM-02 | Inventories of software, services, and systems managed by the organization are maintained | Not addressed | — |
| ID.AM-03 | Representations of the organization's authorized network communication and internal and external network data flows are maintained | Not addressed | — |
| ID.AM-04 | Inventories of services provided by suppliers are maintained | Not addressed | — |
| ID.AM-05 | Assets are prioritized based on classification, criticality, resources, and impact on the mission | Not addressed | — |
| ID.AM-07 | Inventories of data and corresponding metadata for designated data types are maintained | Not addressed | — |
| ID.AM-08 | Systems, hardware, software, services, and data are managed throughout their life cycles | Not addressed | — |
| ID.IM-01 | Improvements are identified from evaluations | Not addressed | — |
| ID.IM-02 | Improvements are identified from security tests and exercises, including those done in coordination with suppliers and relevant third parties | Not addressed | — |
| ID.IM-03 | Improvements are identified from execution of operational processes, procedures, and activities | Not addressed | — |
| ID.IM-04 | Incident response plans and other cybersecurity plans that affect operations are established, communicated, maintained, and improved | Not addressed | — |
| ID.RA-01 | Vulnerabilities in assets are identified, validated, and recorded | Not addressed | — |
| ID.RA-02 | Cyber threat intelligence is received from information sharing forums and sources | Not addressed | — |
| ID.RA-03 | Internal and external threats to the organization are identified and recorded | Described | Threat models in the USA baseline and sectors; engine threat model in CAI-ENG-SEC-001 Core section 5. |
| ID.RA-04 | Potential impacts and likelihoods of threats exploiting vulnerabilities are identified and recorded | Not addressed | — |
| ID.RA-05 | Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk and inform risk response prioritization | Not addressed | — |
| ID.RA-06 | Risk responses are chosen, prioritized, planned, tracked, and communicated | Not addressed | — |
| ID.RA-07 | Changes and exceptions are managed, assessed for risk impact, recorded, and tracked | Partial | Changes to CAI are recorded and tracked (signed CHG commits, register). Not applied to the governed environment. |
| ID.RA-08 | Processes for receiving, analyzing, and responding to vulnerability disclosures are established | Not addressed | — |
| ID.RA-09 | The authenticity and integrity of hardware and software are assessed prior to acquisition and use | Specified | Code integrity of the engine installation (CAI-ENG-SEC-001 Core section 6.4, item 3). |
| ID.RA-10 | Critical suppliers are assessed prior to acquisition | Not addressed | — |
| PR.AA-01 | Identities and credentials for authorized users, services, and hardware are managed by the organization | Specified | Approver and engine keys by purpose (CAI-ENG-SEC-001 Core section 6.3). |
| PR.AA-02 | Identities are proofed and bound to credentials based on the context of interactions | Not addressed | — |
| PR.AA-03 | Users, services, and hardware are authenticated | Specified | Approver authentication by signature (SR-14). Not implemented: the approver is a name. |
| PR.AA-04 | Identity assertions are protected, conveyed, and verified | Specified | Signed statements (CAI-ENG-SEC-001 Core section 8). |
| PR.AA-05 | Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties | Partial | Per-state permitted action categories enforced; AI and approver channels separated. TSM::test_policy_state_constraint. |
| PR.AA-06 | Physical access to assets is managed, monitored, and enforced commensurate with risk | Not addressed | — |
| PR.AT-01 | Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind | Not addressed | — |
| PR.AT-02 | Individuals in specialized roles are provided with awareness and training so that they possess the knowledge and skills to perform relevant tasks with cybersecurity risks in mind | Not addressed | — |
| PR.DS-01 | The confidentiality, integrity, and availability of data-at-rest are protected | Partial | Evidence log is tamper-evident for single records; state.json is not protected. |
| PR.DS-02 | The confidentiality, integrity, and availability of data-in-transit are protected | Not addressed | — |
| PR.DS-10 | The confidentiality, integrity, and availability of data-in-use are protected | Not addressed | — |
| PR.DS-11 | Backups of data are created, protected, maintained, and tested | Not addressed | — |
| PR.IR-01 | Networks and environments are protected from unauthorized logical access and usage | Not addressed | — |
| PR.IR-02 | The organization's technology assets are protected from environmental threats | Not addressed | — |
| PR.IR-03 | Mechanisms are implemented to achieve resilience requirements in normal and adverse situations | Not addressed | — |
| PR.IR-04 | Adequate resource capacity to ensure availability is maintained | Not addressed | — |
| PR.PS-01 | Configuration management practices are established and applied | Partial | Configuration management of the CAI repository: signed changes, register, CI. |
| PR.PS-02 | Software is maintained, replaced, and removed commensurate with risk | Not addressed | — |
| PR.PS-03 | Hardware is maintained, replaced, and removed commensurate with risk | Not addressed | — |
| PR.PS-04 | Log records are generated and made available for continuous monitoring | Partial | An evidence record is generated for every state-changing engine operation and is readable as JSON Lines, through `report()` and `verify()`. TEC::test_report_lists_every_record. Refused requests are not logged. |
| PR.PS-05 | Installation and execution of unauthorized software are prevented | Not addressed | — |
| PR.PS-06 | Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle | Implemented | Engine development: tests, CI on two operating systems and three Python versions, pinned lint, mutation testing. |
| DE.AE-02 | Potentially adverse events are analyzed to better understand associated activities | Not addressed | — |
| DE.AE-03 | Information is correlated from multiple sources | Described | Correlation is described in the USA labs (State-Aware-Correlation). Not implemented. |
| DE.AE-04 | The estimated impact and scope of adverse events are understood | Partial | Impact inputs gate actions: blast radius, Purdue level, destructive flag, sector consequence. Values are supplied by the caller. |
| DE.AE-06 | Information on adverse events is provided to authorized staff and tools | Not addressed | — |
| DE.AE-07 | Cyber threat intelligence and other contextual information are integrated into the analysis | Not addressed | — |
| DE.AE-08 | Incidents are declared when adverse events meet the defined incident criteria | Partial | Leaving DETECT requires `detection_confirmed`; the fact is set by the caller (AUD-07). |
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Not addressed | — |
| DE.CM-02 | The physical environment is monitored to find potentially adverse events | Not addressed | — |
| DE.CM-03 | Personnel activity and technology usage are monitored to find potentially adverse events | Partial | Every AI proposal is recorded with system name, model version, confidence, drift and decision. Values are declared by the AI client. |
| DE.CM-06 | External service provider activities and services are monitored to find potentially adverse events | Not addressed | — |
| DE.CM-09 | Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events | Partial | Telemetry is accepted and validated (test_cai_engine.py::test_good_telemetry_accepted); no detection logic, and telemetry is not used in decisions (xfail AUD-07). |
| RS.AN-03 | Analysis is performed to establish what has taken place during an incident and the root cause of the incident | Not addressed | — |
| RS.AN-06 | Actions performed during an investigation are recorded, and the records' integrity and provenance are preserved | Partial | Every decision is recorded in the hash-chained log with gate reasons and approver. Not signed. |
| RS.AN-07 | Incident data and metadata are collected, and their integrity and provenance are preserved | Partial | Telemetry must carry source and provenance; accepted events are recorded in the chain. |
| RS.AN-08 | An incident's magnitude is estimated and validated | Not addressed | — |
| RS.CO-02 | Internal and external stakeholders are notified of incidents | Not addressed | — |
| RS.CO-03 | Information is shared with designated internal and external stakeholders | Not addressed | — |
| RS.MA-01 | The incident response plan is executed in coordination with relevant third parties once an incident is declared | Partial | The lifecycle orders response phases and blocks invalid transitions. TSM::test_transition_matrix. |
| RS.MA-02 | Incident reports are triaged and validated | Not addressed | — |
| RS.MA-03 | Incidents are categorized and prioritized | Not addressed | — |
| RS.MA-04 | Incidents are escalated or elevated as needed | Partial | ESCALATE decisions wait for a human (PENDING_APPROVAL). Applies to actions, not to incident severity. |
| RS.MA-05 | The criteria for initiating incident recovery are applied | Partial | Entry to RESTORE requires `eviction_completed` and `clean_baseline_validated`; facts set by the caller. |
| RS.MI-01 | Incidents are contained | Partial | CONTAINMENT is permitted only in ISOLATE and needs human approval. The engine governs the decision; it does not contain anything (adapters specified, SR-21). |
| RS.MI-02 | Incidents are eradicated | Partial | ERADICATION is permitted only in EVICT, always with human approval. The engine does not perform it. |
| RC.CO-03 | Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders | Not addressed | — |
| RC.CO-04 | Public updates on incident recovery are shared using approved methods and messaging | Not addressed | — |
| RC.RP-01 | The recovery portion of the incident response plan is executed once initiated from the incident response process | Partial | Recovery starts only through the EVICT to RESTORE transition, which requires `eviction_completed` and `clean_baseline_validated`; facts set by the caller. |
| RC.RP-02 | Recovery actions are selected, scoped, prioritized, and performed | Partial | RECOVERY is permitted only in RESTORE and needs human approval. The engine does not perform it. |
| RC.RP-03 | The integrity of backups and other restoration assets is verified before using them for restoration | Not addressed | — |
| RC.RP-04 | Critical mission functions and cybersecurity risk management are considered to establish post-incident operational norms | Not addressed | — |
| RC.RP-05 | The integrity of restored assets is verified, systems and services are restored, and normal operating status is confirmed | Not addressed | — |
| RC.RP-06 | The end of incident recovery is declared based on criteria, and incident-related documentation is completed | Not addressed | — |

## 7. NIST AI RMF 1.0

All 72 subcategories. The descriptor column is a short paraphrase; the official text in NIST AI 100-1 governs. The engine labels each governed decision with the four function names (`nist_ai_rmf.rmf_trace`); that label is not evidence of any subcategory and is not counted here.

Table 4 — AI RMF 1.0 subcategories.

| ID | Descriptor (paraphrase) | Status | CAI element and evidence |
|---|---|---|---|
| GOVERN 1.1 | Legal and regulatory requirements involving AI are understood, managed and documented | Partial | EU AI Act tiers and USA baseline classification are applied to each proposal and recorded (eu_ai_act.py, usa.py). An unknown jurisdiction is evaluated as EU (xfail JUR). |
| GOVERN 1.2 | Trustworthy AI characteristics are integrated into policies and processes | Not addressed | — |
| GOVERN 1.3 | Risk management activities are scaled to risk tolerance | Not addressed | — |
| GOVERN 1.4 | Risk management is established through transparent policies, procedures and controls | Partial | Gates and thresholds are in the code and documented; every decision records the gate names and reasons. |
| GOVERN 1.5 | Ongoing monitoring and periodic review are planned, with roles and frequency | Specified | Periodic revalidation of AI systems: `revalidation_due` and drift-triggered revalidation (USA profile section 5, USA-SR-03, USA-SR-12). |
| GOVERN 1.6 | AI systems are inventoried and resourced by risk priority | Specified | Registration of AI systems before use (CAI-ENG-SEC-001 Core SR-08; USA profile section 5, USA-SR-03, USA-SR-04). |
| GOVERN 1.7 | AI systems are decommissioned safely | Specified | Lifecycle status DECOMMISSIONED blocks every operation of the AI system (USA profile section 5, USA-SR-03). |
| GOVERN 2.1 | Roles, responsibilities and lines of communication are documented | Described | Roles (operator, approver, AI system) in CAI-USA-Definition and CAI-ENG-SEC-001. |
| GOVERN 2.2 | Personnel and partners receive AI risk management training | Not addressed | — |
| GOVERN 2.3 | Executive leadership takes responsibility for AI risk decisions | Not addressed | — |
| GOVERN 3.1 | Decision-making is informed by a diverse team | Not addressed | — |
| GOVERN 3.2 | Policies define roles for human-AI configurations and oversight | Partial | AI output is advisory: the AI client cannot approve (no MCP approval tool); every ESCALATE needs a named human. Approver not authenticated. |
| GOVERN 4.1 | Policies foster critical thinking and a safety-first mindset | Not addressed | — |
| GOVERN 4.2 | Teams document and communicate AI risks and impacts | Described | Risk documentation in the CAI documents and specifications. |
| GOVERN 4.3 | Practices enable AI testing, incident identification and information sharing | Partial | Testing of the engine itself (tests, CI). No incident sharing. |
| GOVERN 5.1 | External feedback on impacts is collected and integrated | Not addressed | — |
| GOVERN 5.2 | Adjudicated feedback is incorporated into system design | Not addressed | — |
| GOVERN 6.1 | Policies address third-party AI risks | Not addressed | — |
| GOVERN 6.2 | Contingency processes cover failures of high-risk third-party data or systems | Not addressed | — |
| MAP 1.1 | Intended purposes, settings, users, impacts and assumptions are documented | Partial | The classification derived from the declared deployment context (EU tier with rationale and Annex references, or USA sector, SRMA and consequence) is recorded with each governed decision. The context is declared by the AI client (xfail F-01). |
| MAP 1.2 | Interdisciplinary actors take part in establishing context | Not addressed | — |
| MAP 1.3 | Mission and AI goals are documented | Not addressed | — |
| MAP 1.4 | Business value and context of use are defined | Not addressed | — |
| MAP 1.5 | Risk tolerances are determined and documented | Not addressed | — |
| MAP 1.6 | System requirements are elicited from relevant actors | Not addressed | — |
| MAP 2.1 | Tasks and methods the AI system supports are defined | Not addressed | — |
| MAP 2.2 | Knowledge limits and human oversight of outputs are documented | Partial | Knowledge limits enforced per decision: confidence floor, explainability required; oversight recorded. |
| MAP 2.3 | Scientific integrity and TEVV considerations are identified | Not addressed | — |
| MAP 3.1 | Potential benefits are examined and documented | Not addressed | — |
| MAP 3.2 | Potential costs, including non-monetary costs, are examined and documented | Not addressed | — |
| MAP 3.3 | Targeted application scope is specified | Not addressed | — |
| MAP 3.4 | Operator and practitioner proficiency processes are defined | Not addressed | — |
| MAP 3.5 | Human oversight processes are defined, assessed and documented | Partial | Human oversight is defined in code (ESCALATE, PENDING_APPROVAL, approve/deny) and tested. TSM::test_usa_critical_sector_always_needs_a_human. |
| MAP 4.1 | Legal and technology risks of components, including third-party, are mapped | Not addressed | — |
| MAP 4.2 | Internal risk controls for components are identified and documented | Not addressed | — |
| MAP 5.1 | Likelihood and magnitude of each identified impact are characterized | Partial | Magnitude inputs (sector consequence, blast radius, Purdue level) affect gates; likelihood is not modelled. |
| MAP 5.2 | Regular engagement with relevant actors on impacts is supported | Not addressed | — |
| MEASURE 1.1 | Metrics for the most significant risks are selected; unmeasured risks are documented | Partial | Confidence and drift are recorded and gated; they are declared by the AI client, not measured by the engine. |
| MEASURE 1.2 | Appropriateness of metrics and effectiveness of controls are reassessed | Not addressed | — |
| MEASURE 1.3 | Independent assessors and affected parties are involved in assessments | Not addressed | — |
| MEASURE 2.1 | Test sets, metrics and TEVV tools are documented | Not addressed | — |
| MEASURE 2.2 | Evaluations involving human subjects meet requirements and are representative | Not addressed | — |
| MEASURE 2.3 | Performance is measured in conditions similar to deployment | Not addressed | — |
| MEASURE 2.4 | Functionality and behavior are monitored in production | Partial | Each production proposal is recorded with its confidence, drift and decision; values are declared. |
| MEASURE 2.5 | Validity and reliability are demonstrated; generalizability limits are documented | Not addressed | — |
| MEASURE 2.6 | Safety risks, residual risk and safe failure are evaluated | Partial | Safe failure per decision: DENY on low confidence or a non-explainable output; DENY on drift above 0.15 only for EU high-risk and USA critical-infrastructure contexts; human escalation for high consequence. Confidence and drift are declared by the AI client. |
| MEASURE 2.7 | Security and resilience are evaluated and documented | Specified | Security evaluation of the engine: threat model and acceptance tests (CAI-ENG-SEC-001 Core sections 5 and 13). |
| MEASURE 2.8 | Transparency and accountability risks are examined and documented | Partial | Accountability record per decision: gate results, regulatory block, approver name. Not signed. |
| MEASURE 2.9 | The model is explained and validated; output is interpreted in context | Partial | A non-explainable output is denied, but the explainable flag is declared by the AI client. Explanation text is required only for EU high-risk and USA generative AI; provenance only for USA generative AI. Explanation content is not evaluated. |
| MEASURE 2.10 | Privacy risk is examined and documented | Not addressed | — |
| MEASURE 2.11 | Fairness and bias are evaluated | Not addressed | — |
| MEASURE 2.12 | Environmental impact and sustainability are assessed | Not addressed | — |
| MEASURE 2.13 | Effectiveness of TEVV metrics and processes is evaluated | Not addressed | — |
| MEASURE 3.1 | Existing, unanticipated and emergent risks are tracked over time | Not addressed | — |
| MEASURE 3.2 | Risk tracking is considered where measurement is difficult | Not addressed | — |
| MEASURE 3.3 | Feedback processes let users report problems and appeal outcomes | Not addressed | — |
| MEASURE 4.1 | Measurement approaches are connected to deployment context | Not addressed | — |
| MEASURE 4.2 | Trustworthiness results are validated with domain experts and AI actors | Not addressed | — |
| MEASURE 4.3 | Performance changes informed by relevant actors are documented | Not addressed | — |
| MANAGE 1.1 | A determination is made whether the AI system achieves its purpose and should proceed | Not addressed | — |
| MANAGE 1.2 | Treatment of risks is prioritized by impact, likelihood and resources | Not addressed | — |
| MANAGE 1.3 | Responses to high-priority risks are developed, planned and documented | Not addressed | — |
| MANAGE 1.4 | Residual risks to acquirers and end users are documented | Not addressed | — |
| MANAGE 2.1 | Resources and non-AI alternatives are considered to reduce impacts | Not addressed | — |
| MANAGE 2.2 | Mechanisms sustain the value of deployed AI systems | Not addressed | — |
| MANAGE 2.3 | Procedures respond to and recover from previously unknown risks | Not addressed | — |
| MANAGE 2.4 | Mechanisms supersede, disengage or deactivate AI systems inconsistent with intended use | Partial | Per decision, output is superseded (DENY) when confidence is below the floor, or drift exceeds 0.15 in EU high-risk and USA critical-infrastructure contexts. Suspending an AI system as a whole is specified (USA-SR-03, USA-SR-12), not implemented. |
| MANAGE 3.1 | Third-party AI risks and benefits are monitored; controls are documented | Not addressed | — |
| MANAGE 3.2 | Pre-trained models are monitored as part of maintenance | Not addressed | — |
| MANAGE 4.1 | Post-deployment monitoring, appeal, override, decommissioning and incident response are implemented | Not addressed | — |
| MANAGE 4.2 | Continual improvement activities are integrated into updates | Not addressed | — |
| MANAGE 4.3 | Incidents and errors are communicated to relevant actors and tracked | Not addressed | — |

## 8. NIST SP 800-207 Zero Trust Architecture

Table 5 — SP 800-207 tenets (section 2.1) and logical components (section 3).

| Item | Summary | Status | CAI element and limit |
|---|---|---|---|
| Tenet 1 | All data sources and computing services are considered resources. | Not addressed | The engine has no resource model. |
| Tenet 2 | All communication is secured regardless of network location. | Specified | Local IPC hardening (CAI-ENG-SEC-001 Core section 6.5); the MCP transport is local stdio. |
| Tenet 3 | Access to individual enterprise resources is granted on a per-session basis. | Partial | Each proposed action is evaluated on its own; no session concept. |
| Tenet 4 | Access is determined by dynamic policy, including the observable state of client, application and asset. | Partial | Decisions depend on lifecycle state, action attributes and AI metadata. Observable environment state (telemetry) is not used (xfail AUD-07). |
| Tenet 5 | The enterprise monitors and measures the integrity and security posture of all assets. | Not addressed | — |
| Tenet 6 | Authentication and authorization are dynamic and strictly enforced before access is allowed. | Partial | Authorization per action is enforced before any EXECUTED record; no authentication of the requester or approver. |
| Tenet 7 | The enterprise collects data on assets, network and communications and uses it to improve security posture. | Partial | Telemetry is collected and validated; it is not used to improve anything (xfail AUD-07). |
| PE / PA / PEP (section 3) | Policy engine, policy administrator, policy enforcement point. | Partial | evaluate() acts as a policy engine and commit() records the decision. There is no enforcement point in front of resources: adapters that act are specified (SR-21), not implemented. |


## 9. Gaps with the largest effect

1. Environmental state does not enter decisions. Accepted telemetry is recorded but no decision uses it, and telemetry age is not checked (xfail AUD-07). This limits AC-3, SI-4, CSF DE.CM-09 and SP 800-207 tenets 4 and 7.
2. No authentication or signature. Approvers are names, approvals and evidence are not signed (SR-14, SR-19, SR-20). This limits AC-5, AU-9, AU-10, IA-2 and CSF PR.AA.
3. Approval without revalidation. approve() executes a pending action even if the lifecycle state changed after the proposal (xfail T-09).
4. Input and approval handling. A NaN or boolean confidence is accepted (xfail F-02, F-02b); omitting the sector removes USA oversight (xfail F-01); an unknown jurisdiction is evaluated as EU (xfail JUR); pending approvals never expire (xfail SGH 5.2).
5. Evidence continuity. init() truncates an existing log (xfail F-03); truncation of the last records and rewriting of the whole chain are not detected (xfail NEW-06, T-08).

CAI-ENG-SEC-001 Core section 16 plans the implementation of these requirements.

## 10. Maintenance

This map is updated in the same change as any engine, test or specification change that alters a status. When an xfail test starts to pass, the change that fixes the gap updates the rows that cite it. Counts in Table 1 are recomputed from the tables.

## 11. Relationship to Other CAI Documents

This document must be read together with:

- CAI-USA-Definition
- CAI-USA-AI-RMF-Map
- CAI-USA-CISA-ZT-Map
- CAI-USA-Traceability-Matrix
- CAI-Engine/specifications/CAI-ENG-SEC-001-Core.md
- CAI-Engine/specifications/CAI-ENG-SEC-001-USA.md
- CAI-Core-Reference-Resolution-Record

## Status

Status: Draft – Phase 1 of the external-control mapping  
End of Document
