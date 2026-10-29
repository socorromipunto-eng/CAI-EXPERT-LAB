# CAI-MX Positioning: Decision Integrity Layer within the APF Cybersecurity Model

> Proposed design reconciliation CHG-CAI-RECON-2026-10-22-001. Not an approved revision
> or executed validation. Canonical MX references: 15 (entities), 16 (rules),
> 17 (risk). Preserve original authorship and source baseline.

## 1. Positioning Objective

This document defines the formal positioning of CAI-MX within the cybersecurity model established by the **Política General de Ciberseguridad para la Administración Pública Federal (APF)**.

The objective is to clarify:

- What CAI is within the national ecosystem  
- What CAI is NOT  
- Where CAI operates  
- What capability CAI introduces beyond the explicitly defined mechanisms in the APF model  

---

## 2. Architectural Principle

CAI-MX is not a replacement framework.

It operates as a:

> **Transversal Decision Integrity Layer**

designed to function across existing cybersecurity components without modifying their responsibilities.

---

## 3. Non-Disruptive Integration

CAI-MX preserves the structure defined by the APF policy.

### CAI does NOT replace:

- ATDT (governance authority)  
- DGCiber (technical coordination)  
- CSIRT Nacional-APF (incident response)  
- CSOC Nacional Federado (monitoring and detection)  
- Institutional RIC roles  

These components remain fully responsible for governance, detection, and response.

---

## 4. Functional Position within the APF Model

CAI-MX operates at the **decision-execution boundary**.

### Simplified operational flow:

1. CSOC performs detection and correlation  
2. CSIRT defines response strategy  
3. CAI evaluates decision admissibility  
4. Execution layer enforces only validated decisions  

---

## 5. Capability Introduced by CAI

The APF model defines:

- Detection (CSOC)  
- Response (CSIRT)  
- Governance and risk management  
- Control and compliance mechanisms  

However, it does not formally define a mechanism that ensures:

- Decisions remain valid at runtime  
- Contextual integrity is preserved during execution  
- Drift between decision assumptions and real conditions is detected  
- Enforcement occurs only under validated conditions  

CAI introduces this capability as:

> **Continuous Decision Assurance**

---

## 6. Decision Integrity Model

CAI-MX formalizes decision validation through the relationship between:

- **Decision State Awareness (DSA)**  
  → assumptions, constraints, and context under which a decision is made  

- **Environmental State Awareness (ESA)**  
  → real-time conditions at the moment of execution  

A mismatch between DSA and ESA results in:

- Potential invalid execution  
- Deviation from intended outcomes  
- Loss of operational consistency  

CAI ensures that this mismatch is detected and controlled before execution.

---

## 7. Integration Model

CAI-MX integrates as a **control layer**, not as a control authority.

| Component | Role | CAI Interaction |
|----------|------|----------------|
| CSOC | Detection | Provides telemetry and environmental signals |
| CSIRT | Decision | Generates candidate actions |
| CAI | Validation | Evaluates decision integrity and admissibility |
| Execution | Action | Executes only validated decisions |

---

## 8. Enforcement Boundary

CAI introduces a formal:

> **Decision Enforcement Boundary**

At this boundary:

- Decisions are evaluated against integrity thresholds  
- DSA is compared against ESA  
- Contextual consistency is verified  

### Outcome conditions:

- Within threshold → execution allowed  
- Outside threshold → revalidation or blocking  

---

## 9. Risk and Integrity Alignment

CAI does not redefine risk models.

Instead, it:

- Uses existing risk context  
- Ensures decisions remain aligned with that context  
- Detects inconsistencies between risk state and action  

This reinforces continuous risk management within the APF model.

---

## 10. Operational Impact

With CAI-MX integrated:

- Decision drift is reduced  
- Invalid or misaligned actions can be blocked  
- Execution becomes context-aware  
- Traceability is preserved across all stages  

These effects can be evaluated through:

- Consistency under equivalent conditions  
- Reduction in decision variance  
- Detection rate of DSA vs ESA mismatch  

---

## 11. Strategic Value

CAI-MX extends the APF cybersecurity model by introducing:

> **Decision Integrity as an enforceable operational capability**

This transforms the model from:

- Control-based enforcement  

to:

- Context-aware, continuously validated execution  

---

## 12. Scope Clarification

CAI-MX is:

- A validation layer  
- An assurance mechanism  
- An architectural extension  

CAI-MX is NOT:

- A replacement for governance  
- A monitoring system  
- A standalone cybersecurity framework  

---

## 13. Conclusion

CAI-MX complements the APF cybersecurity model by addressing a structural gap:

> The absence of a formal mechanism for ensuring decision integrity between formulation and execution.

By introducing continuous validation and enforcement at runtime, CAI-MX strengthens:

- Operational consistency  
- Risk alignment  
- System resilience  

without disrupting the existing national architecture.