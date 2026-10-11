# CAI-MX – Decision State Model

---

## 1. Purpose

This document defines the CAI (Continuous Adaptive Integrity) Decision State Model applied to the APF cybersecurity framework.

The objective is to formalize how decisions behave, evolve, and degrade over time across federated systems.

This model extends beyond access validation and introduces a state-driven integrity framework for decisions.

---

## 2. Conceptual Foundation

Traditional cybersecurity models treat decisions as outputs of a validation process.

Under CAI:

> A decision is not a static output.  
> A decision is a stateful entity bound to context.

This implies that a decision must:

- Maintain validity over time
- React to environmental changes
- Be continuously verifiable

---

## 3. Decision as a Stateful Object

A decision contains:

- Identity context
- Environmental context
- Policy evaluation result
- Timestamp of issuance
- Associated telemetry baseline

Once created, the decision becomes an entity that evolves over time.

---

## 4. Decision States

### 4.1 ISSUED

The decision is created after:

- Identity validation (IAM, MFA)
- Policy enforcement
- Initial context verification

At this stage:

- Decision is valid ONLY under original conditions

---

### 4.2 VALIDATED

The decision is verified against:

- Current telemetry
- Risk signals
- Policy constraints

This state confirms that the decision is still aligned with the environment.

---

### 4.3 PROPAGATED

The decision is transmitted to another system.

Characteristics:

- Cross-system boundary
- Trust is assumed but not enforced
- Context consistency is not guaranteed

---

### 4.4 DEGRADED

The decision enters a degraded state when:

- Device posture changes
- Network risk increases
- Behavioral anomalies appear
- System conditions diverge

At this stage:

> Decision integrity is uncertain

---

### 4.5 REVALIDATION REQUIRED

Triggered when:

- Context drift exceeds acceptable thresholds
- Telemetry contradicts original conditions

System must:

- Pause execution
- Re-evaluate decision

---

### 4.6 REVOKED

The decision is invalidated when:

- Risk exceeds tolerance
- Context no longer supports authorization
- Integrity cannot be restored

---

## 5. State Transitions

State transitions are dynamic and telemetry-driven.

Example flow:

ISSUED → VALIDATED → PROPAGATED → DEGRADED → REVALIDATION REQUIRED → REVOKED

Transitions depend on:

- Continuous telemetry
- Policy thresholds
- Context evaluation

---

## 6. Telemetry Dependency

State transitions are driven by:

- Device posture signals
- Network trust level
- Behavioral analytics
- System health indicators

Without telemetry:

- State awareness collapses
- Decisions become static artifacts

---

## 7. Policy Interaction

Policies define:

- Acceptable thresholds
- Revalidation triggers
- Revocation conditions

CAI ensures policies are:

- Continuously enforced
- Context-aware
- Decision-centric

---

## 8. Gap in APF Framework

The APF cybersecurity policy defines:

- Access validation
- Monitoring
- Risk management

However, it does NOT define:

- Decision states
- Decision lifecycle transitions
- Context-bound decision validity

---

## 9. CAI Contribution

CAI introduces:

- A formal state model for decisions
- Continuous integrity validation
- Context-aware lifecycle enforcement

---

## 10. Impact

Without a state model:

- Decisions persist beyond valid context
- Systems trust outdated assertions
- Risk propagates silently

With CAI:

- Decisions are continuously validated
- Context drift is enforced
- Integrity is preserved across systems

---

## 11. Conclusion

The introduction of a state model transforms decisions from:

- Static authorization outputs

into:

> Dynamic, verifiable, and enforceable entities.

This enables a new security paradigm:

> Decision-centric integrity enforcement across federated environments.