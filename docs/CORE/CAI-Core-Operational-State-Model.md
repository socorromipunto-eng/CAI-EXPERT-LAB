# CAI-Core-Operational-State-Model
Cybersecurity Artificial Intelligence Framework – Core Operational State Model
Version 0.1 (Draft)  

Author: Antonio José Socorro Marín  
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)  

Copyright © 2025 Antonio José Socorro Marín.  
All rights reserved.  
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.  

**NOTE**  
The normative language of CAI-EXPERT-LAB documentation is English.  
This document defines the formal operational behavior of CAI as a system-level state model intended to enable software implementation, orchestration, and controlled automation.  

## Purpose

The purpose of this document is to define the formal operational behavior of the Cybersecurity Artificial Intelligence Framework (CAI) as an executable state-based system.

This document transforms the CAI lifecycle from a conceptual and operational framework into a machine-interpretable behavioral model, suitable for implementation as software, orchestration engines, and AI-assisted decision systems.

This state model establishes:

- Formal operational states

- Valid and invalid transitions

- Event-driven behavior

- Decision gates and safety constraints

- Feedback and learning loops

- Degraded and recovery modes

This document is the authoritative bridge between CAI framework documentation and the CAI Engine.

## Design Principles

### 2.1 System-as-a-Network Principle

CAI is designed to behave as a distributed, interconnected system, analogous to a neural network of defensive subsystems.

Each CAI stage functions as:

- A specialized processing node

- With defined inputs, outputs, and feedback

- Operating continuously, not linearly

No CAI stage operates in isolation.

### 2.2 Continuous Feedback and Adaptation

All states emit telemetry and decision outcomes that feed:

- Other CAI states

- Policy engines

- AI analytics

- Human oversight mechanisms

### 2.3 Safety, Explainability, and Control

Automation is constrained by:

- Policy gates

- Safety gates

- Human-in-the-loop thresholds

- Sector and environment constraints

CAI never performs irreversible actions without explicit authorization when required.

## Core CAI Operational States

The seven-stage operational branch of CAI defines the following authoritative system states:

- MODEL

- HARDEN

- DETECT

- ISOLATE

- DECEIVE

- EVICT

- RESTORE

Each state represents a continuous operational mode, not a one-time action.

## State Definitions and Responsibilities

### 4.1 MODEL State

The MODEL state establishes system awareness.

Responsibilities:

- Asset, identity, data, firmware, and dependency discovery

- Topology and trust relationship modeling

- Criticality and impact classification

- Baseline context generation

Outputs:

- Authoritative inventories

- Dependency graphs

- Context metadata for all other states

MODEL continuously updates system understanding and feeds all downstream states.

### 4.2 HARDEN State

The HARDEN state reduces attack surface and enforces secure defaults.

Responsibilities:

- Baseline enforcement

- Configuration validation

- Secure-by-design control application

- Drift detection

Outputs:

- Hardened baselines

- Configuration alerts

- Enforcement signals to DETECT and ISOLATE

HARDEN operates continuously and reacts to MODEL updates and post-incident lessons.

### 4.3 DETECT State

The DETECT state identifies abnormal or malicious behavior.

Responsibilities:

- Telemetry analysis

- Anomaly detection

- Threat pattern recognition

- Confidence scoring

Inputs:

- CCES-normalized events

- Context from MODEL and HARDEN

- AI risk and anomaly scores

Outputs:

- Alerts with confidence levels

- Transition signals to ISOLATE, DECEIVE, or EVICT

- Feedback signals to MODEL and HARDEN

### 4.4 ISOLATE State

The ISOLATE state limits blast radius and preserves safety.

Responsibilities:

- Network segmentation

- Access restriction

- Quarantine enforcement

- Safety-aware containment

Constraints:

- OT/ICS safety gating

- Policy thresholds

- Human approval when required

Outputs:

- Isolation actions

Status telemetry  

- Signals to EVICT or DECEIVE

### 4.5 DECEIVE State

The DECEIVE state confirms adversary presence and intent.

Responsibilities:

- Deployment of decoy assets

- Controlled attacker engagement

- High-fidelity telemetry generation

Outputs:

- Confirmation signals

- Behavioral intelligence

- Evidence for EVICT decisions

DECEIVE operates without increasing operational risk.

### 4.6 EVICT State

The EVICT state removes adversaries and malicious artifacts.

Responsibilities:

- Session termination

- Credential revocation

- Malware and persistence removal

Constraints:

- Evidence preservation

- Legal and operational policy

- Safety gating

Outputs:

- Clean-up confirmation

- Lessons learned

- Signals to RESTORE and HARDEN

### 4.7 RESTORE State

The RESTORE state returns systems to trusted operation.

Responsibilities:

- Reimaging and reconfiguration

- Integrity validation

- Post-incident verification

Outputs:

- Restored operational status

- Updated baselines

- Feedback to MODEL and HARDEN

RESTORE completes the defensive loop and strengthens future posture.

## Events and Transitions

### 5.1 Event Model

All transitions are triggered by events, normalized through the CAI Common Event Schema (CCES).

Event categories include:

- Discovery events

- Configuration drift events

- Detection alerts

- Safety violations

- Policy decisions

- Human approvals

### 5.2 Valid Transitions

Examples:

- MODEL → HARDEN

- HARDEN → DETECT

- DETECT → ISOLATE

- DETECT → DECEIVE

- ISOLATE → EVICT

- EVICT → RESTORE

- RESTORE → MODEL

Transitions are non-linear and may occur concurrently.

### 5.3 Invalid Transitions

Examples:

- DETECT → EVICT without confirmation

- ISOLATE → EVICT in OT without safety approval

- HARDEN → EVICT (never allowed)

Invalid transitions are blocked by gates.

## Decision Gates

### 6.1 Policy Gates

Evaluate:

- Risk thresholds

- Compliance constraints

- Organizational rules

### 6.2 Safety Gates

Enforce:

- OT/ICS safety rules

- Physical impact prevention

- Fail-safe defaults

### 6.3 Human-in-the-Loop Gates

Require explicit authorization for:

- High-impact actions

- Irreversible changes

- Cross-boundary operations

- Degraded and Safe Modes

CAI supports degraded operation when:

- Telemetry is incomplete

- AI confidence is low

- System integrity is uncertain

In degraded mode:

- Automation is reduced

- Human oversight is increased

- Defensive posture favors safety

- Feedback and Learning Loops

All states emit feedback to:

- Update MODEL context

- Refine HARDEN baselines

- Improve DETECT accuracy

- Adjust policy thresholds

AI systems consume this feedback under governance defined in CAI-USA-AI-Governance-and-Assurance.

## Relationship to Other CAI Documents

This document must be read together with:

- CAI-Core-Definition

- CAI-Core-Architecture

- CAI-Core-Operations

- CAI-Core-Taxonomy

- CAI-USA-CCES

- CAI-USA-AI-Governance-and-Assurance

This document is authoritative for CAI Engine design.

## End of Document