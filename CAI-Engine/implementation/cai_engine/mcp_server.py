"""CAI-Engine MCP server — exposes a local reference evaluator as MCP tools.

The server evaluates proposals submitted by an MCP client and records its
local decision. It does not execute actions, authenticate an approver, enforce
policy on other client interfaces, or prevent the client from using another
route. Do not connect this reference server to real systems or treat its tools
as an implemented security boundary. `EXECUTED` is the established name for a
completed local governance-decision path; it does not indicate that an external
actuator ran or that any external effect occurred.

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
    version="0.4.2",
    instructions=(
        "Research reference evaluator for CAI-EXPERT-LAB. It evaluates and records "
        "only proposals submitted to these MCP tools. It cannot execute or enforce "
        "actions outside this process, authenticate an approving person, or stop "
        "the client from using other tools or routes. EXECUTED means only that "
        "the local governance-decision path completed; no external effect occurred. "
        "Not an implemented security boundary and not for real systems."
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
    Returns the local decision (EXECUTED / BLOCKED / PENDING_APPROVAL) and
    trace data. EXECUTED records no external action or effect. Regulatory
    mappings are reference mappings, not validated compliance conclusions.
    """
    _ensure_init()
    return GovernedAgent(_engine).govern(proposal, jurisdiction=jurisdiction or None)


@server.tool()
def cai_verify() -> dict:
    """Verify the integrity of the hash-chained evidence log."""
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
