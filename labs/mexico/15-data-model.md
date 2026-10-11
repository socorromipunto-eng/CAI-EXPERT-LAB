# CAI-MX – Formal Data Model Specification

---

## 1. Purpose

This document defines the formal data model for CAI (Continuous Adaptive Integrity).

Its objective is to provide a precise, structured, interoperable, and implementation-ready specification of the core entities required to enforce decision integrity across federated systems aligned with the APF cybersecurity environment.

This specification is designed to be:

- deterministic
- auditable
- interoperable
- extensible
- adversarially robust

---

## 2. Canonical Definition of a Decision

A Decision is a formally identified, context-bound, time-scoped authorization object that represents the result of a validated request under a specific policy, risk posture, and baseline context.

A Decision is NOT:

- a generic access token
- a session
- a log entry
- a telemetry record

A Decision is:

- uniquely identifiable
- stateful
- temporally bounded
- linked to baseline context
- continuously re-evaluable

This definition SHALL be treated as canonical across all CAI-MX documents.

---

## 3. Design Principles

The CAI data model is governed by the following principles:

- **Determinism**: identical inputs MUST produce identical outputs
- **Traceability**: all state transitions MUST be reconstructable
- **Integrity**: all critical entities MUST be verifiable
- **Context Binding**: decisions MUST remain linked to baseline conditions
- **Temporal Consistency**: all evaluation-relevant entities MUST be time-aware
- **Federated Interoperability**: entities MUST be representable consistently across systems

---

## 4. Data Types and Conventions

### 4.1 Primitive Types

- `UUID`: RFC 4122 compliant identifier
- `TIMESTAMP`: ISO 8601 string in UTC
- `FLOAT`: normalized decimal value in [0.0, 1.0] unless explicitly stated otherwise
- `STRING`: UTF-8 encoded text
- `BOOLEAN`: true | false
- `INTEGER`: signed whole number

---

### 4.2 Naming Convention

All field names MUST use:

- `snake_case`
- lowercase only
- no whitespace
- no non-standard abbreviations

---

### 4.3 Nullability Convention

Unless otherwise specified:

- all fields are REQUIRED
- optional fields MUST be explicitly marked as OPTIONAL

---

### 4.4 Canonical Serialization

Any object used for hashing, signing, or integrity comparison MUST be serialized using:

- canonical JSON ordering
- no insignificant whitespace
- stable field ordering
- UTF-8 encoding

---

## 5. Enumerations

### 5.1 DecisionState

Allowed values:

- ISSUED
- VALIDATED
- DEGRADED
- REVALIDATION_REQUIRED
- REVOKED
- DENIED

---

### 5.2 EnforcementOutcome

Allowed values:

- ALLOW
- CONDITIONAL_ALLOW
- REQUIRE_REVALIDATION
- DENY
- REVOKE
- ESCALATE

---

### 5.3 ConfidenceLevel (OPTIONAL abstraction)

Allowed values:

- LOW
- MEDIUM
- HIGH

This enumeration MAY be derived from numerical confidence values.

---

## 6. Canonical Entity Set

The CAI system is composed of the following core entities:

1. Decision
2. BaselineContext
3. TelemetryRecord
4. RiskAssessment
5. DecisionEvent
6. EvidenceReference

These entities MUST remain semantically distinct.

---

## 7. Entity Separation Rules

### 7.1 Decision vs Context

- Decision = authorization object
- BaselineContext = immutable issuance conditions

A Decision MUST reference a BaselineContext but MUST NOT embed mutable runtime telemetry as baseline truth.

---

### 7.2 Context vs Telemetry

- BaselineContext = immutable snapshot at issuance
- TelemetryRecord = mutable runtime observation

These two entities MUST NOT be treated as interchangeable.

---

### 7.3 Risk vs Telemetry

- TelemetryRecord = raw or normalized observation
- RiskAssessment = computed evaluative result derived from telemetry and policy

Risk MUST NOT be treated as raw telemetry.

---

## 8. Decision Entity

### 8.1 Definition

A Decision is the primary authorization object subject to lifecycle control.

---

### 8.2 Schema

{
  "decision_id": "UUID",
  "subject_id": "STRING",
  "action": "STRING",
  "resource": "STRING",
  "origin_system": "STRING",
  "policy_version": "STRING",
  "schema_version": "STRING",
  "timestamp_issued": "TIMESTAMP",
  "validity_window": {
    "start": "TIMESTAMP",
    "end": "TIMESTAMP"
  },
  "baseline_context_id": "UUID",
  "context_hash": "STRING",
  "initial_risk_score": "FLOAT",
  "state": "DecisionState"
}

---

### 8.3 Constraints

- `decision_id` MUST be globally unique
- `timestamp_issued` MUST be within `validity_window`
- `validity_window.start < validity_window.end`
- `baseline_context_id` MUST reference an existing BaselineContext
- `initial_risk_score` MUST be within [0.0, 1.0]
- `context_hash` MUST match canonical serialization of the referenced BaselineContext

---

## 9. BaselineContext Entity

### 9.1 Definition

BaselineContext is the immutable representation of the environmental conditions at the moment of decision issuance.

It exists to preserve the authoritative reference point against which future telemetry is compared.

---

### 9.2 Schema

{
  "baseline_context_id": "UUID",
  "timestamp_captured": "TIMESTAMP",
  "identity": {
    "authentication_level": "STRING",
    "identity_confidence": "FLOAT"
  },
  "device": {
    "device_compliance": "BOOLEAN",
    "device_risk_score": "FLOAT"
  },
  "network": {
    "network_zone": "STRING",
    "network_risk_score": "FLOAT",
    "geo_location": "STRING"
  },
  "behavior": {
    "behavior_anomaly_score": "FLOAT"
  },
  "schema_version": "STRING"
}

---

### 9.3 Constraints

- all confidence and risk-related scores MUST be within [0.0, 1.0]
- `timestamp_captured` MUST be less than or equal to decision issuance time
- BaselineContext MUST be immutable after creation

---

## 10. TelemetryRecord Entity

### 10.1 Definition

TelemetryRecord is a time-scoped runtime observation used for revalidation, drift computation, and risk reassessment.

It is NOT baseline truth.

---

### 10.2 Schema

{
  "telemetry_id": "UUID",
  "decision_id": "UUID",
  "timestamp_observed": "TIMESTAMP",
  "source_system": "STRING",
  "identity": {
    "identity_confidence": "FLOAT"
  },
  "device": {
    "device_posture": "STRING",
    "device_risk_score": "FLOAT"
  },
  "network": {
    "network_risk_score": "FLOAT",
    "geo_location": "STRING",
    "ip_reputation": "STRING"
  },
  "behavior": {
    "behavior_anomaly_score": "FLOAT"
  },
  "telemetry_confidence": "FLOAT"
}

---

### 10.3 Constraints

- `decision_id` MUST reference an existing Decision
- `timestamp_observed` MUST be greater than or equal to decision issuance time
- `telemetry_confidence` MUST be within [0.0, 1.0]
- telemetry values MUST be normalized before use in rule evaluation

---

## 11. RiskAssessment Entity

### 11.1 Definition

RiskAssessment is the computed evaluation of current decision-related risk at a given time.

It is derived from telemetry, context, and policy logic.

---

### 11.2 Schema

{
  "risk_id": "UUID",
  "decision_id": "UUID",
  "timestamp_assessed": "TIMESTAMP",
  "risk_score": "FLOAT",
  "confidence": "FLOAT",
  "components": {
    "identity_risk": "FLOAT",
    "device_risk": "FLOAT",
    "network_risk": "FLOAT",
    "behavior_risk": "FLOAT"
  },
  "aggregation_mode": "STRING",
  "policy_version": "STRING"
}

---

### 11.3 Constraints

- all component scores MUST be within [0.0, 1.0]
- `risk_score` MUST be within [0.0, 1.0]
- `confidence` MUST be within [0.0, 1.0]
- `aggregation_mode` MUST identify the active risk aggregation strategy
- `decision_id` MUST reference an existing Decision

---

## 12. DecisionEvent Entity

### 12.1 Definition

DecisionEvent is an immutable record of a state transition or integrity-relevant lifecycle change.

---

### 12.2 Schema

{
  "event_id": "UUID",
  "decision_id": "UUID",
  "timestamp_recorded": "TIMESTAMP",
  "previous_state": "DecisionState",
  "new_state": "DecisionState",
  "trigger": "STRING",
  "risk_id": "UUID",
  "evidence_ids": ["UUID"]
}

---

### 12.3 Constraints

- `decision_id` MUST reference an existing Decision
- state transitions MUST follow valid lifecycle rules
- events MUST be append-only
- `risk_id` SHOULD reference the RiskAssessment used for transition
- `evidence_ids` SHOULD reference EvidenceReference objects supporting the transition

---

## 13. EvidenceReference Entity

### 13.1 Definition

EvidenceReference is a tamper-evident linkage to any artifact that supports, explains, or justifies a lifecycle decision or integrity evaluation.

---

### 13.2 Schema

{
  "evidence_id": "UUID",
  "decision_id": "UUID",
  "evidence_type": "STRING",
  "reference_uri": "STRING",
  "timestamp_recorded": "TIMESTAMP",
  "integrity_hash": "STRING",
  "source_system": "STRING"
}

---

### 13.3 Constraints

- `decision_id` MUST reference an existing Decision
- `integrity_hash` MUST be cryptographically verifiable
- evidence MUST be externally referencable or internally persistable
- evidence references MUST be immutable after creation

---

## 14. Relationship Model

The following relationships are mandatory:

- one Decision MUST reference exactly one BaselineContext
- one Decision MAY reference multiple TelemetryRecords
- one Decision MAY reference multiple RiskAssessments
- one Decision MAY reference multiple DecisionEvents
- one Decision MAY reference multiple EvidenceReferences

This forms the canonical decision integrity graph.

---

## 15. Context Hashing Model

### 15.1 Definition

The `context_hash` MUST be computed as:

HASH(canonical_json(BaselineContext))

---

### 15.2 Requirements

- canonical field order
- stable serialization
- deterministic encoding
- cryptographically secure hash function

---

## 16. Freshness Requirements

A TelemetryRecord MUST be considered stale if:

current_time - timestamp_observed > telemetry_freshness_threshold

The threshold MUST be policy-defined and system-consistent.

Stale telemetry MUST NOT be treated as equivalent to current runtime state.

---

## 17. Interoperability Requirements

To support federated environments:

- all systems MUST interpret normalized scores consistently
- all systems MUST preserve UUID continuity across propagation
- all systems MUST use canonical representations for Decision and BaselineContext
- no downstream system MAY reinterpret field semantics arbitrarily

This is required to preserve decision interoperability, not merely system connectivity.

---

## 18. Integrity Requirements

The system MUST ensure:

- BaselineContext immutability
- DecisionEvent append-only storage
- cryptographic verifiability of EvidenceReference
- stable linkage between Decision, RiskAssessment, and DecisionEvent
- canonical serialization for all integrity-sensitive comparisons

---

## 19. Storage Requirements

The system MUST support:

- indexed decision retrieval
- append-only event storage
- immutable evidence referencing
- time-series telemetry storage
- audit-oriented retention of lifecycle artifacts

---

## 20. Determinism Requirements

Given identical:

- Decision
- BaselineContext
- TelemetryRecord
- RiskAssessment policy logic

the system MUST produce identical evaluation outputs.

No hidden state MAY alter deterministic behavior.

---

## 21. Strategic Insight

Traditional systems store:

- access grants
- sessions
- events

CAI stores:

- a formal Decision
- a canonical BaselineContext
- runtime TelemetryRecords
- computed RiskAssessments
- immutable lifecycle events
- verifiable evidence linkages

This transforms decision handling from operational convenience into a formally governed integrity system.

---

## 22. Conclusion

This formal data model establishes the foundational structure required for CAI-MX implementation.

It ensures that decisions are:

- uniquely identifiable
- context-bound
- time-aware
- continuously evaluable
- interoperable across systems
- auditable under adversarial scrutiny

This data model is the canonical structural basis for all subsequent decision rules, risk computation, revalidation logic, and enforcement mechanisms.