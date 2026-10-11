CAI-USA-ICS-OT-Safety-Gating
Cybersecurity Artificial Intelligence Framework – ICS/OT Safety Gating and Operational Constraints (USA)

Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2025 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

NOTE
The normative language of CAI-EXPERT-LAB documentation is English.
This document defines safety-aware operational constraints for CAI deployments in ICS and OT environments within the United States.
It does not assert regulatory approval, certification, or authorization to operate.

Purpose

The purpose of this document is to define mandatory safety gating, operational constraints, and escalation rules for CAI deployments operating in Industrial Control Systems (ICS) and Operational Technology (OT) environments.

This document ensures that CAI security actions do not compromise physical safety, operational continuity, or mission-critical processes, and that security automation is subordinate to safety requirements.

Scope

2.1 In Scope

This document applies to CAI deployments involving:
ICS and OT environments
Supervisory Control and Data Acquisition systems
Programmable Logic Controllers and Remote Terminal Units
Industrial networks and field devices
Firmware and embedded control systems
Hybrid IT/OT environments

2.2 Explicitly Out of Scope

This document does not:
Authorize automated shutdowns of industrial processes
Override vendor safety guidance
Replace industrial safety standards
Mandate specific ICS vendors or platforms

Governing Principles

CAI-USA ICS/OT safety gating is based on the following principles:
Safety takes precedence over security
No automation without operational context
Assume physical consequences
Least disruptive response
Human authority is mandatory for high-impact actions
Defense-in-depth without loss of control

ICS/OT Operational Context

ICS and OT environments differ from IT environments due to:
Real-time constraints
Physical process coupling
Safety and environmental impact
Legacy systems with limited security controls
Restricted maintenance windows

CAI explicitly distinguishes IT response logic from OT response logic.

Purdue Model Alignment

CAI aligns ICS/OT controls with the Purdue Enterprise Reference Architecture:

Level 0–1: Physical process and sensors
Level 2: Control systems and HMIs
Level 3: Site operations and control networks
Level 4–5: Enterprise IT and external connectivity

Security actions affecting Levels 0–3 are subject to enhanced safety gating.

Safety Gating by CAI Operational Stage

6.1 MODEL

CAI identifies and classifies:
ICS assets and roles
Safety-critical components
Process dependencies
Maintenance constraints
Vendor and regulatory limitations

No enforcement actions occur at this stage.

6.2 HARDEN

Allowed actions include:
Passive monitoring enablement
Configuration baseline assessment
Firmware integrity validation
Access control tightening with prior approval

Disallowed actions include:
Uncoordinated firmware updates
Unscheduled configuration changes

6.3 DETECT

CAI detection in OT focuses on:
Protocol anomalies
Behavioral deviations
Unauthorized access attempts
Integrity violations

Detection is non-intrusive and read-only by default.

6.4 ISOLATE

ISOLATE actions in OT are constrained:
Network segmentation may be applied only at approved boundaries
Isolation must not interrupt safety systems
Isolation actions require predefined approval thresholds

Automatic isolation is prohibited at Levels 0–2.

6.5 DECEIVE

Deception in OT is limited to:
Decoy assets outside production control paths
Non-interfering monitoring artifacts
Simulation-based deception environments

Live process deception is prohibited.

6.6 EVICT

EVICT actions are highly restricted:
Credential revocation may be permitted with human approval
Session termination requires safety validation
Removal of persistence mechanisms must not affect control logic

Automated eviction at control levels is prohibited.

6.7 RESTORE

RESTORE actions prioritize:
Safe state verification
Vendor-approved restoration procedures
Validated firmware and configuration images
Operational readiness confirmation

Restoration actions require coordination with operations personnel.

Human Escalation and Authority

ICS/OT environments require:
Explicit human approval for high-impact actions
Defined escalation paths to operations and safety teams
Clear authority boundaries between IT security and OT operations

CAI enforces human-in-command governance for OT actions.

Automation Boundaries

CAI automation in ICS/OT environments:
Is limited to advisory and low-risk actions
May not initiate shutdowns or resets
May not alter control logic autonomously
Must support immediate override

Incident Handling in OT Contexts

Security incidents involving OT systems require:
Joint security and operations response
Safety impact assessment
Preservation of forensic evidence
Controlled remediation planning

CAI treats OT incidents as combined cyber-physical events.

Relationship to Other CAI Documents

This document must be read together with:
CAI-Core-Definition
CAI-Core-Architecture
CAI-Core-Taxonomy
CAI-USA-Definition
CAI-USA-CISA-ZT-Map
CAI-USA-Secure-by-Design-Controls
CAI-USA-Operations-Playbooks

Author and Ownership

CAI-USA-ICS-OT-Safety-Gating is authored and owned by
Antonio José Socorro Marín.

This document is an intellectual property asset governed by the legal documents contained in the /legal directory.

End of Document