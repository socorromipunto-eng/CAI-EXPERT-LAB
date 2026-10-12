# CAI-Engine

An executable implementation of the **CAI-EXPERT-LAB execution engine** — the
operational layer of the Cybersecurity Artificial Intelligence Framework (CAI).

It turns the framework's documented design into a running, auditable program:
the seven-stage lifecycle as a strict **state machine**, with **policy
evaluation**, authoritative **safety gates**, **human oversight**, and an
**immutable hash-chained evidence log**.

> Framework author: **Antonio José Socorro Marín**, Creator of CAI-EXPERT-LAB.
> This program *implements* the documented design; it does not redefine it.

## Requirements

- **Python 3.9+** only. No third-party packages, no Node.js, no network access.

## The lifecycle (state machine)

```
MODEL → HARDEN → DETECT → ISOLATE ┐
                        → DECEIVE ┘→ EVICT → RESTORE → (back to MODEL)
```

Only these transitions are valid; every other transition is blocked. Each
target state has **entry conditions** that must be true before it can be
entered, and **execution constraints** that limit which action categories are
permitted while in it.

## Guard order (authority)

For every proposed action and every transition:

1. **Policy evaluation** — is this action permissible in the current state?
2. **Safety gates** (authoritative) — OT/ICS level, blast radius, AI
   confidence/explainability, operational impact. Safety gates override policy
   and automation.
3. **Human oversight** — mandatory approval for eviction, OT/ICS containment,
   privileged-account impact, destructive actions, and any escalated gate.

AI is **advisory only**: low-confidence or non-explainable AI output cannot
trigger any action, and AI can never force a state transition.

## Quick start

```
cd cai-engine
python -m cai_engine init
python -m cai_engine status
python -m cai_engine ingest examples/telemetry_good.json
python -m cai_engine ingest examples/telemetry_bad.json      # rejected (non-conformant)
python -m cai_engine propose examples/action_observe.json    # allowed in MODEL
python -m cai_engine propose examples/action_detect_bad.json # blocked by policy
```

Drive a transition (entry conditions enforced):

```
python -m cai_engine set assets_discovered true
python -m cai_engine set telemetry_validated true
python -m cai_engine transition HARDEN
```

Eviction requires human approval:

```
# ... advance to EVICT, then:
python -m cai_engine propose examples/action_evict.json      # -> PENDING_APPROVAL
python -m cai_engine approve <action_id> --by "A. Socorro"   # -> EXECUTED
```

Audit:

```
python -m cai_engine verify                 # checks the evidence hash chain
python -m cai_engine report --out report.md # Markdown execution/assurance report
```

## Governing an AI (EU AI Act + NIST AI RMF)

The point of the engine for AI: an AI system (an LLM, a model, an agent) never
acts directly. It submits a **proposal** — a recommended action plus its
confidence, explanation, provenance, drift indicator and deployment context —
and the engine governs it through two layers before anything happens:

1. **EU AI Act layer** (Regulation (EU) 2024/1689) — classifies the decision
   into a risk tier and applies the matching articles:
   - **Unacceptable** (Art. 5 prohibited practices) → **denied**.
   - **High** (Art. 6 + Annex III) → obligations Art. 9–15, **human oversight
     mandatory (Art. 14)**, accuracy/robustness threshold (Art. 15),
     transparency (Art. 13), record-keeping (Art. 12).
   - **Limited** (Art. 50) → transparency/disclosure duties.
   - **Minimal** → no specific obligation.
2. **CAI Engine layer** — state constraints, safety gates, human oversight.

The final decision is the **strictest of the two** (DENY wins, then ESCALATE to
human). AI is advisory only: it can never bypass a gate or force a transition,
and a high-risk decision always needs a human. Every governed decision is
written to the immutable evidence log with full traceability to **EU AI Act
articles** and **NIST AI RMF functions** (GOVERN / MAP / MEASURE / MANAGE).

> Alignment, not compliance: the engine maps to and enforces proportionate
> governance; it does not assert legal compliance, conformity assessment or CE
> marking — those are determined outside the engine.

```
python -m cai_engine init
python -m cai_engine govern examples/ai_minimal.json          # MINIMAL  -> executed
python -m cai_engine govern examples/ai_highrisk_energy.json  # HIGH     -> pending (Art. 14)
python -m cai_engine govern examples/ai_highrisk_lowconf.json # HIGH     -> blocked (Art. 15)
python -m cai_engine govern examples/ai_prohibited.json       # UNACCEPT.-> blocked (Art. 5)
```

### Jurisdictions: EU and USA

Each proposal carries a `jurisdiction` (or pass `--jurisdiction EU|USA`), and
the regulatory layer is selected accordingly:

- **EU** → EU AI Act risk tiers + article gates (above).
- **USA** → CAI-USA baseline: **NIST AI RMF**, **NIST AI 600-1** (generative AI),
  and the **NSM-22** critical-infrastructure sectors — treated **per sector**.

The USA profile treats each of the 16 NSM-22 sectors on its own terms. The
sector's **SRMA** (Sector Risk Management Agency) owns human oversight, the
**consequence** level sets the accuracy/assurance floor, and **OT-intensive**
sectors add cyber-physical safety gating:

| consequence | floor | sectors (examples) |
|-------------|------:|--------------------|
| CATASTROPHIC | 0.95 | Energy (DOE), Water (EPA), Chemical, Dams, Nuclear, Transportation |
| HIGH | 0.90 | Healthcare (HHS), Financial Services (Treasury), Communications, IT, Defense Industrial Base (DoD), Critical Manufacturing, Emergency Services, Food & Agriculture, Government Facilities |
| MODERATE | 0.80 | Commercial Facilities; non-critical uses floor 0.70 |

```
python -m cai_engine govern examples/usa_energy.json           # Energy/CATASTROPHIC -> pending (SRMA: DOE)
python -m cai_engine govern examples/usa_energy_lowconf.json   # conf 0.92 < 0.95    -> blocked
python -m cai_engine govern examples/usa_healthcare_genai.json # GenAI + HHS         -> pending (NIST AI 600-1)
python -m cai_engine govern examples/usa_corporate.json        # non-critical        -> executed
python -m cai_engine govern examples/ai_minimal.json --jurisdiction USA   # force USA
```

## Run it on AI (MCP server)

The engine can run as a **Model Context Protocol (MCP) server**, so an AI
client — Claude Desktop, or any MCP client — must route its proposed actions
through the governance runtime before acting. The AI calls `cai_govern`; the
engine returns EXECUTED, BLOCKED, or PENDING_APPROVAL and logs the decision.

Tools exposed: `cai_status`, `cai_govern`, `cai_verify`, `cai_report`.

The MCP server has **no approval tool**. The AI client is the party being
governed, so it cannot approve its own proposals. A `PENDING_APPROVAL` decision
is approved or denied only by a human at the local CLI
(`python -m cai_engine approve <id> --by "<name>"`).

The MCP server is the one component with a dependency (the core stays
dependency-free):

```
pip install "mcp>=2"
python -m cai_engine.mcp_server        # runs over stdio
```

Wire it into Claude Desktop — edit `claude_desktop_config.json`
(Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "cai-engine": {
      "command": "C:\\Users\\socor\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
      "args": ["-m", "cai_engine.mcp_server"],
      "cwd": "C:\\cai-engine",
      "env": { "CAI_HOME": "C:\\cai-engine\\cai_runtime" }
    }
  }
}
```

Restart Claude Desktop; the `cai_*` tools appear, and the AI's actions can be
governed before they run.

## Layout

```
cai_engine/
  core.py            states, transitions, entry conditions, actions, telemetry
  evidence.py        immutable hash-chained evidence log (+ integrity verify)
  gates.py           policy evaluation, safety gates, human-oversight rules
  engine.py          orchestrator (execution flow + persistence)
  eu_ai_act.py       EU AI Act (2024/1689) risk classification + article gates
  usa_sectors.py     NSM-22 critical-infrastructure sectors (SRMA, consequence)
  usa.py             USA profile: NIST AI RMF / AI 600-1 / per-sector gates
  nist_ai_rmf.py     NIST AI RMF function traceability
  governed_agent.py  the governed-AI layer (jurisdiction-aware: EU + USA)
  mcp_server.py      MCP server — exposes governance as tools for an AI client
  cli.py             command-line interface
examples/            sample telemetry, actions and AI proposals (EU + USA)
```

## Status

Version 0.1 — faithful first implementation of the documented engine. The
thresholds in `gates.py` (blast radius, AI confidence, OT levels) are
deliberately conservative and meant to be made configurable per deployment.
