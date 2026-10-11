CAI-USA-CCES
Common CAI Event Schema (USA)

Cybersecurity Artificial Intelligence Framework – USA
Common CAI Event Schema (CCES)

Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2025 Antonio José Socorro Marín.
All rights reserved.

Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

NOTE
The normative language of CAI-EXPERT-LAB documentation is English.
This document defines a normative and mandatory event schema for CAI operational telemetry in United States environments.
It does not assert compliance, certification, accreditation, or regulatory approval.

Purpose

The purpose of this document is to define the Common CAI Event Schema (CCES) for the Cybersecurity Artificial Intelligence Framework (CAI) as applied in United States contexts.

CCES establishes a standardized, machine-readable, and auditable event structure to ensure consistent telemetry, traceability, explainability, and governance across all CAI operational stages, including AI-assisted detection, decision-making, and response.

This schema is authoritative for CAI-USA and SHALL be used by all CAI telemetry producers, playbooks, AI components, and orchestration layers.

Scope and Non-Scope

In Scope

This document defines:

A normative event schema for all CAI operational events

Mandatory fields for security, AI, and governance traceability

Event classification aligned with CAI operational stages

Requirements for event integrity, timing, and correlation

Support for IT, OT/ICS, cloud, firmware, middleware, network, and AI-enabled environments

Explicitly Out of Scope

This document does not:

Define specific logging technologies or vendors

Replace organizational SIEM or data lake architectures

Mandate storage duration or retention policies

Define sector-specific schemas (addressed separately)

Normative Status

The Common CAI Event Schema is a REQUIRED component of CAI-USA.

Any CAI component that emits telemetry, executes automated actions, performs AI inference, or supports security decisions MUST conform to this schema.

Non-conforming telemetry is considered non-authoritative within CAI.

Design Principles

CCES is designed according to the following principles:

Determinism: identical events produce identical schema representations

Traceability: every action, inference, and decision is traceable

Explainability: AI-related events support post-hoc analysis

Minimal ambiguity: semantic meaning is explicit, not inferred

Security-first: events support forensic integrity and auditability

Extensibility: optional fields allow controlled evolution

Event Classification Model

All CAI events SHALL be classified according to:

CAI Operational Stage:

MODEL

HARDEN

DETECT

ISOLATE

DECEIVE

EVICT

RESTORE

Event Category:

Observation

Detection

Decision

Action

Control

Error

Governance

Assurance

Event Severity:

Informational

Low

Medium

High

Critical

Core Event Structure

Every CAI event SHALL include the following top-level fields:

event_id
Globally unique identifier for the event.

event_timestamp
UTC timestamp in ISO 8601 format indicating when the event occurred.

event_ingest_timestamp
UTC timestamp indicating when the event was ingested into the CAI telemetry pipeline.

cai_stage
CAI operational stage associated with the event.

event_category
Logical classification of the event.

event_severity
Impact or risk level of the event.

event_source
Component or system emitting the event.

event_type
Specific type identifier describing the event semantics.

event_description
Human-readable description of the event.

correlation_id
Identifier used to correlate related events across stages and systems.

Asset Context

Each event SHALL include an asset context object:

asset:

asset_id

asset_type (identity, device, application, service, data, network, firmware, AI-model)

asset_owner

asset_environment (IT, OT, ICS, cloud, hybrid)

asset_criticality

Identity and Access Context

If applicable, events SHALL include identity information:

identity:

identity_id

identity_type (user, service account, workload, device identity)

authentication_method

privilege_level

session_id

AI Context (Mandatory for AI-Assisted Events)

Any event involving AI inference, scoring, or decision support SHALL include:

ai_context:

ai_model_id

ai_model_version

ai_function (detection, classification, prioritization, recommendation)

confidence_score

inference_outcome

inference_explanation_reference

human_override_required (true/false)

human_override_status

Decision and Action Context

For events resulting in decisions or actions:

decision:

decision_id

decision_type (allow, deny, isolate, deceive, evict, restore)

decision_basis (policy, AI-assisted, human)

decision_confidence

action:

action_id

action_type

action_scope

action_status

action_rollback_possible (true/false)

Governance and Assurance Context

Governance-relevant events SHALL include:

governance:

policy_id

control_id

assurance_gate

compliance_reference (if applicable)

approval_required

approval_status

Integrity and Security Controls

All events SHALL support integrity assurance:

integrity:

event_signature

hash_algorithm

hash_value

tamper_evidence_supported (true/false)

OT/ICS Safety Context (When Applicable)

For OT/ICS-related events:

safety:

safety_impact_assessed (true/false)

safety_risk_level

production_impact_expected

manual_confirmation_required

Event Extensibility

Optional extensions MAY be added using a controlled namespace:

extensions:

extension_name

extension_version

extension_payload

Extensions MUST NOT redefine core schema semantics.

Relationship to Other CAI Documents

This document is authoritative and MUST be used in conjunction with:

CAI-Core-Taxonomy

CAI-Core-Operations

CAI-USA-Telemetry-and-Data-Model

CAI-USA-Operations-Playbooks

CAI-USA-AI-Governance-and-Assurance

CAI-USA-Threat-and-Assumption-Model

Future sector-specific schemas SHALL inherit from CCES.

Versioning and Change Control

Changes to CCES SHALL:

Be versioned explicitly

Preserve backward compatibility when possible

Be documented through controlled governance processes

Author and Ownership

CAI-USA-CCES is authored and owned by Antonio José Socorro Marín.
This document is an intellectual property asset governed by the legal documents contained in the /legal directory of this repository.

End of Document