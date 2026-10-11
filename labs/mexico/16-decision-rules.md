# CAI-MX – Formal Decision Rules Specification

---

## 1. Purpose

This document defines the formal decision rules governing the CAI (Continuous Adaptive Integrity) model.

Its objective is to establish a deterministic, auditable, and implementable rule system that governs:

- decision validation
- context drift evaluation
- risk-based state transitions
- revalidation
- revocation
- enforcement outcomes

This specification is the canonical behavioral layer built on top of the formal data model defined in `15-data-model.md`.

---

## 2. Normative Scope

These rules apply to every `Decision` object managed by CAI-MX.

All evaluations MUST operate on the canonical entities defined in the data model:

- `Decision`
- `BaselineContext`
- `TelemetryRecord`
- `RiskAssessment`
- `DecisionEvent`
- `EvidenceReference`

No alternative interpretation of these entities is permitted during rule execution.

---

## 3. Canonical Rule Principle

In CAI:

A decision is NOT valid because it was issued.

A decision is valid only if, at evaluation time, it satisfies all of the following:

1. temporal validity
2. context consistency
3. telemetry freshness
4. acceptable computed risk
5. policy compliance
6. sufficient confidence

Therefore, decision validity is time-dependent and continuously re-evaluable.

---

## 4. Formal Validity Function

Decision validity at time `t` is defined as:

D(t) = f(B, T(t), R(t), P, τ)

Where:

- `D(t)` = decision validity at time `t`
- `B` = immutable `BaselineContext`
- `T(t)` = current `TelemetryRecord`
- `R(t)` = current `RiskAssessment`
- `P` = active policy and thresholds
- `τ` = temporal validity constraints

The output of `D(t)` MUST deterministically produce:

- a `DecisionState`
- an `EnforcementOutcome`

---

## 5. Input Preconditions

Before any rule is executed, the following conditions MUST be checked:

### 5.1 Entity Presence

The system MUST confirm that:

- a valid `Decision` exists
- the `Decision` references a valid `BaselineContext`
- at least one current or candidate `TelemetryRecord` is available, unless fail-safe logic is triggered
- a `RiskAssessment` can be computed or verified

If any mandatory dependency is absent:

→ state MUST transition to `REVALIDATION_REQUIRED`

If unresolved after policy-defined handling:

→ state MUST transition to `REVOKED`

---

## 6. Temporal Validity Rules

### 6.1 Validity Window Rule

A `Decision` MUST satisfy:

current_time >= validity_window.start  
AND  
current_time <= validity_window.end

If:

current_time > validity_window.end

Then:

- `DecisionState` → `REVOKED`
- `EnforcementOutcome` → `REVOKE`

---

### 6.2 Telemetry Freshness Rule

A `TelemetryRecord` MUST satisfy:

current_time - timestamp_observed <= telemetry_freshness_threshold

If telemetry is stale:

- telemetry MUST NOT be treated as current truth
- state MUST transition to `REVALIDATION_REQUIRED`

If stale telemetry cannot be replaced within policy-defined tolerances:

- state MUST transition to `REVOKED`

---

## 7. Context Consistency Rules

### 7.1 Baseline–Telemetry Separation Rule

`BaselineContext` is immutable issuance truth.  
`TelemetryRecord` is mutable runtime observation.

The system MUST compare runtime telemetry against baseline context.  
It MUST NOT replace baseline context with telemetry.

---

### 7.2 Context Drift Function

Context drift is defined as the deviation between `BaselineContext` and current `TelemetryRecord`.

For normalized dimensions:

drift_identity  = |B.identity.identity_confidence - T.identity.identity_confidence|  
drift_device    = |B.device.device_risk_score - T.device.device_risk_score|  
drift_network   = |B.network.network_risk_score - T.network.network_risk_score|  
drift_behavior  = |B.behavior.behavior_anomaly_score - T.behavior.behavior_anomaly_score|

---

### 7.3 Weighted Drift Rule

Total drift MUST be computed as:

drift_total = w₁ * drift_identity  
            + w₂ * drift_device  
            + w₃ * drift_network  
            + w₄ * drift_behavior

Constraints:

- w₁ + w₂ + w₃ + w₄ = 1
- each weight MUST be in [0.0, 1.0]
- all compared values MUST be normalized to [0.0, 1.0]

---

### 7.4 Drift Threshold Rules

The active policy MUST define:

- θ₁ = acceptable drift threshold
- θ₂ = elevated drift threshold
- θ₃ = critical drift threshold

Rule outcomes:

- if drift_total <= θ₁ → drift is acceptable
- if θ₁ < drift_total <= θ₂ → drift is elevated
- if θ₂ < drift_total < θ₃ → drift is severe
- if drift_total >= θ₃ → drift is critical

---

## 8. Risk Rules

### 8.1 Canonical Risk Source Rule

Risk evaluation MUST use the canonical `RiskAssessment` produced according to `17-risk-model.md`.

Decision rules MUST NOT independently redefine the risk model.

They may only consume:

- `risk_score`
- risk component values
- `confidence`
- policy-defined thresholds

---

### 8.2 Risk Threshold Rules

The active policy MUST define:

- ρ₁ = acceptable risk threshold
- ρ₂ = elevated risk threshold
- ρ₃ = critical risk threshold

Rule outcomes:

- if risk_score <= ρ₁ → acceptable risk
- if ρ₁ < risk_score <= ρ₂ → elevated risk
- if ρ₂ < risk_score < ρ₃ → severe risk
- if risk_score >= ρ₃ → critical risk

---

### 8.3 Worst-Case Dominance Rule

If any single component risk exceeds the critical component threshold, the rule engine MAY override weighted aggregation and apply worst-case dominance.

In such case:

effective_risk = max(component_risk)

If effective_risk exceeds critical policy threshold:

→ state MUST transition to `REVOKED`

Worst-case dominance MUST take precedence over benign aggregate appearance.

---

## 9. Confidence Rules

### 9.1 Confidence Dependency Rule

Every `RiskAssessment` MUST include a confidence value.

If:

confidence < confidence_min_threshold

Then:

- state MUST transition to `REVALIDATION_REQUIRED`

If confidence remains below threshold after policy-defined retry or corroboration mechanisms:

- state MUST transition to `REVOKED`

---

### 9.2 Missing or Contradictory Telemetry Rule

If telemetry is:

- incomplete
- contradictory
- untrusted
- non-correlatable

Then the system MUST degrade trust.

This MUST result in:

- `DecisionState` → `REVALIDATION_REQUIRED`

and, if unresolved:

- `DecisionState` → `REVOKED`

---

## 10. Policy Compliance Rules

### 10.1 Policy Violation Rule

If the active policy explicitly forbids the action, resource, scope, or runtime condition:

→ `DecisionState` MUST transition to `DENIED`

This rule has immediate precedence regardless of drift or computed risk.

---

### 10.2 Policy Version Consistency Rule

If the policy version applied at evaluation time is incompatible with the policy version associated with the `Decision`, and backward validity is not explicitly guaranteed:

→ `DecisionState` MUST transition to `REVALIDATION_REQUIRED`

---

## 11. State Transition Rules

### 11.1 ISSUED → VALIDATED

A decision MAY transition from `ISSUED` to `VALIDATED` only if all of the following hold:

- temporal validity satisfied
- telemetry freshness satisfied
- drift_total <= θ₁
- risk_score <= ρ₁
- confidence >= confidence_min_threshold
- no policy violation exists

---

### 11.2 VALIDATED → DEGRADED

A decision MUST transition from `VALIDATED` to `DEGRADED` if any of the following hold, while critical failure has not yet occurred:

- θ₁ < drift_total <= θ₂
- ρ₁ < risk_score <= ρ₂
- minor policy tension exists without explicit prohibition
- telemetry confidence is reduced but still above fail-safe threshold

---

### 11.3 DEGRADED → REVALIDATION_REQUIRED

A decision MUST transition from `DEGRADED` to `REVALIDATION_REQUIRED` if any of the following hold:

- drift_total > θ₂
- risk_score > ρ₂
- telemetry freshness violated
- telemetry contradiction detected
- cross-system divergence exceeds permitted tolerance
- confidence falls below minimum threshold

---

### 11.4 REVALIDATION_REQUIRED → VALIDATED

A decision MAY return to `VALIDATED` only if formal revalidation succeeds and all baseline criteria for validation are re-established.

This requires:

- fresh telemetry
- recomputed acceptable risk
- acceptable drift
- adequate confidence
- no policy violation

No direct rollback is permitted without explicit revalidation.

---

### 11.5 ANY STATE → REVOKED

A decision MUST transition to `REVOKED` if any of the following hold:

- temporal validity expired
- drift_total >= θ₃
- risk_score >= ρ₃
- worst-case dominance activated at critical level
- unresolved telemetry uncertainty persists beyond policy tolerance
- trust contamination is confirmed
- downstream execution risk is no longer acceptable

---

### 11.6 ANY STATE → DENIED

A decision MUST transition to `DENIED` if:

- explicit policy violation exists
- action scope is no longer legally or operationally permissible
- required authorization basis does not exist

---

## 12. Cross-System Rules

### 12.1 Propagation Revalidation Rule

Whenever a `Decision` crosses from `origin_system` to another consuming system, the receiving system MUST treat propagation as an integrity control point.

The consuming system MUST:

- validate identifier continuity
- verify policy compatibility
- compute local risk
- compare runtime telemetry with the original baseline
- revalidate before execution if divergence exceeds tolerance

---

### 12.2 Risk Divergence Rule

Let:

ΔR = |R_origin - R_local|

If:

ΔR >= ε

Then:

- `DecisionState` MUST transition to `REVALIDATION_REQUIRED`

This prevents interoperability without semantic risk consistency.

---

### 12.3 Semantic Continuity Rule

No downstream system MAY reinterpret the meaning of:

- action
- resource
- risk semantics
- threshold semantics

without triggering explicit revalidation.

---

## 13. Enforcement Mapping Rules

The rule engine MUST produce the following enforcement outcomes:

- `VALIDATED` → `ALLOW`
- `DEGRADED` → `CONDITIONAL_ALLOW`
- `REVALIDATION_REQUIRED` → `REQUIRE_REVALIDATION`
- `REVOKED` → `REVOKE`
- `DENIED` → `DENY`

If the state implies systemic risk or attack suspicion, the engine MAY additionally produce:

- `ESCALATE`

for CSOC / CSIRT integration.

---

## 14. Enforcement Timing Rule

Enforcement MUST occur BEFORE execution.

No decision MAY be executed first and revalidated later as a normal operating condition.

Any model that permits execution before integrity evaluation SHALL be considered non-compliant with CAI.

---

## 15. Revalidation Rules

Formal revalidation MUST include, at minimum:

1. fresh telemetry acquisition
2. risk recomputation
3. policy re-evaluation
4. drift recomputation
5. confidence verification
6. cross-system divergence check if applicable

If any mandatory revalidation step fails:

→ `DecisionState` MUST transition to `REVOKED` unless policy explicitly allows temporary degraded handling

---

## 16. Determinism Rules

Given identical values for:

- `Decision`
- `BaselineContext`
- `TelemetryRecord`
- `RiskAssessment`
- active policy thresholds

the engine MUST produce identical:

- `DecisionState`
- `EnforcementOutcome`

No hidden state, heuristic drift, or non-canonical interpretation MAY alter deterministic behavior.

---

## 17. Event Recording Rules

Every state transition MUST generate a `DecisionEvent`.

Each `DecisionEvent` SHOULD include:

- `decision_id`
- `previous_state`
- `new_state`
- `trigger`
- `risk_id`
- associated `evidence_ids`

No state transition MAY occur silently.

---

## 18. Fail-Safe Rules

If the system cannot establish safe continued validity because of:

- stale telemetry
- missing telemetry
- low confidence
- system divergence
- unresolved policy ambiguity

the engine MUST degrade trust rather than preserve it.

Fail-safe precedence:

1. `REVALIDATION_REQUIRED`
2. `REVOKED` if unresolved

---

## 19. Rule Precedence Order

If multiple rules fire simultaneously, precedence MUST be:

1. explicit policy denial
2. critical temporal violation
3. critical drift
4. critical risk
5. worst-case dominance trigger
6. low-confidence fail-safe
7. severe drift/risk revalidation
8. degraded state logic
9. validated state logic

This ordering prevents benign rules from masking critical ones.

---

## 20. Strategic Insight

Traditional systems validate access at discrete checkpoints.

CAI governs decisions through:

- context-aware rules
- drift-aware rules
- risk-aware rules
- time-aware rules
- cross-system consistency rules

This transforms decision handling from static authorization into formal integrity governance.

---

## 21. Conclusion

This specification defines the canonical behavioral logic of CAI-MX.

It ensures that decisions are:

- not trusted by default
- not preserved by inertia
- not executed under uncertainty
- not propagated without semantic control

Instead, decisions are continuously governed through deterministic, auditable, and interoperable rules that preserve integrity across time, context, and federated system boundaries.