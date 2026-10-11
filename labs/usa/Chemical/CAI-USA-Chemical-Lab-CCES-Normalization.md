Cybersecurity Artificial Intelligence Framework – USA Chemical Labs
CAI USA Chemical Lab – CCES Normalization and Evidence Integrity

Version 0.1 (Draft)
Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)
Copyright © 2025 Antonio José Socorro Marín.
All rights reserved.

Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

NOTE
The normative language of CAI-EXPERT-LAB documentation is English.
This laboratory artifact is non-normative and does not assert compliance, certification, accreditation, or regulatory approval.

Purpose

The purpose of this laboratory is to demonstrate, in a controlled and reproducible manner, how CCES-compliant telemetry normalization is performed within Chemical sector environments under the CAI USA framework.

This lab validates that telemetry originating from heterogeneous IT, OT, ICS, and CPS sources can be normalized into CCES without loss of safety context, process integrity, provenance, or evidentiary value, while remaining compatible with AI-assisted analysis governed by CAI non-autonomy principles.

This lab does not modify CAI CORE semantics, the CAI USA baseline, or the Chemical sector overlay. It exists solely to demonstrate execution fidelity.

Scope and Applicability

This lab applies to Chemical sector environments that include, but are not limited to:

Industrial control systems (DCS, PLCs, safety controllers)
Process monitoring sensors and analyzers
Manufacturing execution systems (MES)
Plant IT systems supporting operations, logistics, and safety
Telemetry pipelines feeding SIEM, SOAR, XDR, and analytics platforms

The lab assumes mixed-criticality environments where cybersecurity actions must not introduce unsafe process states, chemical release risk, or loss of operator authority.

CAI Lifecycle Alignment

This lab primarily supports the following CAI lifecycle stages:

MODEL
DETECT

Secondary support is provided to HARDEN through validation of telemetry integrity and to ISOLATE through evidence-ready observability.

No automated containment, eviction, or restoration actions are executed or simulated in this lab.

Laboratory Objectives

This laboratory demonstrates the ability to:

Establish authoritative telemetry sources across IT, OT, and ICS domains
Normalize telemetry into CCES while preserving process and safety semantics
Attach immutable provenance, timestamps, and source integrity metadata
Ensure telemetry is consumable by AI systems only as governed decision-support inputs
Produce evidence artifacts suitable for audit, investigation, and forensic reconstruction

Environment Assumptions

The laboratory environment assumes:

Chemical processes are continuous or semi-continuous
OT telemetry is safety-sensitive and must not be altered at source
Human authority over process control is absolute
AI systems operate in advisory mode only
All telemetry handling prioritizes integrity over volume or speed

No live production systems are modified during this lab.

Telemetry Domains Included

The lab explicitly covers telemetry from the following domains:

Process variables (temperature, pressure, flow, chemical concentration)
Controller state and mode transitions
Safety system alerts and interlocks
Authentication and access events for OT and plant IT
Configuration and firmware integrity signals
Network flow and protocol metadata relevant to ICS communications

Each domain is normalized independently and then correlated under CCES.

CCES Normalization Process

Telemetry is normalized according to CAI-USA-CCES principles:

Each event is assigned a unique CCES event identifier
Source system, asset identity, and trust domain are explicitly declared
Time synchronization and clock source are recorded
Process context and safety relevance flags are preserved
Transformation steps are logged and reproducible
No destructive aggregation or semantic compression is permitted

Normalization explicitly avoids converting process telemetry into abstract “security events” that would obscure operational meaning.

AI Governance Constraints

AI systems may consume normalized telemetry only under the following constraints:

AI outputs are advisory and non-authoritative
Confidence and uncertainty must be explicit
No autonomous action is permitted based on AI output
AI models must not modify telemetry or evidence artifacts
Model version, input set, and inference context are recorded

This lab validates governed AI consumption, not AI performance.

Evidence Artifacts Produced

Successful execution of this lab produces:

Raw telemetry samples (sanitized)
CCES-normalized event records
Transformation logs and hashes
Source provenance mappings
AI consumption records (read-only)
Validation checklist and acceptance sign-off

All artifacts are immutable once generated.

Acceptance Criteria

The lab is considered successful when:

All telemetry domains are normalized without semantic loss
CCES fields are complete and consistent
Evidence artifacts are traceable end-to-end
AI consumption is demonstrably non-autonomous
No safety or control pathways are altered

Failure of any criterion invalidates the lab run.

Relationship to Normative CAI Documents

This lab operates alongside, but does not modify:

CAI-Core-Definition.md
CAI-Core-Architecture.md
CAI-Core-Operational-State-Model.md
CAI-Core-Integrity-and-Self-Defense-Governance.md
CAI-USA-Definition.md
CAI-USA-CCES.md
CAI-USA-Chemical-Sector-Definition.md
CAI-USA-Chemical-Telemetry-and-Data-Model.md

If a conflict exists, the normative document is authoritative.

Non-Claims

This laboratory does not assert compliance with EPA, DHS, CISA, NIST, OSHA, or any other authority.
It does not certify systems, validate production deployments, or authorize operational changes.
It demonstrates cybersecurity execution fidelity only.

Status

Draft – CAI USA Chemical CCES normalization lab defined.

End of Document