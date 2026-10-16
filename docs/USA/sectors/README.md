# CAI-USA Sector Profiles

## Cybersecurity Artificial Intelligence Framework – USA Sector Profiles

Version 0.1 (Draft)  
Author: Antonio José Socorro Marín  
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)  

Copyright © 2025 Antonio José Socorro Marín.  
All rights reserved.  
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.  

**NOTE**  
The normative language of CAI-EXPERT-LAB documentation is English.  
This directory defines sector-specific operational profiles for the United States and does not assert compliance, certification, accreditation, or regulatory approval.  

## Purpose

The purpose of the sectors directory is to host sector-specific operational profiles that extend the CAI-USA baseline into concrete, high-impact critical infrastructure and federal domains.

Each sector profile applies CAI consistently while respecting the unique risk, safety, mission, and operational constraints of that sector.

Sector profiles are not independent frameworks.  
They are constrained implementations of CAI.

## Scope

This directory contains one subdirectory per sector.

Each sector directory defines:

- Sector-specific threat models

- Mission and safety constraints

- OT / IT / cyber-physical considerations

- Sector-relevant telemetry sources

- AI usage boundaries and prohibitions

- Execution constraints enforced by the CAI Engine

- Traceability back to CAI CORE and CAI-USA

## Relationship to CAI CORE

All sector profiles are bound to CAI CORE artifacts, including but not limited to:

- CAI-Core-Definition

- CAI-Core-Architecture

- CAI-Core-Operations

- CAI-Core-Operational-State-Model

- CAI-Core-Taxonomy

- CAI-Core-Standards-Evolution-and-Governance

No sector profile may redefine CAI semantics, lifecycle stages, or governance principles.

## Relationship to CAI Engine

Sector profiles do not execute logic directly.

They define constraints, parameters, and conditions that are enforced by the CAI Engine, including:

- Safety gating thresholds

- Allowed and prohibited actions

- Human-in-the-loop requirements

- Automation ceilings

- Sector-specific state transition constraints

The CAI Engine remains authoritative for execution.

## Relationship to CAI-USA Baseline

Each sector profile is an extension of:

- CAI-USA-Definition

- CAI-USA-CCES

- CAI-USA-Telemetry-and-Data-Model

- CAI-USA-Secure-by-Design-Controls

- CAI-USA-AI-Governance-and-Assurance

- CAI-USA-ICS-OT-Safety-Gating (where applicable)

Sector profiles refine these documents; they do not replace them.

## Sector Development Methodology

Sector profiles are developed one at a time, using a scientific and auditable approach:

- Define sector scope and mission context

- Identify dominant threat classes and failure modes

- Define safety and non-negotiable constraints

- Map allowed CAI operational stages and transitions

- Define telemetry requirements and exclusions

- Define AI usage boundaries

- Bind execution rules to the CAI Engine

- Establish traceability to CAI CORE and CAI-USA

No sector is added until the previous one is complete and internally consistent.

## Initial Sector Strategy

Sector profiles are intentionally developed starting with the most complex and safety-critical domains, to stress-test CAI rigor, not to simplify it.

This approach maximizes credibility, resilience, and external defensibility.

## Sector Coverage

The CAI Engine (`CAI-Engine/implementation/cai_engine/usa_sectors.py`) defines the 16 critical infrastructure sectors of National Security Memorandum 22 (NSM-22). This directory holds sector profiles for 14 of them, plus one reference profile:

- Sectors with a profile: Chemical, Communications, Critical Manufacturing, Defense Industrial Base, Emergency Services, Energy, Financial Services, Food and Agriculture, Government (Government Facilities), Healthcare (Healthcare and Public Health), Information Technology, Nuclear (Nuclear Reactors, Materials, and Waste), Transportation Systems, Water and Wastewater (Water and Wastewater Systems).
- Sectors without a profile: Commercial Facilities and Dams. The engine applies the CAI-USA baseline and the NSM-22 sector parameters to them; no sector overlay exists.
- Reference profile: `aviation`. Aviation is not one of the 16 sectors; it is a subsector (mode) of the Transportation Systems Sector (CISA, https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors/transportation-systems-sector). It is kept as a separate reference profile, frozen as such by CAI-USA-Master-Freeze-v0.1.
- Folder name: the Communications sector profile is in the folder `Communication`. Its documents use the sector name Communications. The folder is not renamed because the sector profiles are frozen under CAI-USA-Master-Freeze-v0.1.

Adding the two missing profiles or renaming the folder requires a version increment of CAI USA under CAI-USA-Master-Freeze-v0.1.

The frameworks that apply to each sector, including Commercial Facilities and Dams, and the decision-time controls CAI adds to them are mapped in docs/USA/sector-frameworks.

## Extensibility and Evolution

New sectors may be added over time.

Sector updates are governed by:

- CAI-Core-Standards-Evolution-and-Governance

## CAI-USA-Standards-Lifecycle-and-Update-Control

Changes must preserve:

- Backward interpretability

- Safety guarantees

- Semantic consistency

- Audit traceability

Author and Ownership  

All sector profiles are authored and owned by:

- Antonio José Socorro Marín
- Creator of CAI-EXPERT-LAB

This directory is a foundational component of CAI’s operational credibility and sector applicability.

## End of Document