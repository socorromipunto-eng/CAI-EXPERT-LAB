"""Test suite for the CAI-Engine.

Covers the state machine, telemetry validation, policy and safety gates, the
hash-chained evidence log (including tamper detection), and the governed-agent
layer under both jurisdictions (EU AI Act and USA / NSM-22).

Run:  pytest -q      (from CAI-Engine/implementation)
"""
from __future__ import annotations

import pytest

from cai_engine.core import State, TelemetryEvent
from cai_engine.engine import CAIEngine, EngineError
from cai_engine.governed_agent import GovernedAgent


@pytest.fixture
def engine(tmp_path):
    eng = CAIEngine(home=str(tmp_path / "rt"))
    eng.init()
    return eng


# --------------------------------------------------------------------------
# State machine
# --------------------------------------------------------------------------
def test_initial_state_is_model(engine):
    assert engine.status()["current_state"] == State.MODEL.value


def test_invalid_transition_blocked(engine):
    # MODEL -> DETECT is not a valid transition
    out = engine.transition("DETECT")
    assert out["status"] == "BLOCKED"


def test_transition_blocked_on_unmet_entry_conditions(engine):
    out = engine.transition("HARDEN")  # needs assets_discovered + telemetry_validated
    assert out["status"] == "BLOCKED"
    assert "assets_discovered" in out["unmet_entry_conditions"]


def test_valid_transition_with_entry_conditions(engine):
    engine.set_fact("assets_discovered", True)
    engine.set_fact("telemetry_validated", True)
    out = engine.transition("HARDEN")
    assert out["status"] == "OK"
    assert engine.status()["current_state"] == "HARDEN"


def test_full_lifecycle_to_evict(engine):
    for k in ("assets_discovered", "telemetry_validated", "baseline_hardened",
              "telemetry_active", "detection_confirmed",
              "malicious_presence_confirmed", "safety_approved"):
        engine.set_fact(k, True)
    assert engine.transition("HARDEN")["status"] == "OK"
    assert engine.transition("DETECT")["status"] == "OK"
    assert engine.transition("ISOLATE")["status"] == "OK"
    assert engine.transition("EVICT")["status"] == "OK"
    # EVICT -> DETECT is invalid
    assert engine.transition("DETECT")["status"] == "BLOCKED"


# --------------------------------------------------------------------------
# Telemetry validation
# --------------------------------------------------------------------------
def test_good_telemetry_accepted(engine):
    out = engine.ingest({"source": "edr", "domain": "device", "confidence": 0.9,
                         "provenance": "p", "timestamp": 1.0})
    assert out["accepted"] is True


def test_bad_telemetry_rejected(engine):
    out = engine.ingest({"source": "", "domain": "weather", "confidence": 2.0,
                         "provenance": "", "timestamp": None})
    assert out["accepted"] is False
    assert len(out["errors"]) >= 3


def test_telemetry_validate_unit():
    ev = TelemetryEvent(source="s", domain="network", confidence=0.5,
                        provenance="x", timestamp=1.0)
    assert ev.validate() == []


# --------------------------------------------------------------------------
# Policy + safety gates
# --------------------------------------------------------------------------
def test_policy_blocks_eradication_in_model(engine):
    out = engine.propose({"category": "ERADICATION", "description": "x", "destructive": True})
    assert out["status"] == "BLOCKED"


def test_observe_allowed_in_model(engine):
    out = engine.propose({"category": "OBSERVE", "description": "discovery"})
    assert out["status"] == "EXECUTED"


def test_low_confidence_ai_denied(engine):
    out = engine.propose({"category": "OBSERVE", "description": "x",
                          "ai_assisted": True, "ai_confidence": 0.5})
    assert out["status"] == "BLOCKED"


# --------------------------------------------------------------------------
# Evidence chain
# --------------------------------------------------------------------------
def test_evidence_chain_verifies(engine):
    engine.propose({"category": "OBSERVE", "description": "x"})
    assert engine.verify()["integrity_ok"] is True


def test_evidence_tamper_detected(engine):
    engine.propose({"category": "OBSERVE", "description": "x"})
    import json
    path = engine.evidence.path
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    rec = json.loads(lines[-1])
    rec["payload"]["tampered"] = True
    lines[-1] = json.dumps(rec, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    assert engine.verify()["integrity_ok"] is False


# --------------------------------------------------------------------------
# Governed agent — EU jurisdiction
# --------------------------------------------------------------------------
def _ga(engine):
    return GovernedAgent(engine)


def test_eu_minimal_executed(engine):
    p = {"ai": {"confidence": 0.9, "explanation": "ok", "explainable": True},
         "context": {"sector": "corporate_it"},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "EU"}
    out = _ga(engine).govern(p)
    assert out["regulatory"]["label"] == "MINIMAL"
    assert out["status"] == "EXECUTED"


def test_eu_high_risk_requires_human(engine):
    p = {"ai": {"confidence": 0.95, "explanation": "ok", "explainable": True, "human_disclosed": True},
         "context": {"sector": "energy", "safety_component": True},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "EU"}
    out = _ga(engine).govern(p)
    assert out["regulatory"]["label"] == "HIGH"
    assert out["status"] == "PENDING_APPROVAL"
    assert out["requires_human_approval"] is True


def test_eu_prohibited_blocked(engine):
    p = {"ai": {"confidence": 0.99, "explanation": "x", "explainable": True},
         "context": {"prohibited_practice": True, "prohibited_reason": "social scoring"},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "EU"}
    out = _ga(engine).govern(p)
    assert out["regulatory"]["label"] == "UNACCEPTABLE"
    assert out["status"] == "BLOCKED"


def test_eu_high_risk_lowconf_blocked(engine):
    p = {"ai": {"confidence": 0.71, "explanation": "x", "explainable": True},
         "context": {"sector": "energy", "safety_component": True},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "EU"}
    out = _ga(engine).govern(p)
    assert out["status"] == "BLOCKED"


# --------------------------------------------------------------------------
# Governed agent — USA jurisdiction (per sector)
# --------------------------------------------------------------------------
def test_usa_energy_catastrophic_requires_human(engine):
    p = {"ai": {"confidence": 0.96, "explanation": "ok", "explainable": True,
                "provenance": "p", "drift_score": 0.03},
         "context": {"sector": "energy", "safety_component": True},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "USA"}
    out = _ga(engine).govern(p)
    assert out["regulatory"]["sector"] == "Energy"
    assert out["regulatory"]["srma"] == "Department of Energy"
    assert out["regulatory"]["consequence"] == "CATASTROPHIC"
    assert out["status"] == "PENDING_APPROVAL"


def test_usa_energy_below_floor_blocked(engine):
    p = {"ai": {"confidence": 0.92, "explanation": "x", "explainable": True,
                "provenance": "p", "drift_score": 0.03},
         "context": {"sector": "energy", "safety_component": True},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "USA"}
    out = _ga(engine).govern(p)
    assert out["status"] == "BLOCKED"  # 0.92 < 0.95 catastrophic floor


def test_usa_noncritical_executed(engine):
    p = {"ai": {"confidence": 0.85, "explanation": "ok", "explainable": True,
                "provenance": "p", "drift_score": 0.02},
         "context": {"sector": "corporate_it"},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "USA"}
    out = _ga(engine).govern(p)
    assert out["regulatory"]["label"] == "NON_CRITICAL"
    assert out["status"] == "EXECUTED"


def test_jurisdiction_override(engine):
    p = {"ai": {"confidence": 0.9, "explanation": "ok", "explainable": True},
         "context": {"sector": "corporate_it"},
         "action": {"category": "OBSERVE", "description": "x"}}
    out = _ga(engine).govern(p, jurisdiction="USA")
    assert out["regulatory"]["jurisdiction"] == "USA"


# --------------------------------------------------------------------------
# Human approval flow
# --------------------------------------------------------------------------
def test_human_approval_executes_pending(engine):
    p = {"ai": {"confidence": 0.96, "explanation": "ok", "explainable": True,
                "provenance": "p", "drift_score": 0.03},
         "context": {"sector": "energy", "safety_component": True},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "USA"}
    out = _ga(engine).govern(p)
    aid = out["action_id"]
    res = engine.approve(aid, "Antonio Socorro")
    assert res["status"] == "EXECUTED"
    assert res["approved_by"] == "Antonio Socorro"


def test_approve_requires_approver(engine):
    p = {"ai": {"confidence": 0.96, "explanation": "ok", "explainable": True,
                "provenance": "p", "drift_score": 0.03},
         "context": {"sector": "energy", "safety_component": True},
         "action": {"category": "OBSERVE", "description": "x"}, "jurisdiction": "USA"}
    out = _ga(engine).govern(p)
    with pytest.raises(EngineError):
        engine.approve(out["action_id"], "")


# --------------------------------------------------------------------------
# MCP boundary: the governed AI must not be able to approve its own actions
# (audit finding ENG-01). Checked statically so the test needs no MCP SDK.
# --------------------------------------------------------------------------
def test_mcp_server_exposes_no_approval_tool():
    import ast
    import pathlib

    src = pathlib.Path(__file__).resolve().parent.parent / "cai_engine" / "mcp_server.py"
    tree = ast.parse(src.read_text(encoding="utf-8"))
    tools = [
        node.name for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and any("tool" in ast.unparse(d) for d in node.decorator_list)
    ]
    assert tools, "no MCP tools found; the check would be meaningless"
    assert not any("approve" in t or "deny" in t for t in tools), tools


# --------------------------------------------------------------------------
# Packaging: the declared package version must match the code version.
# --------------------------------------------------------------------------
def test_pyproject_version_matches_package():
    import pathlib
    import re

    import cai_engine

    root = pathlib.Path(__file__).resolve().parent.parent
    text = (root / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version = "([^"]+)"', text, re.MULTILINE)
    assert m, "no version in pyproject.toml"
    assert m.group(1) == cai_engine.__version__
