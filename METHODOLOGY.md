# CAI-EXPERT-LAB — Methodology

This document unifies, in one place, the methodology of CAI-EXPERT-LAB: how the
framework is reasoned about, engineered, assured, and evolved, and the external
standards it aligns to. It consolidates what is defined across the CORE
documents (`docs/CORE/`) and states the engineering-assurance posture the
framework holds itself to.

> Author and owner: **Antonio José Socorro Marín** — Creator of CAI-EXPERT-LAB®.
> Copyright © 2025. Reference-Only Governance Framework License v1.0 (`LICENSE.md`, `/legal`).
> Alignment, not compliance: CAI-EXPERT-LAB maps to and strengthens external
> standards; it does not replace them and asserts no certification.

- **Last reviewed:** 2026-10-11
- **Companion documents:** `REGULATORY-BASIS.md`, `docs/CORE/CAI-Core-Definition.md`,
  `docs/CORE/CAI-Core-Execution-Model.md`,
  `docs/CORE/CAI-Core-Standards-Evolution-and-Governance.md`.

---

## 1. Methodological foundation — decision integrity

CAI is a **decision-centric** cybersecurity governance framework. Its central
claim is simple and strict:

> A decision is not assumed valid once issued; it must continuously prove its
> validity under changing conditions.

The method rests on:

- **Decision State Awareness (DSA)** — the state and validity of each decision
  is tracked explicitly.
- **Environmental State Awareness (ESA)** — decisions are evaluated against the
  real, current operating context.
- **Continuous validation at execution boundaries** — validation is continuous,
  not a one-time check or a periodic pentest.
- **Traceability** — every decision, transition and action is traceable.
- **Contamination control** — the framework protects its own semantic integrity
  against uncontrolled drift or misuse.

## 2. Principles (normative)

1. Continuous decision validation.
2. Zero Trust by default (identity, device and context continuously validated).
3. Defense in depth **plus decision assurance**.
4. AI as a first-class, **governed and auditable** component.
5. Sectorization — sector profiles where regulation or risk require it.
6. Measurability — every capability traces to an assurance objective or an
   external standard.
7. Responsible AI — explainability, bias control, drift monitoring, human
   oversight.
8. Framework integrity and contamination prevention.

## 3. Operational method — the seven-stage lifecycle

CAI is operationalized as an explicit, state-driven lifecycle. It is **one**
operational expression of the CAI core, not the definition of CAI itself.

```
MODEL → HARDEN → DETECT → ISOLATE → DECEIVE → EVICT → RESTORE
```

Execution is **state-driven, not checklist-driven**; continuous, not episodic;
and subordinate to governance and safety by design. Each stage is a valid state
with entry conditions, permitted actions, constraints and exit criteria; invalid
or unsafe transitions are prohibited; human authority is preserved for
high-impact actions; and no autonomous destructive action is permitted by
default. These semantics are defined in `CAI-Core-Execution-Model.md` and
enforced by the execution engine (`CAI-Engine/implementation/`).

## 4. Engineering and assurance rigor (NASA-aligned)

CAI holds its engineering and assurance process to the rigor model used for
mission- and safety-critical software. It aligns its assurance posture to NASA's
software engineering and assurance practice:

- **NASA Software Engineering & Software Assurance Handbook (SWEHB)** —
  engineering, assurance, IV&V and milestone governance
  (https://swehb.nasa.gov).
- **NPR 7150.2 — NASA Software Engineering Requirements** — lifecycle,
  requirements and verification discipline.
- **NASA-STD-8739.8 — Software Assurance and Software Safety** — independent
  assurance and safety requirements.
- **NASA/SP-2016-6105 — Systems Engineering Handbook** — systems-engineering
  lifecycle, verification and validation.

These map directly onto capabilities CAI already defines:

| CAI capability | NASA-rigor counterpart |
|---|---|
| Dual-Audit Pipeline (`CAI-Core-Dual-Audit-Pipeline.md`) | Independent Verification & Validation (IV&V) |
| Evolution Traceability Register | Requirements/decision traceability and milestone governance |
| Continuous validation at execution boundaries | Verification & validation discipline |
| Core Integrity & Self-Defense Governance | Configuration control and assurance of the baseline |
| Evidence generation (hash-chained, in the engine) | Objective, auditable assurance evidence |

The intent is explicit: **adopt the assurance discipline of a high-reliability
engineering organization**, expressed for cyber-AI governance.

## 5. Standards alignment

CAI aligns to, strengthens, and does **not** replace the following. The framework
provides a governance and execution-assurance layer on top of them.

| Domain | Standards CAI aligns to |
|---|---|
| Cybersecurity governance | **NIST** CSF 2.0; SP 800-53, 800-171, 800-171A; **CMMC** Level 2 |
| Zero Trust | **CISA** Zero Trust Maturity Model |
| Controls baselines | **CIS** Controls; **ISO/IEC 27001** |
| Threat modeling | **MITRE** ATT&CK |
| OT / ICS | **IEC 62443**; **Purdue** model |
| AI governance | **NIST AI RMF**, NIST AI 600-1 (USA); **EU AI Act** (EU) — see `REGULATORY-BASIS.md` |
| Engineering assurance | **NASA** SWEHB / NPR 7150.2 / NASA-STD-8739.8 / NASA/SP-2016-6105 |

CAI explicitly does not replace NIST SP 800-53, CMMC, PCI DSS, HIPAA or GDPR; it
operationalizes and strengthens the decisions derived from them.

## 6. Roles

- **CAI Architect** — designs architecture, mappings and sector profiles.
- **CAI Engineer** — implements capabilities, telemetry and automation.
- **CAI Assessor** — validates maturity, alignment, governance and effectiveness
  (the independent-assurance role, consistent with the IV&V posture above).

## 7. Evolution and review

The methodology and its standards alignment evolve under
`CAI-Core-Standards-Evolution-and-Governance.md`. Changes in external standards
do not silently alter execution behavior: they are reviewed, and any adopted
change is recorded in `CAI-Core-Evolution-Traceability-Register.md`, reflected in
`REGULATORY-BASIS.md`, and versioned. Core execution semantics remain stable
unless a new CAI Core version revises them.
