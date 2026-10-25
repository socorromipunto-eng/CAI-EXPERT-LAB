# Cybersecurity Artificial Intelligence Framework – United States Definition

> Candidate amendment CHG-CAI-RECON-2026-10-22-001; versioning and human adoption pending.
Version 0.1 (Draft)  

Author: Antonio José Socorro Marín  
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)  

Copyright © 2025 Antonio José Socorro Marín.  
All rights reserved.  
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.  

**NOTE**  
The normative language of CAI-EXPERT-LAB documentation is English.  
Spanish companion materials and explanatory documents may be produced separately and are non-normative unless explicitly stated.  

## 1. Purpose

This document defines the United States–specific operational definition of the Cybersecurity Artificial Intelligence Framework (CAI).

CAI-USA operationalizes the CAI Core framework within the technical, regulatory, safety, and assurance expectations of the United States, including federal, defense, critical infrastructure, and regulated commercial environments.

This document does not modify the CAI seven-stage lifecycle.  
It defines how the lifecycle is applied, constrained, and assured in the U.S. context.

## 2. Relationship to CAI Core

This document must be read in conjunction with:

- CAI-Core-Definition.md
- CAI-Core-Architecture.md
- CAI-Core-Operations.md

CAI-USA inherits the CAI lifecycle without modification:

- MODEL → HARDEN → DETECT → ISOLATE → DECEIVE → EVICT → RESTORE

All USA-specific requirements are implemented within this lifecycle.

## 3. USA Scope

### 3.1 Organizational Scope

CAI-USA applies to organizations operating within the United States, including:

- Federal agencies and departments
- State and local government entities
- Defense Industrial Base (DIB) organizations
- Critical infrastructure operators
- Regulated commercial enterprises
- Security engineering and security operations organizations

### 3.2 Technical Scope

CAI-USA applies across the full technology stack, including:

- Information Technology (IT) systems

Operational Technology (OT) and Industrial Control Systems (ICS)  
Cloud, hybrid, and multi-cloud architectures  
Embedded systems and firmware-bearing devices  
Middleware, platforms, and service orchestration layers  
Network and connectivity infrastructure  
Artificial intelligence and analytics systems

CAI-USA treats firmware, middleware, networks, and AI systems as first-class security domains.

## 4. USA Standards Alignment Baseline

CAI-USA is designed to align operationally with the following U.S. technical and regulatory baselines.

### 4.1 Core Cybersecurity and Compliance Standards

NIST Cybersecurity Framework (CSF) 2.0  
NIST SP 800-171  
NIST SP 800-171A / 171Ar3 (Assessment Methodology)  
NIST SP 800-53 (reference control baseline)  
CMMC Level 2 scoping, assessment, and operational expectations

### 4.2 Zero Trust and Secure Engineering

NIST SP 800-207 (Zero Trust Architecture)  
CISA Zero Trust Maturity Model  
CISA Secure-by-Design and Secure-by-Default principles

### 4.3 Industrial Control Systems and OT

NIST SP 800-82 (ICS Security)  
CISA / NCCIC Defense-in-Depth for ICS  
ICS Monitoring and Detection Technology Guidance

### 4.4 Configuration, Firmware, and Embedded Systems

NIST SP 800-70 (National Checklist Program)  
ICS Application Whitelisting Guidance  
Firmware integrity, secure update, and provenance principles

### 4.5 Artificial Intelligence Governance

NIST AI Risk Management Framework (AI RMF 1.0)  
NIST AI RMF Playbook  
Responsible AI lifecycle governance and assurance guidance

CAI integrates these standards operationally, not as checklists.

### 4.6 Access-Control Policy Verification References

These publications address access-control policies and models. They are
cross-cutting verification references, not ICS-specific design standards:

- NIST SP 800-192, *Verification and Test Methods for Access Control Policies/Models* (June 2017).
- NIST IR 8360, *Machine Learning for Access Control Policy Verification* (September 2021).
- NIST IR 8539, *Security Property Verification by Transition Model* (January 2025).

Official identification sources:

- https://csrc.nist.gov/pubs/sp/800/192/final
- https://csrc.nist.gov/pubs/ir/8360/final
- https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8539.pdf

Inclusion does not establish binding applicability, implementation or
conformance. Record exact sections, applicable requirements and evidence
separately. The identifiers are preserved; this amendment does not guess which
different ICS publication a previous description might have intended.

## 5. USA Operational Philosophy

CAI-USA is based on the following principles:

- Continuous defense over periodic assessment
- Telemetry-driven decision-making
- Safety-aware automation
- Zero Trust enforced at runtime
- AI-enabled but human-governed operations
- Measurable, auditable security outcomes

## 6. CAI-USA Domain-Specific Baselines

### 6.1 Firmware and Embedded Systems Security

Firmware and embedded components are treated as critical security assets.

#### 6.1.1 Scope

Applies to:

- BIOS, UEFI, BMC firmware
- Network device firmware
- OT and ICS devices (PLCs, RTUs, IEDs)
- Security appliances
- IoT and embedded platforms

#### 6.1.2 Minimum Expectations

Authoritative firmware inventories  
Approved firmware baselines  
Secure or measured boot where supported  
Verification of firmware provenance  
Controlled update and rollback procedures  
Prevention of unauthorized firmware modification

#### 6.1.3 Telemetry and Evidence

Firmware version and integrity state  
Boot measurements where available  
Firmware update logs  
Alerts on unauthorized changes

#### 6.1.4 Safety Constraints

Automated firmware actions must be policy-bound.  
ICS firmware actions must respect safety and vendor constraints.

#### 6.1.5 Metrics

Firmware inventory coverage  
Baseline compliance rate  
Time to detect unauthorized firmware changes  
Time to restore trusted firmware state

### 6.2 Middleware and Platform Security

Middleware is treated as a control plane and execution layer.

#### 6.2.1 Scope

Application servers and runtimes  
API gateways and service meshes  
Message brokers and streaming platforms  
Authentication, authorization, and token services  
CI/CD execution environments

#### 6.2.2 Minimum Expectations

Authoritative middleware inventories  
Hardened configuration baselines  
Secure service-to-service authentication  
Secret and credential lifecycle management  
Dependency awareness and supply chain controls

#### 6.2.3 Telemetry

Authentication and authorization events  
Service invocation and API logs  
Configuration changes  
Runtime and dependency loading events

#### 6.2.4 Safety Constraints

Availability must be preserved.  
Isolation actions must be staged when required.

#### 6.2.5 Metrics

Middleware coverage  
Baseline drift detection  
Anomalous behavior detection rate  
Restoration time to baseline

### 6.3 Network and Connectivity Security

Networks are continuous enforcement and observability planes.

#### 6.3.1 Scope

Enterprise and data center networks  
Cloud virtual networks  
Remote access infrastructure  
OT and ICS networks  
DNS and routing systems  
Wireless environments

#### 6.3.2 Minimum Expectations

Authoritative network inventories  
Defined segmentation and trust boundaries  
Policy-based access enforcement  
Controls against lateral movement  
DNS and routing integrity protections

#### 6.3.3 Telemetry

Network flow metadata  
DNS logs  
Access and authentication events  
Routing and configuration changes

#### 6.3.4 Safety Constraints

OT network actions must be safety-aware.  
Automated isolation must be reversible.

#### 6.3.5 Metrics

Telemetry coverage  
Time to detect lateral movement  
Time to isolate affected segments  
Time to restore trusted connectivity

### 6.4 Artificial Intelligence and Analytics Governance

AI is a cross-cutting, governed capability.

#### 6.4.1 Scope

Detection and anomaly models  
Risk scoring and prioritization engines  
Inference services  
Feedback and retraining pipelines

#### 6.4.2 Minimum Expectations

Defined purpose and scope per model  
Documented data sources and features  
Model versioning and lifecycle controls  
Human oversight thresholds  
Bounded automated actions

#### 6.4.3 Telemetry and Evidence

Model inputs and outputs  
Confidence and risk scores  
Explainability artifacts  
Drift and bias monitoring  
Human override records

#### 6.4.4 Safety Constraints

Unsafe actions require human approval.  
Fallback mechanisms must exist.  
Models must be continuously monitored.

#### 6.4.5 Metrics

Explainability coverage  
Drift detection frequency  
Accuracy and precision trends  
Human intervention rates

## 7. CAI-USA Lifecycle Interpretation

MODEL includes full asset, firmware, middleware, network, and AI inventories.  
HARDEN enforces secure-by-design baselines across all layers.  
DETECT correlates telemetry across domains.  
ISOLATE limits blast radius with safety constraints.  
DECEIVE increases detection confidence and adversary cost.  
EVICT removes persistence and unauthorized access.  
RESTORE returns systems to validated trusted states.

## 8. Sector Profiles

Sector Profiles are mandatory where safety, availability, or regulation applies.

ICS/OT profiles include:

- Purdue model segmentation
- OT protocol awareness
- Firmware whitelisting
- Safety-aware isolation
- Vendor-validated restoration

Sector Profiles extend CAI without altering core semantics.

## 9. Roles

CAI Architect  
Designs architecture, mappings, and sector profiles.

CAI Engineer  
Implements telemetry, controls, and automation.

CAI Assessor  
Validates maturity, alignment, and effectiveness.

## 10. Relationship to Other CAI Documents

This document is complemented by:

- CAI-USA-NIST-Map.md
- CAI-USA-CMMC-Map.md
- Sector Profiles under docs/USA
- Legal documents under /legal

## 11. Author and Ownership

CAI-EXPERT-LAB is authored and owned by:

- Antonio José Socorro Marín

Creator of CAI-EXPERT-LAB – Cybersecurity Artificial Intelligence Framework  

All intellectual property, architecture, lifecycle semantics, and documentation are protected under applicable law and governed by the legal documents in the /legal directory.

## End of Document