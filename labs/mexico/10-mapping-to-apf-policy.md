# CAI-MX – Mapping to APF Cybersecurity Policy

## 1. Purpose

This document establishes a structured mapping between the CAI (Continuous Adaptive Integrity) model and the Mexican Federal Cybersecurity Policy for the Federal Public Administration (APF).

Its objective is to demonstrate not only alignment, but also the identification of structural gaps and the corresponding contribution of CAI as a decision integrity layer.

---

## 2. Positioning Statement

CAI does not replace the APF cybersecurity policy.

CAI operates as:

> **A decision integrity enforcement layer extending the APF framework into runtime decision assurance**

The APF policy defines **control domains and operational capabilities**.

CAI defines **how decision integrity is continuously validated and enforced at execution time**.

---

## 3. APF Capability Coverage

The APF cybersecurity framework establishes the following core capabilities:

- Identity and Access Management (IAM)
- Multi-Factor Authentication (MFA)
- Zero Trust principles
- Continuous monitoring (CSOC Federado)
- Incident response (CSIRT Nacional-APF)
- Risk management processes
- Security event correlation
- Governance and coordination

These capabilities establish a strong baseline for:

- Access control
- System visibility
- Event detection and response

---

## 4. Structural Gap Definition

The APF framework focuses on:

- Access validation  
- System monitoring  
- Incident detection  
- Risk response  

However, it does not formally define a mechanism for:

> **Validating decision-state consistency against environmental-state conditions at execution time**

This results in a structural gap between:

- Decision formulation  
- Decision execution  

---

## 5. Formal Gap Model (DSA vs ESA)

The gap can be expressed as the absence of control over the relationship between:

- **Decision State Awareness (DSA)**  
  → assumptions, constraints, and context at the moment a decision is defined  

- **Environmental State Awareness (ESA)**  
  → real-time conditions at the moment a decision is executed  

Without a validation mechanism:

- DSA may become inconsistent with ESA  
- Decisions may remain active despite context changes  
- Execution may occur under invalid conditions  

---

## 6. Structured Mapping Model

| APF Capability | Capability Scope | Gap Identified | CAI Contribution |
|---------------|-----------------|---------------|-----------------|
| IAM / MFA | Identity validation at access time | No validation beyond access event | Extends identity validation across decision lifecycle |
| Zero Trust | Continuous access verification | No decision-level verification | Enforces continuous validation at decision level |
| CSOC Monitoring | Event detection and correlation | No binding between telemetry and decisions | Binds telemetry to decision revalidation |
| CSIRT Response | Incident response actions | No validation before execution | Validates decisions prior to enforcement |
| Risk Management | Continuous risk evaluation | No direct linkage to decision execution | Integrates risk into decision admissibility |

---

## 7. CAI Extension Layers

CAI introduces capabilities not explicitly defined in APF:

### 7.1 Decision Lifecycle Model
Defines decision states, transitions, and lifecycle validation.

### 7.2 Telemetry Binding
Links real-time signals to decision evaluation (ESA integration).

### 7.3 Evidence Model
Creates structured, decision-level evidence for audit and traceability.

### 7.4 Revalidation Engine
Continuously evaluates decision validity against environmental conditions.

### 7.5 Contamination Control
Prevents propagation of invalid decisions across systems.

### 7.6 Traceability Model
Reconstructs full decision lifecycle across distributed environments.

### 7.7 Enforcement Outcomes
Ensures that execution is conditional upon validated integrity.

---

## 8. Enforcement Boundary

CAI introduces a formal:

> **Decision Enforcement Boundary**

At this boundary:

- DSA is compared against ESA  
- Integrity thresholds are evaluated  
- Decisions are either:

  - Executed (within threshold)  
  - Revalidated  
  - Blocked  

---

## 9. Complementary Role

CAI does not duplicate APF controls.

Instead, it:

- Connects existing capabilities  
- Extends them into decision-level assurance  
- Enforces consistency across system boundaries  

---

## 10. Operational Impact

Without CAI:

- Decisions may persist beyond valid conditions  
- Monitoring detects issues after execution  
- Risk propagates across systems  

With CAI:

- Decisions are continuously validated  
- Execution is context-dependent  
- Risk is contained before impact  

---

## 11. Strategic Differentiation

The APF framework ensures:

- Secure access  
- Monitored systems  
- Responsive operations  

CAI ensures:

> **Decision integrity across time, context, and execution boundaries**

---

## 12. Defensive Positioning

CAI is not:

- A replacement framework  
- A competing standard  
- A theoretical overlay  

CAI is:

- A runtime validation layer  
- A decision integrity enforcement mechanism  
- An architectural extension required for dynamic environments  

---

## 13. Final Assertion

A system can fully comply with the APF cybersecurity policy and still:

- Execute outdated decisions  
- Operate under invalid context  
- Propagate risk across systems  

CAI resolves this by ensuring that:

> **Decisions must continuously prove their validity before execution**

---

## 14. Conclusion

The APF cybersecurity policy defines a strong operational security foundation.

CAI completes this foundation by introducing:

- Decision lifecycle control  
- Continuous validation (DSA vs ESA)  
- Enforcement at execution boundary  

Together, they form:

> **A coherent, enforceable, and resilient cybersecurity model**