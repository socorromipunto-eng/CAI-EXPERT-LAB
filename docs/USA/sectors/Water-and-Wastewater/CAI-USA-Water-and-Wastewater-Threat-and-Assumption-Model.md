Cybersecurity Artificial Intelligence Framework – USA Water and Wastewater Threat and Assumption Model
Version 0.1 (Draft)
Author: Antonio José Socorro Marín
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)

Copyright © 2025 Antonio José Socorro Marín.
All rights reserved.
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.

NOTE
The normative language of CAI-EXPERT-LAB documentation is English.
This document defines the authoritative threat boundaries and operational assumptions for the Water and Wastewater sector under the CAI USA framework.
This document does not assert compliance, certification, accreditation, or regulatory approval.

Purpose

The purpose of this document is to define the authoritative threat context, assumptions, and operational boundaries governing the application of the Cybersecurity Artificial Intelligence Framework within the Water and Wastewater sector.

This model establishes how threats are interpreted, prioritized, constrained, and operationalized across the CAI lifecycle while preserving public safety, environmental protection, operational continuity, accountability, and regulatory neutrality.

Scope

This document applies exclusively to the Water and Wastewater sector as defined in CAI-USA-Water-and-Wastewater-Sector-Definition.

It governs threat interpretation, assumed breach posture, containment philosophy, and response constraints without redefining CAI CORE semantics or CAI USA baseline requirements.

This document introduces no new controls and records no regulatory interpretations.

Foundational Assumptions

Water and Wastewater systems are public-safety–critical environments where availability, integrity, and predictability outweigh speed of response.

Human authority remains mandatory for any action affecting physical treatment processes, chemical dosing, pumping, distribution, or wastewater discharge.

Automation must be deterministic, observable, reversible, and auditable.

Cybersecurity actions must never introduce unsafe treatment states, uncontrolled service interruptions, environmental contamination, or cascading infrastructure failures.

Evidence generation and preservation are mandatory due to public accountability, legal scrutiny, and potential health impact investigations.

Threat Modeling Philosophy

Threat modeling in the Water and Wastewater sector is consequence-driven rather than frequency-driven.

Low-probability, high-impact events affecting water safety, environmental integrity, or population awareness are treated as first-order risks.

Assumed breach is handled conservatively, emphasizing containment, monitoring, safety preservation, and controlled escalation rather than aggressive eviction.

Threat novelty is secondary to systemic impact and recovery complexity.

Threat Categories

Threats considered within scope include, but are not limited to, disruption of water availability, manipulation of treatment or chemical dosing parameters, integrity compromise of sensor and telemetry data, unauthorized control of pumps or valves, degradation of situational awareness, supply-chain compromise of ICS components, insider misuse, and coordinated attacks designed to induce public panic or environmental harm.

Threats are evaluated based on potential public health impact, environmental consequences, operational recovery complexity, and cross-sector cascading effects.

Threat Boundaries

CAI does not assume direct control over physical process execution or safety-certified treatment mechanisms.

CAI operates within supporting IT, OT-adjacent, monitoring, analytics, and decision-support environments.

Any interaction with physical control domains is mediated through strict safety gating and explicit human authorization.

These boundaries are non-negotiable.

Relationship to CAI Lifecycle Stages

MODEL identifies assets, dependencies, physical process interfaces, data flows, trust relationships, and safety-relevant telemetry.

HARDEN prioritizes reduction of attack surface without introducing operational instability or process disruption.

DETECT emphasizes early anomaly identification with conservative confidence thresholds and explicit uncertainty representation.

ISOLATE is applied cautiously to prevent blast-radius expansion without interrupting essential services.

DECEIVE may be used only where it does not interfere with treatment processes or operational visibility.

EVICT is gated by safety approval, operational readiness, and evidence sufficiency.

RESTORE prioritizes validated baselines, controlled sequencing, and predictable recovery paths.

Assumptions About Adversaries

Adversaries may be patient, resourceful, and willing to remain dormant within long-lived infrastructure.

Supply-chain compromise is considered plausible due to extended vendor lifecycles.

Adversaries may target integrity and availability over data theft.

Attribution is not required for defensive action, but evidence preservation is mandatory.

Non-Assumptions

CAI does not assume perfect visibility.
CAI does not assume immediate remediation is always safe.
CAI does not assume automation is superior to human judgment.
CAI does not assume regulatory authority or operational control.

Relationship to Other CAI Documents

This document must be read together with CAI-USA-Water-and-Wastewater-Sector-Definition, CAI-USA-Threat-Model-Integration, CAI-USA-ICS-OT-Safety-Gating, CAI-USA-AI-Governance-and-Assurance, CAI-Core-Operational-State-Model, and CAI Engine safety and orchestration documents.

Status

Draft – USA Water and Wastewater threat and assumption model defined.
This document establishes the authoritative threat boundaries for Water and Wastewater sector operations under CAI USA.

End of Document