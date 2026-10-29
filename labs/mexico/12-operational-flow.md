# CAI-MX – Operational Flow

> Proposed design reconciliation CHG-CAI-RECON-2026-10-22-001. Not an approved revision
> or executed validation. Canonical MX references: 15 (entities), 16 (rules),
> 17 (risk). Preserve original authorship and source baseline.

---

## 1. Purpose

This document defines the operational flow of CAI (Cybersecurity Artificial Intelligence) within the APF cybersecurity environment.

Its objective is to describe, step by step, how decisions are created, evaluated, propagated, revalidated, and enforced in real-time conditions.

---

## 2. Operational Perspective

The APF framework provides:

- identity validation (IAM / MFA)
- Zero Trust access control
- continuous monitoring (CSOC)
- incident response (CSIRT)

CAI introduces a continuous operational flow where:

> decisions are evaluated not once, but continuously throughout their lifecycle.

---

## 3. High-Level Flow

The operational flow consists of the following stages:

1. Request Initiation  
2. Identity Validation  
3. Decision Issuance  
4. Decision Registration  
5. Telemetry Binding  
6. Continuous Evaluation  
7. Decision Propagation  
8. Execution Gate  
9. Revalidation  
10. Enforcement Outcome  
11. Trace Closure  

---

## 4. Step-by-Step Flow

---

### 4.1 Request Initiation

A subject initiates a request:

- access to a system  
- execution of an action  
- authorization for an operation  

Inputs include:

- identity credentials  
- device context  
- network context  
- behavioral context  

---

### 4.2 Identity Validation

The system performs:

- authentication (MFA)  
- identity verification  
- Zero Trust checks  

Outcome:

- identity is validated or rejected  

---

### 4.3 Decision Issuance

If validation succeeds:

- System A captures and verifies the immutable BaselineContext before issuance
- Capture time is no later than issuance time
- System A generates the Decision UUID and binds the existing context reference
  and verified hash under a versioned policy before issuing the Decision

The decision includes:

- subject identity  
- action scope  
- resource scope  
- contextual baseline  
- risk level  

---

### 4.4 Decision Registration

The decision is registered in the CAI Integrity Layer:

- retains the unique identifier assigned at issuance
- linked to initial telemetry  
- stored for lifecycle tracking  

---

### 4.5 Telemetry Binding

CAI binds the decision to real-time telemetry:

- identity signals  
- device posture  
- network conditions  
- behavioral patterns  

This associates runtime observations with the already captured immutable
BaselineContext. It does not create a baseline retroactively or overwrite it.

---

### 4.6 Continuous Evaluation

The Revalidation Engine begins continuous evaluation:

- compares current telemetry with baseline  
- monitors drift  
- evaluates risk thresholds  

This process is continuous and dynamic.

---

### 4.7 Decision Propagation

The decision is transmitted to another system:

System A → System B  

At this stage:

- context may differ  
- telemetry may be incomplete  
- trust assumptions may exist  

CAI flags this as a **critical control point**.

---

### 4.8 Execution Gate

Before execution:

System B must validate:

- current context alignment  
- telemetry consistency  
- decision integrity  

If validation is not performed:

> execution becomes a blind trust action  

CAI prevents this.

---

### 4.9 Revalidation

If drift is detected:

- CAI triggers revalidation  

Process:

- re-evaluate policy  
- reassess risk  
- compare telemetry  
- update decision state  

---

### 4.10 Enforcement Outcome

Based on revalidation:

- allow  
- conditional allow  
- require revalidation  
- deny  
- revoke  
- escalate  

This directly controls execution behavior.

---

### 4.11 Trace Closure

All actions are recorded:

- decision origin  
- lifecycle transitions  
- telemetry changes  
- enforcement outcomes  

This enables:

- auditability  
- forensic reconstruction  
- policy refinement  

---

## 5. Runtime Characteristics

The CAI operational flow is:

- continuous  
- event-driven  
- telemetry-driven  
- context-aware  

It does not rely on:

- static validation  
- one-time decisions  

---

## 6. Failure Scenario (Without CAI)

Without CAI:

1. decision is issued  
2. decision is propagated  
3. context changes  
4. decision is executed anyway  

Result:

- invalid execution  
- increased risk  
- delayed detection  

---

## 7. Controlled Scenario (With CAI)

With CAI:

1. decision is issued  
2. telemetry is bound  
3. context changes  
4. revalidation is triggered  
5. execution is gated  
6. decision is revoked or adjusted  

Result:

- execution prevented or controlled  
- integrity preserved  
- risk contained  

---

## 8. Integration with APF

The operational flow integrates with:

- IAM → identity validation  
- Zero Trust → initial access control  
- CSOC → telemetry ingestion  
- CSIRT → escalation handling  

CAI connects these components into a continuous decision flow.

---

## 9. Strategic Insight

Traditional systems operate in phases:

- validate → execute → monitor  

CAI operates in a loop:

> validate → evaluate → revalidate → enforce → repeat  

---

## 10. Conclusion

The operational flow defines how CAI functions in real-time environments.

It ensures that:

> decisions are not executed because they were valid once,  
> but because they remain valid at the exact moment of execution.