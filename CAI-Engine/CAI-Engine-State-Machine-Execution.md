# Cybersecurity Artificial Intelligence Framework – CAI Engine State Machine Execution

Version 0.1 (Draft)  

Author: Antonio José Socorro Marín  
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)  

Copyright © 2025 Antonio José Socorro Marín.  
All rights reserved.  
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.  

**NOTE**  
The normative language of CAI-EXPERT-LAB documentation is English.  
This document defines the executable state-machine behavior enforced by the CAI Execution Engine.  
It does not assert certification, accreditation, regulatory approval, or compliance.  

## 1. Purpose

The purpose of this document is to define how the CAI Execution Engine executes the CAI operational lifecycle as a strict state machine, including valid states, transitions, guards, and enforcement logic.

This document ensures that CAI execution is deterministic, auditable, safety-aware, and governance-constrained, preventing undefined behavior, shortcut execution, or unauthorized transitions.

## 2. Normative Authority

This document is normative with respect to:

- CAI-Core-Definition
- CAI-Core-Architecture
- CAI-Core-Operations
- CAI-Core-Operational-State-Model
- CAI-Core-Taxonomy
- CAI-Core-Standards-Evolution-and-Governance

And operationally constrained by:

- CAI-USA-Definition
- CAI-USA-Threat-Model-Integration
- CAI-USA-ICS-OT-Safety-Gating
- CAI-USA-AI-Governance-and-Assurance

Any execution behavior outside these authorities is invalid.

## 3. State Machine Principles

The CAI Engine state machine follows these principles:

- Explicit states only
- No implicit transitions
- Guarded entry and exit
- Safety-first execution
- Evidence generation by default
- Human oversight where required

The Engine never infers a state. States are entered only when conditions are satisfied.

## 4. Authoritative State Set

The CAI Engine recognizes the following authoritative states:

- MODEL
- HARDEN
- DETECT
- ISOLATE
- DECEIVE
- EVICT
- RESTORE

No additional operational states may be introduced without CORE modification.

## 5. State Entry Conditions

Each state has mandatory entry conditions.

MODEL  
Requires validated telemetry and asset discovery inputs.

HARDEN  
Requires completed MODEL state with asset and dependency context.

DETECT  
Requires hardened baseline and active telemetry streams.

ISOLATE  
Requires confirmed or high-confidence detection signals.

DECEIVE  
Requires threat presence confirmation and approved deception scope.

EVICT  
Requires confirmed malicious presence and safety approval.

RESTORE  
Requires eviction completion and validated clean baselines.

If entry conditions are not met, state transition is denied.

## 6. State Execution Constraints

During execution, each state enforces constraints.

MODEL  
No operational actions permitted.

HARDEN  
No disruptive changes without approval.

DETECT  
No containment or eradication actions permitted.

ISOLATE  
Limited to containment actions only.

DECEIVE  
Restricted to approved deception assets.

EVICT  
Subject to safety gates and human approval.

RESTORE  
Must follow validated recovery procedures.

State-specific constraints are non-configurable.

## 7. Valid State Transitions

The following transitions are valid:

- MODEL → HARDEN
- HARDEN → DETECT
- DETECT → ISOLATE
- DETECT → DECEIVE
- ISOLATE → EVICT
- DECEIVE → EVICT
- EVICT → RESTORE
- RESTORE → MODEL

All other transitions are invalid and blocked.

## 8. Guard Conditions and Enforcement

Before any transition:

- Policy Evaluation must approve permissibility.
- Safety Gates must approve impact and scope.
- Human approval must be obtained if required.

- Failure at any guard blocks transition.

## 9. Error Handling and Safe Failure

When execution errors occur:

- The Engine halts the current transition.
- The system remains in the last valid state.
- Safety gates are re-evaluated.
- Human escalation is triggered when required.

- There is no automatic rollback without authorization.

## 10. Evidence and Traceability

For each state transition, the Engine records:

- State entry and exit timestamps
- Guard evaluation outcomes
- Human approvals
- AI inference metadata
- Execution results

State history is immutable and auditable.

## 11. Interaction with AI

AI outputs:

- May influence prioritization and confidence scoring.
- May never force state transitions.
- Must meet explainability and confidence thresholds.

- AI is advisory only.

## 12. Versioning and Evolution

State-machine changes must:

- Preserve semantic meaning of states
- Maintain backward compatibility
- Be reviewed under governance

State evolution is conservative by design.

## 13. Author and Ownership

CAI Engine State Machine Execution is authored and owned by:

- Antonio José Socorro Marín
- Creator of CAI-EXPERT-LAB

This document defines the executable backbone of CAI and ensures disciplined, safe, and auditable operational behavior.

## End of Document