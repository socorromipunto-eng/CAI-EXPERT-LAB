"""CAI-Engine MCP server — exposes the governance runtime as MCP tools.

This lets an AI client (Claude Desktop, or any Model Context Protocol client)
submit its proposed actions to the engine BEFORE acting. The AI does not act
directly: it calls `cai_govern`, and the engine governs the proposal under the
selected jurisdiction (EU AI Act or USA / NSM-22 + NIST), returning
EXECUTED, BLOCKED, or PENDING_APPROVAL (human oversight). Every decision is
written to the immutable, hash-chained evidence log.

Human approval is deliberately NOT exposed here. The AI client is the party
being governed, so it must never be able to approve its own proposals.
Approvals and denials are recorded only by a human at the local CLI:
    python -m cai_engine approve <decision_id> --by "<human name>"
    python -m cai_engine deny <decision_id> --by "<human name>" --reason "..."

Requires the MCP SDK (separate from the dependency-free core):
    pip install "mcp>=2"

Run it directly:
    python -m cai_engine.mcp_server
or point an MCP client's command at that module (see README).
"""
from __future__ import annotations

import os

from mcp.server.mcpserver import MCPServer

from .engine import CAIEngine, EngineError
from .governed_agent import GovernedAgent

HOME = os.environ.get("CAI_HOME", "cai_runtime")
_engine = CAIEngine(home=HOME)

server = MCPServer(
    "cai-engine",
    version="0.4.1",
    instructions=(
        "Governance runtime for AI actions (CAI-EXPERT-LAB). Before acting, an "
        "AI must submit its proposal to cai_govern; the engine governs it under "
        "EU AI Act or USA (NSM-22 / NIST AI RMF) jurisdiction and returns "
        "EXECUTED, BLOCKED, or PENDING_APPROVAL. AI output is advisory only; "
        "high-risk / critical-infrastructure decisions require human approval, "
        "which only a human can record through the local CLI; this server cannot approve."
    ),
)


def _ensure_init() -> None:
    try:
        _engine.status()
    except EngineError:
        _engine.init()


@server.tool()
def cai_status() -> dict:
    """Current CAI state, allowed transitions, context facts and evidence count."""
    _ensure_init()
    return _engine.status()


@server.tool()
def cai_govern(proposal: dict, jurisdiction: str = "") -> dict:
    """Govern an AI proposal before it acts.

    proposal: {
      "ai": {"system","model_version","confidence","explanation","explainable",
             "provenance","drift_score","genai","human_disclosed"},
      "context": {"sector","safety_component","biometric",
                  "affects_essential_services","prohibited_practice",...},
      "action": {"category","description","target","ot_level","destructive",...},
      "jurisdiction": "EU" | "USA"   (optional; can be overridden by the argument)
    }
    Returns the governed decision (EXECUTED / BLOCKED / PENDING_APPROVAL) with
    full EU/USA regulatory traceability and NIST AI RMF mapping.
    """
    _ensure_init()
    return GovernedAgent(_engine).govern(proposal, jurisdiction=jurisdiction or None)


@server.tool()
def cai_verify() -> dict:
    """Verify the integrity of the immutable, hash-chained evidence log."""
    _ensure_init()
    return _engine.verify()


@server.tool()
def cai_report() -> str:
    """A Markdown execution/assurance report of all governed decisions and transitions."""
    _ensure_init()
    return _engine.report()


def main() -> None:
    _ensure_init()
    server.run("stdio")


if __name__ == "__main__":
    main()
