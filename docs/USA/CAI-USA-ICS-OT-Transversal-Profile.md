Cybersecurity Artificial Intelligence Framework – USA ICS/OT Transversal Profile
Version 0.1 (Draft)
Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)
Copyright © 2025 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

NOTE
The normative language of CAI-EXPERT-LAB documentation is English.
This document defines a transversal ICS/OT profile under the CAI USA baseline. It does not assert compliance, certification, accreditation, or regulatory approval.

Purpose

The purpose of this document is to define a transversal Industrial Control Systems and Operational Technology (ICS/OT) profile under the CAI USA baseline.
This profile establishes shared assumptions, safety dominance principles, and inheritance rules applicable to all USA sectors that include or depend on ICS/OT environments.

This document exists to prevent sector fragmentation, ensure consistent safety treatment, and enable interoperable application of CAI across ICS/OT-dependent sectors.

Scope

This document applies to all CAI USA sector overlays that include ICS, OT, CPS, or safety-adjacent operational environments.
It is not a sector definition and does not replace sector-specific overlays.

This profile is inherited by, but not limited to, Aviation, Energy, Water and Wastewater, Manufacturing, Nuclear, Transportation Systems, and other critical infrastructure sectors with operational technology dependencies.

ICS/OT Foundational Assumptions

ICS/OT environments prioritize safety, determinism, and operational continuity over flexibility or rapid change.
Human authority is mandatory for actions that may affect physical processes or safety-adjacent systems.
Automation must be deterministic, observable, reversible, and explicitly bounded.
Operational changes are constrained by engineering approval, maintenance windows, and safety validation.
Cybersecurity actions must never introduce unsafe system states or ambiguous operational conditions.

Safety Dominance and Human Authority

Safety dominance is non-negotiable in all ICS/OT contexts under CAI USA.
Cybersecurity objectives must remain subordinate to physical safety and process integrity.

Human authority is required for high-impact actions, including isolation, eviction, shutdown, or restoration of ICS/OT assets.
AI-assisted decisions may inform and prioritize but must not autonomously execute safety-relevant actions.

Purdue Model Boundaries

ICS/OT environments are expected to follow logical segmentation consistent with the Purdue Enterprise Reference Architecture or equivalent models.

CAI operates primarily within higher Purdue levels and adjacent supporting environments.
Direct interaction with lower-level control systems is mediated through strict safety gates and explicit authorization.

This profile does not define certified control behavior or real-time process control logic.

Interaction with the CAI Lifecycle

MODEL focuses on identifying ICS/OT assets, dependencies, trust relationships, and safety-relevant data flows.
HARDEN emphasizes reduction of attack surface without destabilizing operational processes.
DETECT prioritizes high-confidence anomaly identification and integrity monitoring.
ISOLATE is applied conservatively to limit blast radius without disrupting safe operation.
DECEIVE is permitted only where it does not interfere with operational safety or control logic.
EVICT requires explicit safety approval and operational readiness.
RESTORE prioritizes validated baselines and predictable recovery paths.

Relationship to CAI CORE

This transversal profile inherits all semantics, lifecycle stages, and governance principles defined in CAI CORE.
It does not redefine CAI concepts, execution semantics, or integrity rules.

CAI CORE remains authoritative for taxonomy, execution model, integrity governance, and evolution control.

Relationship to CAI USA Baseline

This document complements, but does not replace, existing CAI USA baseline artifacts.
It operates in conjunction with CAI-USA-ICS-OT-Safety-Gating, CAI-USA-Telemetry-and-Data-Model, CAI-USA-AI-Governance-and-Assurance, and CAI-USA-Threat-Model-Integration.

Sector overlays may refine or constrain this profile but must not weaken its safety or governance assumptions.

Explicit Non-Claims

This document does not assert compliance with NERC CIP, ISA/IEC 62443, FAA, TSA, DHS, DoD, CISA, or NIST.
It does not certify systems, authorize operational changes, or replace regulatory or safety processes.

Status

Draft – USA ICS/OT transversal profile defined.
This document is authoritative for shared ICS/OT assumptions and inheritance under CAI USA.

End of Document