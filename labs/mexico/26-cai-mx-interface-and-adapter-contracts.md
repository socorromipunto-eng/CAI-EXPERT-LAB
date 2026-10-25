# CAI-MX – Interface and Adapter Contracts

> Proposed design reconciliation CHG-CAI-RECON-2026-10-22-001. Not an approved revision
> or executed validation. Canonical MX references: 15 (entities), 16 (rules),
> 17 (risk). Preserve original authorship and source baseline.

---

## 1. Purpose

This document defines the formal interface contracts and adapter models required to integrate CAI (Cybersecurity Artificial Intelligence) into operational systems.

Its objective is to establish:

- standardized decision input structures (DSA)
- telemetry ingestion models (ESA)
- validation request/response contracts
- enforcement semantics at execution boundaries
- interoperability mechanisms across heterogeneous systems

---

## 2. Contract Principle

CAI operates through:

> explicit, enforceable interface contracts between decision systems, telemetry sources, and execution layers

These contracts ensure:

- deterministic validation behavior  
- cross-system consistency  
- interoperability in federated environments  
- controlled enforcement at runtime  

---

## 3. Core Interaction Model

CAI operates through three primary interaction flows:

1. Decision Submission (DSA input)  
2. Telemetry Ingestion (ESA input)  
3. Validation and Enforcement Output  

These flows define the boundary between:

- decision definition  
- environmental observation  
- execution control  

---

## 4. Decision Submission Contract (DSA)

The wire representation preserves the canonical Decision in `15-data-model.md`
section 8: decision_id, subject_id, action, resource, origin_system,
policy_version, schema_version, timestamp_issued, validity_window.start/end,
baseline_context_id, context_hash, initial_risk_score and state are required.
Identifiers satisfy the canonical UUID type. The immutable BaselineContext in
section 9 exists and is verified before issuance; the Decision references it.
Mutable telemetry must not replace baseline truth. Use the canonical schema,
not a second shortened JSON example. Serialization/hash profile and the actual
transport schema version require adoption before interoperability is claimed.

## 5. Telemetry Input Contract (ESA)

Telemetry used for a Decision satisfies TelemetryRecord in document 15 section
10, including telemetry_id, required decision_id, timestamp_observed,
source_system, canonical identity/device/network/behavior fields and
telemetry_confidence. decision_id references an existing Decision.
A source-native event without correlation is not yet a canonical record eligible
for that decision. A named adapter must evidence correlation, source authority,
ordering, completeness and freshness. Partial updates cannot silently replace
an authoritative record. RiskAssessment remains distinct from telemetry.

## 6. Validation Request Interface

The consumer identifies the canonical Decision UUID before an effect. The
evaluator retrieves the immutable context, versioned policy, source-validated
telemetry, compatible RiskAssessment and recorded evaluation time, then applies
`16-decision-rules.md` in its defined precedence order. Client overrides cannot
change authority, baseline or scope outside an explicitly authorized workflow.

## 7. Validation Response Contract

DecisionState and EnforcementOutcome are distinct types. Preserve all canonical
outcomes rather than compressing them to ALLOW/DENY/REVALIDATE.

| DecisionState | Primary EnforcementOutcome | Boundary behavior |
|---|---|---|
| ISSUED | No permission yet | Evaluate before any effect |
| VALIDATED | ALLOW | Only the evaluated, still-valid scope may proceed |
| DEGRADED | CONDITIONAL_ALLOW | All explicit restrictions must be supported and enforced |
| REVALIDATION_REQUIRED | REQUIRE_REVALIDATION | Suspend effects pending revalidation |
| REVOKED | REVOKE | Invalidate authorization; reconcile dependent effects |
| DENIED | DENY | Block the effect |

ESCALATE is an additional canonical outcome/notification under document 16
section 13. It never independently authorizes execution or suppresses a blocking
outcome. A response preserves the Decision UUID, state, outcome, cause and
canonical event/evidence references. The adopted transport schema must bind
scope, evaluation snapshot, policy/schema versions, validity and integrity.
This design contract is not an implemented authorization token.

## 8. Enforcement Contract

Only an admissible ALLOW or a supported, enforceable CONDITIONAL_ALLOW can
permit the evaluated effect. Unsupported conditions, unknown outcomes, missing
bindings, integrity failures, errors and expired responses never permit effects.
REQUIRE_REVALIDATION, DENY, REVOKE and ESCALATE do not independently authorize
execution. Asynchronous preparation cannot authorize execution before the gate
required by document 16 section 14. Revalidation occurs at system boundaries
and immediately before dispatch under the adopted validity/authority contract.
A new denial is not evidence that an earlier partial effect was rolled back.

A legacy adapter may translate REVALIDATE to REQUIRE_REVALIDATION only through
a named, versioned, non-permitting mapping. Reject or HOLD lossy mappings and
missing fields; never guess UUIDs, versions, baselines or risk assessments.

---

## 9. Adapter Model

Due to system heterogeneity, CAI operates through adapters.

Adapters define the translation layer between native systems and CAI contracts.

Responsibilities
normalize decision and telemetry formats
enforce contract compliance
translate protocols and data models
preserve semantic integrity across systems
Constraint

Adapters must not alter:

decision intent
contextual meaning
validation semantics
## 10. Integration Patterns

CAI supports multiple integration patterns:

10.1 Synchronous Validation
request-response before execution
deterministic control
10.2 Asynchronous Validation
event-driven validation
asynchronous preparation with effects blocked until the pre-execution gate passes
10.3 Hybrid Model
initial validation
continuous revalidation
## 11. Error Handling

Failure scenarios include:

missing telemetry
delayed ESA updates
inconsistent decision context
Required behavior
default to conservative enforcement
return the canonical blocking/revalidation outcome with its cause recorded
log and trace all failures
## 12. Security Requirements

All interfaces must ensure:

authentication of calling systems
integrity of transmitted data
secure communication channels
## 13. Versioning and Evolution

Interfaces must support:

backward compatibility
versioned contracts
incremental system integration
## 14. Interoperability

Contracts must be:

technology-agnostic
platform-independent
adaptable to institutional constraints
## 15. Conclusion

These contracts define how CAI integrates at the system level.

They ensure that:

decisions are consistently evaluated
telemetry is correctly interpreted
enforcement is deterministic and verifiable

This establishes CAI as:

an interoperable, enforceable decision integrity system operating at execution boundaries