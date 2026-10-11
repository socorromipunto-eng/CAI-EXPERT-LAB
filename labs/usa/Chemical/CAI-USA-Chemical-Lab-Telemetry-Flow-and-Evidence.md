Cybersecurity Artificial Intelligence Framework – USA Chemical Labs
Cybersecurity Artificial Intelligence Framework – USA Chemical Lab – Telemetry Flow and Evidence Generation
Version 0.1 (Draft)
Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)
Copyright © 2025 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.
NOTE
The normative language of CAI-EXPERT-LAB documentation is English.
This laboratory artifact is non-normative and does not assert compliance, certification, accreditation, or regulatory approval.

Purpose
The purpose of this laboratory is to demonstrate a controlled, reproducible telemetry flow for Chemical sector environments that produces audit-ready evidence packages from CCES-normalized inputs. This lab validates that CAI execution depends on evidence integrity, provenance, and traceable decision context before any analytical enrichment or AI-assisted decision support is permitted. This lab establishes the evidentiary backbone required for governed operations across the CAI lifecycle while preserving the non-autonomous AI posture of CAI.

Scope and Applicability
This lab applies to Chemical sector environments where:
Telemetry originates from mixed IT, OT, and ICS domains.
Operational safety and process continuity require conservative handling of telemetry collection and transport.
Evidence must remain suitable for internal audit, external review, and defensible reconstruction of events.
Correlation, anomaly scoring, and decision support must not be performed on untrusted or unverifiable data.
This lab does not execute containment, eviction, or restoration actions. It produces evidence artifacts and verifies the controlled telemetry-to-evidence pipeline only.

CAI Lifecycle Alignment
Primary lifecycle stages supported:
MODEL
DETECT
Secondary alignment:
HARDEN (through validation of telemetry trust boundaries and evidence-by-design controls)
ISOLATE, DECEIVE, EVICT, and RESTORE are out of scope for action execution, but the evidence outputs produced here are prerequisites for those stages when governed execution is later demonstrated in other labs.

Laboratory Objectives
This laboratory demonstrates the ability to:
Define telemetry trust boundaries for Chemical environments and enforce them deterministically.
Normalize raw telemetry to CCES while preserving OT/ICS safety context and process semantics.
Produce immutable evidence artifacts with clear provenance, timestamps, and integrity checks.
Maintain an auditable chain-of-custody for telemetry and derived evidence packages.
Record decision context metadata required for governed analysis and non-autonomous AI advisory use.
Prove that evidence packages are reproducible from the same inputs and ruleset.

Laboratory Assumptions and Constraints
Telemetry collection must not disrupt or alter physical or chemical processes.
OT/ICS telemetry sources may be latency-sensitive and may impose conservative read-only constraints.
Time synchronization is imperfect; time sources must be recorded and drift must be detectable.
The lab enforces “trust first, intelligence second” and rejects analysis on inputs that fail integrity or provenance checks.
AI is explicitly out of scope for autonomous action. AI may be used later for advisory enrichment only after evidence eligibility gates are satisfied.

Telemetry Flow Model (Chemical Sector)
The telemetry flow validated in this lab is structured as a deterministic pipeline with explicit trust checkpoints.

Source Domains
Telemetry sources may include:
OT/ICS: PLC events, SCADA alarms, historian records, safety system signals, controller configuration changes, interlock and inhibit indicators.
Network: flow metadata, DPI summaries (where permitted), firewall events, remote access session records, VPN and jump-host logs.
Identity and Access: authentication attempts, privileged access events, account changes, token issuance, MFA outcomes.
Endpoint and Server: integrity alerts, process execution telemetry, configuration baselines, patch state signals, EDR/XDR events.
Application and Operations: batch process logs, MES/ERP integration signals (where present), maintenance window markers, change approvals.

Trust Boundary and Collection Rules
Collection is governed by these constraints:
Read-only collection in OT/ICS domains unless explicitly authorized by operational authority.
No polling patterns that create unsafe load or timing effects on controllers.
Explicit recording of collection method per source (agent, syslog, API pull, historian export).
Explicit identification of collection vantage point (OT segment sensor, IT SIEM forwarder, jump host, vendor gateway).
Strict segregation of lab collection from production enforcement actions.

Ingest Validation (Pre-Normalization Gate)
Before CCES normalization, each telemetry item must pass validation gates:
Source identification and asset binding (asset_id must resolve deterministically).
Integrity check of transport where applicable (e.g., signed payload, TLS metadata, collector hash).
Timestamp capture and time-source labeling (system time, NTP reference, collector receipt time).
Schema sanity checks and minimum required fields for sector eligibility.
If validation fails, the item is quarantined as non-eligible for correlation or AI advisory consumption.

CCES Normalization and Sector Context Preservation
This lab requires CCES-conformant normalization while preserving Chemical-specific context.

CCES Core Fields (Minimum)
Each normalized event must include, at minimum, the applicable CCES core elements such as:
asset_id
event_time (with time-source metadata)
event_type
source_domain (IT, OT, ICS, Network, Identity, Application)
sector_profile (Chemical)
confidence (if derived)
anomaly_score (if derived)
evidence_id (immutable reference to evidence package link)

Chemical Sector Context Fields
Where applicable, normalized records must include Chemical context fields such as:
process_mode (startup, steady-state, shutdown, maintenance)
safety_system_state (armed, inhibited, fault, test)
controller_state (active, standby, degraded)
control_zone (site/plant/area/unit cell naming as defined by the sector MODEL baseline)
purdue_level (where the environment uses Purdue-like segmentation)
ot_protocol (if observed and permitted)
change_window_reference (maintenance window identifier if available)

Normalization Ruleset Governance
Normalization must be deterministic and governed:
Normalization rules are versioned and immutable once evidence is generated.
Any change to normalization rules requires a new lab run and new evidence package identifiers.
Normalization must not discard raw records; it must reference raw artifacts by hash and location.

Evidence Package Model
This lab produces an evidence package that is sufficient for audit reconstruction.

Evidence Package Contents
Each lab run produces:
Raw telemetry bundle references (or pointers) with hashes.
Normalized CCES event set with hashes.
Collector and pipeline metadata (collector identity, configuration hash, ingestion time).
Validation results (pass/fail reasons, quarantine list).
Ruleset metadata (normalization ruleset id, version, hash).
Chain-of-custody log (who/what handled the data, when, and under what authority).
Lab execution record (operator, environment assumptions, run identifier).
Eligibility declaration for downstream correlation and AI advisory use.

Integrity and Chain-of-Custody Requirements
Evidence artifacts must meet:
Immutability after generation (no edits; only superseding via new packages).
Hashing of each artifact and of the evidence manifest.
Timestamping of manifest creation and retention.
Clear linkage between raw telemetry and derived normalized events.
Separation of duties where feasible (capture vs review), recorded as part of the lab run.

Governed AI Boundary for Evidence
AI may only consume evidence from this lab under explicit constraints:
Only CCES-normalized, validation-passed events may be presented to AI systems.
AI receives evidence references, not raw uncontrolled telemetry.
AI outputs are advisory and must include uncertainty indicators and references to evidence_id.
AI outputs must never trigger action and must never overwrite deterministic pipeline results.
If evidence eligibility is not satisfied, AI consumption is prohibited.

Procedures

Define the lab environment and select representative Chemical telemetry sources across IT and OT/ICS domains.

Document collection vantage points and confirm read-only constraints in OT/ICS domains.

Execute telemetry capture for a defined observation window and record the exact window boundaries.

Run ingest validation gates; quarantine any failing records and record reasons.

Normalize passing records into CCES with Chemical sector context fields preserved.

Generate the evidence package manifest, including all hashes and ruleset identifiers.

Produce a short reconstruction test: demonstrate that the normalized set can be regenerated from the raw references and the ruleset without divergence.

Record acceptance results and sign-off.

Expected Outputs
A completed lab run produces:
A CCES-normalized event set suitable for correlation labs.
An immutable evidence package with manifest and integrity hashes.
A chain-of-custody record sufficient for audit reconstruction.
A validation quarantine report for non-eligible telemetry.
A governed AI eligibility statement linking AI advisory inputs to evidence_id.

Acceptance Criteria
The lab is successful when all criteria below are satisfied:
Telemetry trust boundaries are explicitly defined and enforced.
All accepted telemetry passes validation gates and is traceable to a known source and asset_id.
CCES normalization preserves Chemical sector safety and process context.
Evidence package artifacts are immutable, hashed, and include a complete manifest.
Chain-of-custody is recorded and supports reconstruction of who handled what and when.
A reconstruction test demonstrates deterministic regeneration of normalized outputs from inputs and ruleset.
Any failure invalidates the lab run and requires a new evidence package.

Relationship to Normative CAI Documents
This lab operates alongside and must remain consistent with:
CAI-Core-Execution-Model.md
CAI-Core-Operational-State-Model.md
CAI-Core-Integrity-and-Self-Defense-Governance.md
CAI-USA-CCES.md
CAI-USA-Telemetry-and-Data-Model.md
CAI-USA-AI-Governance-and-Assurance.md
CAI-USA-Chemical-Sector-Definition.md
CAI-USA-Chemical-Telemetry-and-Data-Model.md
If a conflict is identified, the lab must be corrected. Normative documents remain authoritative.

Non-Claims
This laboratory does not assert compliance with EPA, DHS, CISA, NIST, OSHA, CFATS, ISA/IEC standards, or any other authority. It does not authorize operational response actions. It demonstrates telemetry-to-evidence execution fidelity only.

Status
Draft – CAI USA Chemical telemetry flow and evidence generation lab defined.

End of Document