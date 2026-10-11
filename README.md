# CAI-EXPERT-LAB

**Cybersecurity Artificial Intelligence Framework** — a governance framework and
an executable **execution engine** for operating AI responsibly in cybersecurity,
including IT, OT/ICS, cloud and AI-enabled environments.

> Author and owner: **Antonio José Socorro Marín** — Creator of CAI-EXPERT-LAB®
> Copyright © 2025 Antonio José Socorro Marín. All rights reserved.
> Licensed under the **Reference-Only Governance Framework License v1.0** (see `LICENSE.md` and `/legal`).

CAI-EXPERT-LAB turns AI governance from a document into something that **runs,
enforces its own rules, and proves what it did** — under two jurisdictions
(EU AI Act and USA NSM-22 / NIST), treated per critical-infrastructure sector.

---

## The seven-stage operational lifecycle

The framework and engine execute CAI as an explicit, guarded state machine.
Only the transitions below are valid; every other transition is blocked.

```mermaid
stateDiagram-v2
    [*] --> MODEL
    MODEL   --> HARDEN
    HARDEN  --> DETECT
    DETECT  --> ISOLATE
    DETECT  --> DECEIVE
    ISOLATE --> EVICT
    DECEIVE --> EVICT
    EVICT   --> RESTORE
    RESTORE --> MODEL
```

Each state has entry conditions, permitted actions, telemetry requirements,
safety constraints and exit criteria. No state is ever inferred.

---

## What makes it different

- **Governance that executes.** Policy, safety and human-authority constraints
  are enforced by the engine, not just described in documents.
- **AI is advisory only.** Low-confidence or non-explainable AI output cannot
  trigger an action, and AI can never force a state transition or bypass a gate.
- **Human authority is final.** High-risk / critical-infrastructure decisions
  require explicit, attributed human approval.
- **Immutable evidence.** Every decision is written to a hash-chained,
  tamper-evident audit log.
- **Two jurisdictions, per sector.**
  - **EU** — EU AI Act (Regulation (EU) 2024/1689): risk tiers + article gates
    (Art. 5 / 9–15 / 50).
  - **USA** — NIST AI RMF, NIST AI 600-1 and the **NSM-22** critical-infrastructure
    sectors, each treated by its **SRMA** and consequence level, with OT/ICS
    safety gating.

> Alignment, not compliance: CAI-EXPERT-LAB maps to and enforces proportionate
> governance. It does not assert legal compliance, conformity assessment,
> certification or accreditation.

---

## Repository structure

```
docs/
  CORE/        definitions, lifecycle, state model, taxonomy, governance
  USA/         USA baseline + sectors/ (Energy, Nuclear, Healthcare, Financial, …)
  EU/          EU governance overlays and risk/proportionality model
  EXTERNAL/    white papers and foundational architecture
labs/          applied scenarios (Mexico, USA sectors, EU)
legal/         IP, ownership, commercial-use, attribution and confidentiality
CAI-Engine/              engine design documents
  implementation/        the executable engine (Python)
LICENSE.md     Reference-Only Governance Framework License v1.0
```

---

## The execution engine (quickstart)

The engine is in `CAI-Engine/implementation/`. The core is **pure Python
(3.9+), no dependencies**; only the optional MCP server needs `mcp`.

```bash
cd CAI-Engine/implementation
python -m cai_engine init
python -m cai_engine status

# Govern an AI proposal before it acts (EU jurisdiction)
python -m cai_engine govern examples/ai_highrisk_energy.json        # HIGH -> human oversight (Art. 14)
python -m cai_engine govern examples/ai_prohibited.json             # Art. 5 -> blocked

# USA, treated per NSM-22 sector
python -m cai_engine govern examples/usa_energy.json                # Energy / SRMA: DOE -> human oversight
python -m cai_engine govern examples/usa_energy_lowconf.json        # below assurance floor -> blocked

# Verify the immutable evidence chain
python -m cai_engine verify
```

It also runs as a **Model Context Protocol (MCP) server**, so an AI client
(e.g. Claude) must route its proposed actions through the governance runtime
before acting. See `CAI-Engine/implementation/README.md`.

---

## Status

Version 0.1 — the framework baseline (CORE / USA / EU, 16 NSM-22 sectors, labs)
with a working, tested execution engine. Standards evolve under
`docs/CORE/CAI-Core-Standards-Evolution-and-Governance.md`.

## Citation

> Socorro Marín, Antonio José. *CAI-EXPERT-LAB — Cybersecurity Artificial
> Intelligence Framework.* 2025. https://github.com/socorromipunto-eng/CAI-EXPERT-LAB

All permitted uses must clearly attribute authorship to
**Antonio José Socorro Marín — CAI-EXPERT-LAB**, as set out in `LICENSE.md`
and `/legal`.
