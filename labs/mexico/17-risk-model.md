# CAI-MX – Formal Risk Model Specification

---

## 1. Purpose

This document defines the formal risk model for CAI (Cybersecurity Artificial Intelligence).

Its objective is to establish a deterministic, quantifiable, interoperable, and adversarially robust method for calculating, evaluating, and enforcing risk as a primary control variable for decision integrity.

This model provides the canonical source of truth for risk consumption by the decision rules defined in `16-decision-rules.md`.

---

## 2. Normative Scope

This specification governs the generation and evaluation of the `RiskAssessment` entity defined in `15-data-model.md`.

All decision rules MUST consume risk exclusively through this model.

No alternative risk computation logic is permitted during rule evaluation.

---

## 3. Definition of Risk

In CAI:

Risk is defined as:

the probability that execution of a decision, under current observable conditions, results in a security-relevant negative outcome.

Risk MUST be:

- time-dependent
- context-aware
- telemetry-driven
- bounded in [0.0, 1.0]
- continuously recomputed
- interoperable across systems

---

## 4. Risk Model Structure

A `RiskAssessment` consists of:

- a normalized aggregate risk score
- a vector of component risks
- a confidence value
- an aggregation mode
- a policy reference

---

## 5. Risk Dimensions

Risk MUST be decomposed into four canonical dimensions:

1. identity_risk
2. device_risk
3. network_risk
4. behavior_risk

All dimensions MUST be present and normalized.

---

## 6. Component Risk Definitions

### 6.1 Identity Risk

identity_risk = 1 - identity_confidence

Where:

- identity_confidence is derived from authentication strength, session integrity, and identity assurance mechanisms

---

### 6.2 Device Risk

device_risk = f(device_posture, compliance_status, vulnerability_state)

Where:

- compliant devices produce lower risk
- degraded posture increases risk

Function MUST be monotonic with respect to insecurity.

---

### 6.3 Network Risk

network_risk = f(ip_reputation, geo_deviation, network_zone)

Where:

- trusted zones reduce risk
- anomalous location or untrusted network increases risk

---

### 6.4 Behavioral Risk

behavior_risk = anomaly_score

Where:

- anomaly_score is normalized and derived from behavioral deviation models

---

## 7. Risk Normalization

All component risks MUST satisfy:

0.0 ≤ component_risk ≤ 1.0

Normalization MUST be consistent across all systems to preserve interoperability.

---

## 8. Risk Aggregation

### 8.1 Weighted Aggregation Function

R_weighted(t) = α₁ * identity_risk  
              + α₂ * device_risk  
              + α₃ * network_risk  
              + α₄ * behavior_risk  

Constraints:

- α₁ + α₂ + α₃ + α₄ = 1
- αᵢ ∈ [0.0, 1.0]
- weights MUST be policy-defined

---

### 8.2 Worst-Case Dominance Function

R_max(t) = max(identity_risk, device_risk, network_risk, behavior_risk)

---

### 8.3 Effective Risk Rule

The effective risk used by the decision engine MUST be:

R(t) = max(R_weighted(t), R_max(t)) IF any component exceeds critical component threshold  
ELSE  
R(t) = R_weighted(t)

This resolves conflict between aggregation and worst-case logic.

---

## 9. Adaptive Weighting

Weights MAY be dynamic:

αᵢ = f(context, policy, decision_type)

Example:

- privileged actions → higher device weight
- remote access → higher network weight

Weighting functions MUST remain deterministic.

---

## 10. Temporal Risk Evolution

Risk MUST be time-dependent:

R(t + Δt) ≠ R(t)

Changes are driven by:

- new telemetry
- context drift
- environmental variation

The system MUST recompute risk whenever new telemetry is ingested.

---

## 11. Risk Confidence

Each `RiskAssessment` MUST include:

confidence ∈ [0.0, 1.0]

Confidence represents:

- completeness of telemetry
- trustworthiness of sources
- internal consistency of signals

---

### 11.1 Confidence Rule

If:

confidence < confidence_min_threshold

Then:

- risk MUST be treated as unreliable
- decision rules MUST trigger REVALIDATION_REQUIRED

---

## 12. Risk Freshness

A risk value MUST be considered valid only if:

current_time - timestamp_assessed ≤ risk_freshness_threshold

If risk is stale:

- it MUST NOT be used for validation
- revalidation MUST be triggered

---

## 13. Risk Drift

Risk drift is defined as:

ΔR = |R(t) - R₀|

Where:

- R₀ = initial risk at decision issuance

---

### 13.1 Drift Rule

If:

ΔR ≥ risk_drift_threshold

Then:

- REVALIDATION_REQUIRED MUST be triggered

---

## 14. Cross-System Risk Consistency

### 14.1 Problem Definition

Different systems may:

- compute risk differently
- apply different weights
- interpret telemetry differently

This creates risk inconsistency.

---

### 14.2 Canonical Requirement

All systems MUST:

- use normalized risk representation [0.0, 1.0]
- apply consistent threshold semantics
- preserve component structure

---

### 14.3 Risk Divergence Rule

Let:

ΔR_system = |R_origin - R_local|

If:

ΔR_system ≥ ε

Then:

- decision MUST transition to REVALIDATION_REQUIRED

---

### 14.4 Local Recalculation Rule

Upon receiving a decision:

System B MUST:

- recompute risk using local telemetry
- compare against received risk
- enforce divergence constraints

---

## 15. Telemetry Dependency Rules

Risk MUST be computed from:

- fresh telemetry
- multi-source inputs
- normalized signals

Risk MUST NOT rely on:

- single-source telemetry
- stale inputs
- unverified signals

---

## 16. Adversarial Resilience Rules

The model MUST assume:

- telemetry manipulation
- signal delay
- risk masking attempts

Therefore:

- multi-source correlation MUST be applied
- anomaly detection MUST influence risk
- worst-case dominance MUST prevent masking

---

## 17. Fail-Safe Rules

If risk cannot be computed:

→ REVALIDATION_REQUIRED

If risk remains undefined:

→ REVOKED

Risk absence MUST NEVER result in implicit trust.

---

## 18. Integration with Decision Rules

The decision rules (16) MUST:

- consume `risk_score`
- respect thresholds ρ₁, ρ₂, ρ₃
- respect confidence constraints
- respect drift triggers

Decision rules MUST NOT override the risk model.

---

## 19. Determinism Requirements

Given identical:

- telemetry inputs
- baseline context
- policy configuration

The risk model MUST produce identical:

- component risks
- aggregate risk
- confidence values

No stochastic or hidden state behavior is permitted.

---

## 20. Strategic Insight

Traditional systems treat risk as a point-in-time evaluation.

CAI defines risk as:

a continuously evolving, formally structured, and interoperable control variable that governs decision validity.

---

## 21. Conclusion

This risk model establishes:

- a deterministic computation framework
- a multi-dimensional representation of risk
- a cross-system consistency mechanism
- an adversarially resilient evaluation process

This ensures that risk is not merely observed, but actively enforced as a governing factor in decision integrity.