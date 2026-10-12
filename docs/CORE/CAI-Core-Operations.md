# Cybersecurity Artificial Intelligence Framework (CAI) – Core Operations

**Version:** 0.1 (Revised Draft)  
**Author:** Antonio José Socorro Marín – Creator of CAI-EXPERT-LAB  

---

## Language Note

The normative language of CAI-EXPERT-LAB documentation is English.

---

## 1. Purpose and Scope

The purpose of this document is to define the operational semantics of the Cybersecurity Artificial Intelligence Framework (CAI).

While:

- CAI-Core-Definition establishes what CAI is  
- CAI-Core-Architecture defines how CAI is structured  

this document defines:

> how CAI operates across domains in a consistent, measurable, and implementation-agnostic manner

This document applies exclusively to the CAI Core and intentionally excludes:

- Sector-specific adaptations  
- Jurisdictional mappings  
- Vendor-specific tooling  
- Implementation code  

These elements are defined in separate CAI documents and extensions.

---

## 2. CAI Operational Behavior

CAI operational behavior can be implemented through a continuous, telemetry-driven lifecycle rather than a linear incident-response chain.

One primary operational model is:

MODEL → HARDEN → DETECT → ISOLATE → DECEIVE → EVICT → RESTORE

Key properties of this operational model include:

- Continuous execution  
- Feedback-driven improvement  
- AI-assisted prioritization  
- Safety- and policy-constrained actions  
- Metrics-first observability  

Each operational domain may operate:

- Concurrently  
- Asynchronously  
- Coordinated through control and orchestration mechanisms  

All operational domains operate under the governance of the **Decision Integrity Layer**, which evaluates:

- Decision State Awareness (DSA)  
- Environmental State Awareness (ESA)  

to ensure that:

> all actions remain valid under current conditions before execution

---

## 3. Operational Domain Specifications

Each CAI operational domain is defined using a uniform structure to ensure:

- Consistency  
- Auditability  
- Extensibility  

---

### 3.1 MODEL

#### Purpose
Establish authoritative knowledge of assets, data, dependencies, and exposure.

#### Core Responsibilities
- Asset and environment discovery  
- Classification of systems, data, and workflows  
- Dependency and trust relationship modeling  
- Baseline risk context generation  

#### Operational Activities
- Asset inventory and validation  
- Network and communication mapping  
- Data identification and classification  
- Service and dependency graph construction  

#### Inputs
- Discovery scans  
- Configuration inventories  
- Network topology data  
- Sector profile requirements (when applicable)  

#### Outputs
- Authoritative asset inventory  
- Dependency and trust graphs  
- Context tags for downstream domains  
- Baseline exposure metrics  

#### Operational Constraints
- Non-disruptive data collection  
- Accuracy prioritized over speed  
- Continuous reconciliation with observed telemetry  

---

### 3.2 HARDEN

#### Purpose
Reduce attack surface and enforce secure-by-design configurations.

#### Core Responsibilities
- Security baseline definition  
- Configuration and identity hardening  
- Policy enforcement preparation  
- Telemetry readiness enablement  

#### Operational Activities
- Baseline configuration assessment  
- Identity and access policy enforcement  
- Cryptographic and authentication control setup  
- Secure configuration drift detection  

#### Inputs
- Asset criticality and context from MODEL  
- Security standards and baselines  
- Engineering and policy constraints  

#### Outputs
- Hardened configurations and templates  
- Enforced identity and access controls  
- Drift alerts and remediation candidates  
- Telemetry configuration guidelines  

#### Operational Constraints
- Least privilege enforcement  
- Change control and rollback awareness  
- Compatibility with operational availability requirements  

---

### 3.3 DETECT

#### Purpose
Identify malicious, anomalous, or unsafe behavior with high fidelity.

#### Core Responsibilities
- Continuous telemetry analysis  
- Threat and anomaly detection  
- Confidence and severity scoring  
- Signal correlation across domains  

#### Operational Activities
- Behavioral and pattern analysis  
- Signature and heuristic detection  
- AI-assisted anomaly scoring  
- Alert enrichment and prioritization  

#### Inputs
- Telemetry from the Data Plane  
- Context from MODEL and HARDEN  
- AI-generated risk and anomaly scores  

#### Outputs
- Context-rich alerts  
- Confidence and risk indicators  
- Signals to ISOLATE, DECEIVE, and EVICT  
- Detection performance metrics  

#### Operational Constraints
- False-positive minimization  
- Explainability of AI-driven signals  
- Preservation of forensic evidence  

---

### 3.4 ISOLATE

#### Purpose
Contain threats and limit impact while preserving safety and availability.

#### Core Responsibilities
- Containment decision enforcement  
- Segmentation and access restriction  
- Blast-radius reduction  

#### Operational Activities
- Network and host isolation  
- Policy-driven access restriction  
- Quarantine of affected components  

#### Inputs
- High-confidence detection signals  
- Zero Trust and safety policies  
- Sector-specific constraints (when applicable)  

#### Outputs
- Isolation actions and status updates  
- Containment metrics  
- Context feedback to DETECT and EVICT  

#### Operational Constraints
- Safety and operational continuity  
- Policy-bound execution  
- Reversibility and auditability  

---

### 3.5 DECEIVE

#### Purpose
Increase adversary cost and detection fidelity through controlled deception.

#### Core Responsibilities
- Deployment of decoy assets and identities  
- Adversary interaction monitoring  
- High-confidence attacker confirmation  

#### Operational Activities
- Creation of decoy systems and credentials  
- Monitoring interaction with deceptive elements  
- Telemetry enrichment for attribution  

#### Inputs
- High-risk asset context  
- Threat behavior patterns  
- Detection confidence signals  

#### Outputs
- Deception telemetry  
- Confirmation signals for DETECT and EVICT  
- Intelligence artifacts  

#### Operational Constraints
- Non-interference with legitimate operations  
- Clear separation from production assets  
- Ethical and legal compliance  

---

### 3.6 EVICT

#### Purpose
Remove adversaries, persistence mechanisms, and unauthorized changes.

#### Core Responsibilities
- Termination of malicious access  
- Elimination of persistence  
- Neutralization of active threats  

#### Operational Activities
- Session termination  
- Credential revocation  
- Process and artifact removal  

#### Inputs
- Confirmed malicious entities  
- Isolation context  
- Legal and evidence-preservation requirements  

#### Outputs
- Eviction confirmation  
- Clean-up records  
- Post-action telemetry  

#### Operational Constraints
- Evidence preservation  
- Controlled sequencing  
- Policy and legal compliance  

---

### 3.7 RESTORE

#### Purpose
Return systems to a trusted operational baseline and validate recovery.

#### Core Responsibilities
- Recovery execution  
- Integrity validation  
- Lessons-learned feedback  

#### Operational Activities
- Restoration of configurations and images  
- Access re-enablement  
- Post-incident verification  

#### Inputs
- Approved baselines  
- Incident findings  
- Recovery policies  

#### Outputs
- Restored systems  
- Validation reports  
- Updated hardening and modeling inputs  

#### Operational Constraints
- Business continuity alignment  
- Verification before reintegration  
- Documentation for audit and compliance  

---

## 4. Cross-Domain Interaction Rules

- MODEL provides context to all domains  
- HARDEN influences DETECT fidelity  
- DETECT gates ISOLATE, DECEIVE, and EVICT  
- ISOLATE precedes EVICT unless policy allows otherwise  
- RESTORE feeds back into MODEL and HARDEN  

No operational domain functions in isolation.

---

## 5. Metrics, Telemetry, and Observability

Each domain must emit measurable outputs, including:

- Coverage  
- Accuracy  
- Latency  
- Effectiveness  

These metrics support:

- Maturity assessment  
- AI feedback loops  
- Compliance reporting  

---

## 6. Operational Constraints and Safety Hooks

CAI operations must respect:

- Safety constraints (especially ICS/OT environments)  
- Policy and governance requirements  
- Legal and regulatory conditions  

Automation must always be bounded by:

- Defined constraints  
- Human oversight thresholds  

---

## 7. Relationship to Architecture and Extensions

This document operationalizes CAI-Core-Architecture and provides the functional contract for:

- CAI extensions  
- CAI-USA mappings  
- CAI Engine implementations  

All extensions must preserve the semantics defined in this document.

---

## 8. Conclusion

This document defines the operational behavior of CAI as:

> a decision integrity-driven cybersecurity governance system in which all actions are continuously validated, context-aware, and governed under dynamic conditions
