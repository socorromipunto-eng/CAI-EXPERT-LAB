Cybersecurity Artificial Intelligence Framework – Core Taxonomy
Version 0.1 (Draft)

Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2025 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

NOTE
The normative language of CAI-EXPERT-LAB documentation is English.
This taxonomy is normative for CAI, but regulatory-neutral.
It does not define compliance requirements, certification criteria, or regulatory obligations.

1. Purpose of the Taxonomy

The purpose of this document is to define the authoritative and normative vocabulary of the Cybersecurity Artificial Intelligence Framework (CAI).

This taxonomy establishes the precise meaning of terms used across all CAI Core, USA, EU, sector profiles, mappings, and implementations.

This taxonomy is intentionally regulatory-neutral.
It defines concepts, not obligations.
Alignment with external standards is conceptual only and does not imply conformity, certification, or regulatory satisfaction.

2. Conceptual Reference Frameworks (Non-Normative)

The CAI taxonomy is informed by widely recognized frameworks and standards for the purpose of terminology consistency and rigor, including:

NIST Cybersecurity Framework
NIST SP 800-series publications
NIST AI Risk Management Framework
CISA Zero Trust Maturity Model
ISO/IEC 15408 (Common Criteria – conceptual rigor only)
ISO/IEC 27000-series terminology (conceptual alignment)

These references do not impose requirements within CAI.

3. Taxonomy Rules

The following rules apply:

Defined terms are normative within CAI.
Capitalized terms indicate defined concepts.
Undefined terms MUST NOT be introduced.
Regional documents MUST NOT redefine CORE terms.
Sector Profiles may extend concepts without altering definitions.

4. Assets and Domains
4.1 Asset

An Asset is any identifiable element that has value to an organization and requires protection, monitoring, or governance.

Assets include physical, virtual, logical, and conceptual elements, including systems, data, firmware, software, networks, and AI components.

4.2 Asset Domain

An Asset Domain is a logical grouping of assets sharing common technical or operational characteristics.

Core CAI domains include:

IT Domain
OT / ICS Domain
Cloud Domain
Firmware and Embedded Domain
Middleware and Platform Domain
Network and Connectivity Domain
AI and Analytics Domain

5. Identity, Trust, and State
5.1 Identity

An Identity is a uniquely identifiable subject capable of performing actions or accessing assets.

Identities include human, service, machine, device, and workload identities.

5.2 Trust State

A Trust State represents the assessed level of confidence in an asset or identity at a given point in time.

Trust States are dynamic, telemetry-driven, and auditable.

6. Baseline, Configuration, and Integrity
6.1 Baseline

A Baseline is an approved reference state for configuration, behavior, or integrity.

6.2 Configuration Drift

Configuration Drift is any deviation from an approved baseline.

6.3 Integrity

Integrity is the assurance that an asset has not been altered in an unauthorized or unintended manner.

7. Telemetry, Evidence, and Observability
7.1 Telemetry

Telemetry is data emitted by systems that provides visibility into state, behavior, or events.

7.2 Evidence

Evidence is retained telemetry or artifacts supporting analysis, response, or assurance.

7.3 Observability

Observability is the ability to infer internal system states from telemetry.

8. Risk and Decision Concepts
8.1 Risk

Risk is the potential for loss or harm arising from the interaction of threats, vulnerabilities, and impact.

8.2 Risk Score

A Risk Score is a representation of assessed risk used to support decision-making.
Risk Scores MUST be explainable.

8.3 Decision Threshold

A Decision Threshold is a defined boundary at which an operational action may be triggered.

9. Firmware and Embedded Systems
9.1 Firmware

Firmware is executable code embedded in hardware components that provides low-level control and operation.

Firmware is treated as a first-class security asset.

9.2 Firmware Integrity State

A Firmware Integrity State represents whether firmware matches an approved baseline.

10. Middleware and Platforms

Middleware is software that enables communication, orchestration, or integration between components and services.

Middleware functions as a control and execution plane.

11. Network and Connectivity
11.1 Network

A Network is an interconnected system enabling communication between assets.

11.2 Segmentation

Segmentation is the separation of network domains to limit impact and lateral movement.

12. Artificial Intelligence and Analytics
12.1 AI Model

An AI Model is a computational system that produces outputs based on data-driven inference.

12.2 AI Lifecycle

The AI Lifecycle includes design, training, validation, deployment, operation, monitoring, and retirement.

12.3 AI Drift

AI Drift is degradation in model validity or performance over time.

12.4 Explainability

Explainability is the ability to understand and justify AI outputs.
Explainability is mandatory for security-relevant decisions.

13. Operational Actions

Detection
Isolation
Deception
Eviction
Restoration

These actions correspond to the CAI operational lifecycle and are defined in CAI-Core-Operations.

14. Assurance and Evaluation Concepts

CAI adopts assurance rigor concepts inspired by formal evaluation models such as Common Criteria, without claiming certification equivalence or Evaluation Assurance Levels.

15. Applicability

This taxonomy applies uniformly to:

CAI Core
CAI USA
CAI EU
Sector Profiles
Mappings and assessments

No regional document may redefine CORE taxonomy terms.

16. Author and Ownership

CAI-Core-Taxonomy is authored and owned by:

Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB – Cybersecurity Artificial Intelligence Framework

This document is a foundational intellectual property asset governed by the legal documents in the /legal directory.

End of Document