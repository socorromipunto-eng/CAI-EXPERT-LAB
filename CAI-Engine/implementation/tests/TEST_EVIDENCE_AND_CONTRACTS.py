"""Evidence and interface contracts for the CAI-Engine reference implementation.

Part of CAI-EXPERT-LAB (owner: Antonio José Socorro Marín).

Purpose
    TEST_SPECIFICATION_MATRIX.py checks WHAT the engine decides. This module
    checks WHAT THE ENGINE RECORDS AND RETURNS, because an audit trail is only
    useful if its content is exact and stable:

      * the evidence record schema, sequence numbers, hash links and event names;
      * the stable gate names and the article / threshold references in reasons;
      * the regulatory blocks (EU and USA) attached to every governed decision;
      * the NIST AI RMF trace;
      * the return values of every engine operation;
      * defaults applied when an AI proposal omits a field.

    These tests were added after automatic mutation testing (mutmut 3.8, engine
    0.4.2, commit b52935e) showed that most surviving mutants changed record
    content, gate names or defaults without changing the final decision.

Run (from CAI-Engine/implementation):  python -m pytest -q tests/TEST_EVIDENCE_AND_CONTRACTS.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from cai_engine import eu_ai_act, usa
from cai_engine.core import Action, ActionCategory, State
from cai_engine.engine import CAIEngine, EngineError
from cai_engine.evidence import GENESIS_HASH, EvidenceLog, _record_hash
from cai_engine.gates import Decision, policy_evaluate, safety_gates
from cai_engine.governed_agent import GovernedAgent
from cai_engine.nist_ai_rmf import rmf_trace

C = ActionCategory
RECORD_KEYS = {"seq", "timestamp", "event_type", "prev_hash", "payload", "record_hash"}
ALL_FACTS = ("assets_discovered", "telemetry_validated", "baseline_hardened", "telemetry_active",
             "detection_confirmed", "deception_scope_approved", "malicious_presence_confirmed",
             "safety_approved", "eviction_completed", "clean_baseline_validated")


@pytest.fixture
def engine(tmp_path):
    eng = CAIEngine(home=str(tmp_path / "rt"))
    eng.init()
    return eng


def records(eng: CAIEngine) -> list[dict]:
    return list(eng.evidence.records())


def last(eng: CAIEngine) -> dict:
    return records(eng)[-1]


def to_state(eng: CAIEngine, *path: str) -> None:
    for f in ALL_FACTS:
        eng.set_fact(f, True)
    for s in path:
        assert eng.transition(s)["status"] == "OK"


def gp(*, juris="EU", conf=0.95, sector="", category="OBSERVE", **ctx) -> dict:
    return {"jurisdiction": juris,
            "ai": {"system": "soc-llm", "model_version": "2.1", "confidence": conf, "explanation": "why",
                   "explainable": True, "provenance": "cces://x", "drift_score": 0.03, "human_disclosed": True},
            "context": {"sector": sector, **ctx},
            "action": {"category": category, "description": "d", "target": "t"}}


# ==========================================================================
# 1. Evidence record schema and chain
# ==========================================================================
def _busy(eng: CAIEngine) -> None:
    eng.set_fact("assets_discovered", True)
    eng.ingest({"source": "edr", "domain": "device", "confidence": 0.9, "provenance": "p", "timestamp": 1.0})
    eng.ingest({"source": "", "domain": "weather", "confidence": 2, "provenance": "", "timestamp": None})
    eng.transition("DETECT")
    eng.propose({"category": "OBSERVE", "description": "look", "target": "h"})
    eng.propose({"category": "ERADICATION", "description": "wipe", "target": "h"})
    GovernedAgent(eng).govern(gp())


def test_every_record_has_exactly_the_documented_fields(engine):
    _busy(engine)
    for rec in records(engine):
        assert set(rec) == RECORD_KEYS, rec


def test_sequence_numbers_are_contiguous_from_one(engine):
    _busy(engine)
    assert [r["seq"] for r in records(engine)] == list(range(1, engine.evidence.count() + 1))


def test_each_record_links_to_its_predecessor(engine):
    _busy(engine)
    prev = GENESIS_HASH
    for rec in records(engine):
        assert rec["prev_hash"] == prev
        body = {k: v for k, v in rec.items() if k != "record_hash"}
        assert rec["record_hash"] == _record_hash(body)
        assert re.fullmatch(r"[0-9a-f]{64}", rec["record_hash"])
        prev = rec["record_hash"]


def test_timestamps_never_go_backwards(engine):
    _busy(engine)
    ts = [r["timestamp"] for r in records(engine)]
    assert all(isinstance(t, float) for t in ts)
    assert ts == sorted(ts)


def test_last_hash_and_count_match_the_file(engine):
    _busy(engine)
    recs = records(engine)
    assert engine.evidence.count() == len(recs)
    assert engine.evidence.last_hash() == recs[-1]["record_hash"]


def test_empty_log_reports_genesis(tmp_path):
    log = EvidenceLog(str(tmp_path / "none.jsonl"))
    assert (log.count(), log.last_hash(), log.verify()) == (0, GENESIS_HASH, (True, None))


def test_non_ascii_text_is_stored_verbatim(tmp_path):
    log = EvidenceLog(str(tmp_path / "e.jsonl"))
    log.append("NOTE", {"by": "Antonio José Socorro Marín", "where": "Ciudad de México"})
    raw = Path(log.path).read_text(encoding="utf-8")
    assert "José" in raw and "México" in raw and "\\u00e9" not in raw
    assert log.verify() == (True, None)


def test_one_json_object_per_line(engine):
    _busy(engine)
    lines = Path(engine.evidence.path).read_text(encoding="utf-8").splitlines()
    assert len(lines) == engine.evidence.count()
    for line in lines:
        assert isinstance(json.loads(line), dict)


def test_log_in_nested_directory_is_created(tmp_path):
    log = EvidenceLog(str(tmp_path / "a" / "b" / "e.jsonl"))
    log.append("X", {})
    assert log.count() == 1


def test_log_in_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    log = EvidenceLog("e.jsonl")
    log.append("X", {"n": 1})
    log.append("Y", {"n": 2})
    assert log.count() == 2 and (tmp_path / "e.jsonl").exists()


def test_blank_lines_are_ignored(tmp_path):
    log = EvidenceLog(str(tmp_path / "e.jsonl"))
    log.append("A", {})
    with open(log.path, "a", encoding="utf-8") as fh:
        fh.write("\n   \n")
    log.append("B", {})
    assert log.count() == 2 and log.verify() == (True, None)


@pytest.mark.parametrize("field", ["seq", "event_type", "prev_hash", "timestamp"])
def test_editing_any_header_field_is_detected(tmp_path, field):
    log = EvidenceLog(str(tmp_path / "e.jsonl"))
    for i in range(3):
        log.append(f"E{i}", {"i": i})
    lines = Path(log.path).read_text(encoding="utf-8").splitlines(keepends=True)
    rec = json.loads(lines[1])
    rec[field] = {"seq": 99, "event_type": "FORGED", "prev_hash": "f" * 64, "timestamp": 1.0}[field]
    lines[1] = json.dumps(rec) + "\n"
    Path(log.path).write_text("".join(lines), encoding="utf-8")
    ok, err = log.verify()
    assert ok is False
    assert err.startswith(("broken chain at seq", "tampered record at seq"))


def test_verify_names_the_kind_of_damage(tmp_path):
    log = EvidenceLog(str(tmp_path / "e.jsonl"))
    for i in range(3):
        log.append(f"E{i}", {"i": i})
    lines = Path(log.path).read_text(encoding="utf-8").splitlines(keepends=True)
    edited = json.loads(lines[2])
    edited["payload"]["i"] = 7
    Path(log.path).write_text(lines[0] + lines[1] + json.dumps(edited) + "\n", encoding="utf-8")
    assert log.verify() == (False, "tampered record at seq 3: hash mismatch")
    Path(log.path).write_text(lines[0] + lines[2], encoding="utf-8")
    assert log.verify() == (False, "broken chain at seq 3: prev_hash mismatch")


# ==========================================================================
# 2. Event names per operation (the vocabulary auditors search for)
# ==========================================================================
def test_init_event(engine):
    recs = records(engine)
    assert len(recs) == 1
    assert recs[0]["event_type"] == "ENGINE_INIT"
    assert recs[0]["payload"] == {"initial_state": "MODEL"}


def test_fact_event(engine):
    engine.set_fact("assets_discovered", 1)
    assert last(engine)["event_type"] == "FACT_SET"
    assert last(engine)["payload"] == {"fact": "assets_discovered", "value": True}


def test_telemetry_events(engine):
    good = {"source": "edr", "domain": "device", "confidence": 0.9, "provenance": "p", "timestamp": 5.0}
    out = engine.ingest(good)
    rec = last(engine)
    assert out == {"accepted": True, "id": rec["payload"]["event"]["id"]}
    assert rec["event_type"] == "TELEMETRY_ACCEPTED"
    assert {k: rec["payload"]["event"][k] for k in good} == good
    out = engine.ingest({"domain": "device", "confidence": 0.9, "timestamp": 5.0})
    rec = last(engine)
    assert out["accepted"] is False and out["errors"] == rec["payload"]["errors"]
    assert rec["event_type"] == "TELEMETRY_REJECTED"
    assert "missing source" in out["errors"] and "missing provenance metadata" in out["errors"]
    assert rec["payload"]["event"]["source"] == "" and rec["payload"]["event"]["provenance"] == ""


def test_telemetry_without_confidence_is_rejected(engine):
    out = engine.ingest({"source": "s", "domain": "device", "provenance": "p", "timestamp": 1.0})
    assert out["accepted"] is False
    assert "confidence must be a number in [0.0, 1.0]" in out["errors"]


def test_transition_events_and_results(engine):
    out = engine.transition("EVICT")
    assert out == {"status": "BLOCKED", "from": "MODEL", "to": "EVICT",
                   "reason": "MODEL -> EVICT is not a valid transition"}
    assert last(engine)["event_type"] == "TRANSITION_BLOCKED"
    assert last(engine)["payload"] == {"from": "MODEL", "to": "EVICT", "reason": "invalid transition"}

    out = engine.transition("harden")                       # case-insensitive
    assert out == {"status": "BLOCKED", "from": "MODEL", "to": "HARDEN",
                   "unmet_entry_conditions": ["assets_discovered", "telemetry_validated"]}
    assert last(engine)["payload"] == {"from": "MODEL", "to": "HARDEN",
                                       "unmet_entry_conditions": ["assets_discovered", "telemetry_validated"]}

    engine.set_fact("assets_discovered", True)
    engine.set_fact("telemetry_validated", True)
    assert engine.transition("HARDEN") == {"status": "OK", "from": "MODEL", "to": "HARDEN"}
    assert last(engine)["event_type"] == "STATE_TRANSITION"
    assert last(engine)["payload"] == {"from": "MODEL", "to": "HARDEN"}


def test_unknown_state_is_an_error_and_not_recorded(engine):
    n = engine.evidence.count()
    with pytest.raises(EngineError, match="unknown state 'PANIC'"):
        engine.transition("PANIC")
    assert engine.evidence.count() == n


@pytest.mark.parametrize("data,event,status", [
    ({"category": "OBSERVE", "description": "look", "target": "h"}, "ACTION_EXECUTED", "EXECUTED"),
    ({"category": "ERADICATION", "description": "wipe", "target": "h"}, "ACTION_BLOCKED", "BLOCKED"),
])
def test_proposal_events(engine, data, event, status):
    out = engine.propose(data)
    rec = last(engine)
    assert out["status"] == status and rec["event_type"] == event
    assert rec["payload"]["action"]["description"] == data["description"]
    assert rec["payload"]["state"] == "MODEL"
    if status == "EXECUTED":
        assert rec["payload"]["approved_by"] is None
        assert out["action_id"] == rec["payload"]["action"]["id"]


def test_pending_approve_and_deny_events(engine):
    to_state(engine, "HARDEN", "DETECT", "ISOLATE")
    a = engine.propose({"category": "CONTAINMENT", "description": "isolate", "target": "h1"})
    b = engine.propose({"category": "CONTAINMENT", "description": "isolate", "target": "h2"})
    assert a["status"] == b["status"] == "PENDING_APPROVAL"
    assert last(engine)["event_type"] == "ACTION_PENDING_APPROVAL"
    assert engine.status()["pending_approvals"] == [a["action_id"], b["action_id"]]

    out = engine.approve(a["action_id"], "ops.garcia")
    assert out == {"status": "EXECUTED", "action_id": a["action_id"], "approved_by": "ops.garcia"}
    r1, r2 = records(engine)[-2:]
    assert r1["event_type"] == "HUMAN_APPROVAL"
    assert r1["payload"] == {"action_id": a["action_id"], "approved_by": "ops.garcia"}
    assert r2["event_type"] == "ACTION_EXECUTED" and r2["payload"]["approved_by"] == "ops.garcia"

    out = engine.deny(b["action_id"], "ops.garcia", "wrong host")
    assert out == {"status": "DENIED_BY_HUMAN", "action_id": b["action_id"]}
    assert last(engine)["event_type"] == "HUMAN_DENIAL"
    assert last(engine)["payload"] == {"action_id": b["action_id"], "denied_by": "ops.garcia", "reason": "wrong host"}
    assert engine.status()["pending_approvals"] == []


def test_approval_requires_a_named_human_and_a_pending_action(engine):
    to_state(engine, "HARDEN", "DETECT", "ISOLATE")
    a = engine.propose({"category": "CONTAINMENT", "description": "x", "target": "h"})
    with pytest.raises(EngineError, match="approver name is required"):
        engine.approve(a["action_id"], "")
    assert engine.status()["pending_approvals"] == [a["action_id"]]   # still pending after the refusal
    with pytest.raises(EngineError, match="no pending action with id nope"):
        engine.approve("nope", "ops")
    with pytest.raises(EngineError, match="no pending action with id nope"):
        engine.deny("nope", "ops", "r")
    engine.approve(a["action_id"], "ops")
    with pytest.raises(EngineError):                                  # cannot approve twice
        engine.approve(a["action_id"], "ops")


@pytest.mark.parametrize("ctx,event", [
    ({}, "GOVERNED_DECISION_EXECUTED"),
    ({"sector": "energy", "safety_component": True}, "GOVERNED_DECISION_PENDING_APPROVAL"),
    ({"prohibited_practice": True}, "GOVERNED_DECISION_BLOCKED"),
])
def test_governed_events(engine, ctx, event):
    GovernedAgent(engine).govern(gp(**ctx))
    assert last(engine)["event_type"] == event


# ==========================================================================
# 3. Return values and status
# ==========================================================================
def test_status_contract(engine):
    st = engine.status()
    assert st == {"current_state": "MODEL", "allowed_transitions": ["HARDEN"],
                  "entry_conditions_next": {"HARDEN": ["assets_discovered", "telemetry_validated"]},
                  "facts": {}, "pending_approvals": [], "evidence_records": 1}
    to_state(engine, "HARDEN", "DETECT")
    st = engine.status()
    assert st["allowed_transitions"] == ["ISOLATE", "DECEIVE"]
    assert st["entry_conditions_next"] == {"ISOLATE": ["detection_confirmed"],
                                           "DECEIVE": ["detection_confirmed", "deception_scope_approved"]}
    assert st["facts"] == {f: True for f in ALL_FACTS}


def test_uninitialized_engine_refuses_to_work(tmp_path):
    eng = CAIEngine(home=str(tmp_path / "never"))
    with pytest.raises(EngineError, match="not initialized"):
        eng.status()


def test_verify_contract(engine):
    assert engine.verify() == {"integrity_ok": True, "error": None, "records": 1}


def test_report_lists_every_record(engine):
    _busy(engine)
    rep = engine.report()
    assert rep.startswith("# CAI-Engine — Execution & Assurance Report")
    assert "Evidence integrity: OK (chain verified)" in rep
    for rec in records(engine):
        assert f"| {rec['seq']} | {rec['event_type']} |" in rep


def test_state_survives_a_new_engine_instance(engine):
    to_state(engine, "HARDEN")
    again = CAIEngine(home=engine.home)
    assert again.status()["current_state"] == "HARDEN"
    assert again.status()["facts"]["safety_approved"] is True


# ==========================================================================
# 4. Action construction from JSON (_build_action)
# ==========================================================================
def test_every_action_field_is_carried_into_the_record(engine):
    to_state(engine, "HARDEN")
    out = engine.propose({"category": "HARDENING", "description": "patch", "target": "plc-3", "ot_level": 3,
                          "blast_radius": "7", "destructive": 0, "ai_assisted": 1, "ai_confidence": "0.91",
                          "ai_explainable": 1, "affects_privileged_accounts": 0})
    a = out["action"]
    assert (a["category"], a["description"], a["target"], a["ot_level"]) == ("HARDENING", "patch", "plc-3", 3)
    assert a["blast_radius"] == 7 and isinstance(a["blast_radius"], int)
    assert a["ai_confidence"] == 0.91 and isinstance(a["ai_confidence"], float)
    assert (a["destructive"], a["ai_assisted"], a["ai_explainable"], a["affects_privileged_accounts"]) == \
           (False, True, True, False)
    assert re.fullmatch(r"act-[0-9a-f]{10}", a["id"])


def test_action_defaults(engine):
    a = engine.propose({"category": "OBSERVE"})["action"]
    assert a == {**a, "description": "", "target": "", "ot_level": None, "blast_radius": 0,
                 "destructive": False, "ai_assisted": False, "ai_confidence": 1.0, "ai_explainable": True,
                 "affects_privileged_accounts": False}


@pytest.mark.parametrize("bad", [{}, {"category": "NUKE"}, {"category": ""}, {"category": "observe"}])
def test_invalid_category_is_refused_with_the_allowed_list(engine, bad):
    with pytest.raises(EngineError) as exc:
        engine.propose(bad)
    msg = str(exc.value)
    assert "invalid or missing 'category'" in msg
    for c in C:
        assert c.value in msg


@pytest.mark.parametrize("flag", ["destructive", "affects_privileged_accounts"])
def test_boolean_flags_change_the_outcome(engine, flag):
    to_state(engine, "HARDEN")
    out = engine.propose({"category": "HARDENING", "description": "x", flag: True})
    assert out["status"] == "PENDING_APPROVAL"


# ==========================================================================
# 5. Gate names and reasons (stable identifiers, values visible)
# ==========================================================================
def _act(cat=C.OBSERVE, **kw):
    return Action(category=cat, description="d", target="t", **kw)


def test_policy_gate_names_and_reasons():
    deny = policy_evaluate(_act(C.ERADICATION), State.MODEL)
    assert deny.gate == "policy.state_constraint"
    assert deny.reason == "action category ERADICATION is not permitted in state MODEL (permitted: ['OBSERVE'])"
    allow = policy_evaluate(_act(C.OBSERVE), State.MODEL)
    assert (allow.gate, allow.reason) == ("policy.state_constraint", "action permitted by state constraints")


def test_category_given_as_string_is_normalized():
    a = Action(category="CONTAINMENT", description="d")
    assert policy_evaluate(a, State.ISOLATE).decision == Decision.ALLOW
    assert a.normalized_category() is C.CONTAINMENT


def test_safety_gate_names_and_reasons():
    res = {g.gate: g for g in safety_gates(_act(C.CONTAINMENT, ai_assisted=True, ai_confidence=0.65,
                                                ai_explainable=False, ot_level=1, destructive=True,
                                                blast_radius=30))}
    assert set(res) == {"safety.ai_confidence", "safety.ai_explainability", "safety.ot_ics",
                        "safety.operational_impact", "safety.blast_radius"}
    assert res["safety.ai_confidence"].reason == "AI confidence 0.65 < minimum 0.80"
    assert res["safety.ai_explainability"].reason == "AI output is not explainable; cannot trigger action"
    assert res["safety.ot_ics"].reason.startswith("OT/ICS asset at Purdue level 1: human approval required")
    assert res["safety.operational_impact"].reason == "destructive action: human approval required before execution"
    assert res["safety.blast_radius"].reason == "blast radius 30 assets > threshold 25"
    none = safety_gates(_act())
    assert [(g.gate, g.decision, g.reason) for g in none] == \
           [("safety.none_triggered", Decision.ALLOW, "no safety gate triggered")]


def _eu(ctx, **kw):
    args = dict(confidence=0.95, explainable=True, explanation="e", drift_score=0.0, human_disclosed=True)
    args.update(kw)
    return {g.gate: g for g in eu_ai_act.eu_gates(eu_ai_act.classify(eu_ai_act.AIContext(**ctx)), **args)}


def test_eu_gate_names_and_reasons():
    hi = _eu({"sector": "energy", "safety_component": True}, confidence=0.85, drift_score=0.2, explanation="")
    assert set(hi) == {"eu.art14_human_oversight", "eu.art15_accuracy", "eu.art15_robustness",
                       "eu.art13_transparency", "eu.art12_record_keeping"}
    assert hi["eu.art14_human_oversight"].reason == "high-risk: human oversight required (Art. 14)"
    assert hi["eu.art15_accuracy"].reason == "confidence 0.85 < high-risk minimum 0.90"
    assert hi["eu.art15_robustness"].reason == "model drift 0.20 > maximum 0.15"
    assert hi["eu.art13_transparency"].reason == "high-risk decision lacks an explanation (Art. 13)"
    assert (hi["eu.art12_record_keeping"].decision, hi["eu.art12_record_keeping"].reason) == \
           (Decision.ALLOW, "decision recorded in hash-chained evidence log (Art. 12)")

    pro = eu_ai_act.eu_gates(eu_ai_act.classify(eu_ai_act.AIContext(prohibited_practice=True)), confidence=1,
                             explainable=True, explanation="e", drift_score=0, human_disclosed=True)
    assert [(g.gate, g.decision, g.reason) for g in pro] == \
           [("eu.art5_prohibited", Decision.DENY, "Art. 5 prohibited practice: unspecified")]

    lim = _eu({"interacts_with_persons": True}, confidence=0.6, human_disclosed=False)
    assert lim["eu.art50_transparency"].reason == "limited risk: AI interaction/content must be disclosed (Art. 50)"
    assert lim["eu.art50_quality"].reason == "confidence 0.60 < minimum 0.70"
    ok = _eu({"interacts_with_persons": True})
    assert [(g.gate, g.decision, g.reason) for g in ok.values()] == \
           [("eu.art50_transparency", Decision.ALLOW, "transparency satisfied")]
    mini = _eu({})
    assert [(g.gate, g.decision, g.reason) for g in mini.values()] == \
           [("eu.minimal_risk", Decision.ALLOW, "minimal risk — no EU gate triggered")]


def test_eu_classification_texts():
    c = eu_ai_act.classify
    A = eu_ai_act.AIContext
    assert c(A(prohibited_practice=True, prohibited_reason="social scoring")).rationale == \
           "Art. 5 prohibited practice: social scoring"
    p = c(A(prohibited_practice=True))
    assert (p.annex_refs, p.obligations) == (["Art.5"], {})
    h = c(A(sector="Energy", safety_component=True, biometric=True, affects_essential_services=True,
            law_enforcement=True))
    assert h.annex_refs == ["Annex III(1) — Biometrics",
                            "Annex III(2) — Critical infrastructure (safety components)",
                            "Annex III(5) — Access to essential private and public services",
                            "Annex III(6) — Law enforcement"]
    assert h.rationale == "High-risk under Art. 6 and " + "; ".join(h.annex_refs)
    assert h.obligations == eu_ai_act.HIGH_RISK_OBLIGATIONS and h.obligations is not eu_ai_act.HIGH_RISK_OBLIGATIONS
    lim = c(A(generates_content=True))
    assert (lim.rationale, lim.annex_refs, lim.obligations) == \
           ("Limited risk — Art. 50 transparency obligations apply", [], {"Art.50": "Transparency obligations"})
    m = c(A())
    assert (m.rationale, m.annex_refs, m.obligations) == ("Minimal risk — no specific obligations", [], {})


def _us(sector, **kw):
    args = dict(confidence=0.99, explainable=True, explanation="e", drift_score=0.0, genai=False,
                provenance="p", action_is_ot=False, action_destructive=False, prohibited=False,
                prohibited_reason="")
    args.update(kw)
    cls = usa.classify(eu_ai_act.AIContext(sector=sector))
    return cls, {g.gate: g for g in usa.usa_gates(cls, **args)}


def test_usa_gate_names_and_reasons():
    cls, g = _us("energy", confidence=0.9, drift_score=0.3, action_is_ot=True)
    assert set(g) == {"usa.nist_ai_rmf", "usa.srma_oversight", "usa.assurance_floor", "usa.robustness",
                      "usa.ot_ics_safety"}
    assert g["usa.nist_ai_rmf"].reason == "governed under NIST AI RMF (Govern/Map/Measure/Manage)"
    assert g["usa.srma_oversight"].reason == "Energy: human oversight under SRMA Department of Energy"
    assert g["usa.assurance_floor"].reason == "confidence 0.90 < CATASTROPHIC floor 0.95"
    assert g["usa.robustness"].reason == "model drift 0.30 > maximum 0.15"
    assert g["usa.ot_ics_safety"].reason == "Energy is OT-intensive: cyber-physical safety approval required"
    _, g = _us("retail", confidence=0.6)
    assert g["usa.assurance_floor"].reason == "confidence 0.60 < non-critical floor 0.70"
    assert g["usa.assurance_floor"].decision == Decision.DENY
    _, g = _us("energy", prohibited=True)
    assert list(g) == ["usa.unlawful_use"] and g["usa.unlawful_use"].reason == "use designated unlawful/prohibited"
    _, g = _us("energy", prohibited=True, prohibited_reason="mass surveillance")
    assert g["usa.unlawful_use"].reason == "mass surveillance"
    _, g = _us("healthcare", genai=True)
    assert (g["usa.nist_ai_600_1"].decision, g["usa.nist_ai_600_1"].reason) == \
           (Decision.ALLOW, "generative AI provenance and explanation present")
    _, g = _us("healthcare", genai=True, provenance="  ")
    assert g["usa.nist_ai_600_1"].reason == "generative AI without provenance/explanation (NIST AI 600-1)"


def test_usa_classification_record():
    cls = usa.classify(eu_ai_act.AIContext(sector="electricity"))
    assert (cls.posture, cls.sector_key, cls.sector_name, cls.srma, cls.consequence, cls.ot_intensive) == \
           ("CRITICAL_INFRASTRUCTURE", "energy", "Energy", "Department of Energy", "CATASTROPHIC", True)
    assert cls.references == ["NIST AI RMF 1.0", "NSM-22 sector: Energy (SRMA: Department of Energy)"]
    nc = usa.classify(eu_ai_act.AIContext(sector="retail"))
    assert (nc.posture, nc.sector_key, nc.sector_name, nc.srma, nc.consequence, nc.ot_intensive, nc.references) == \
           ("NON_CRITICAL", "", "retail", "n/a", "MODERATE", False, ["NIST AI RMF 1.0"])
    assert usa.classify(eu_ai_act.AIContext(sector="")).sector_name == "unspecified"


# ==========================================================================
# 6. Governed decision record (regulatory block, defaults, NIST trace)
# ==========================================================================
def test_eu_governed_record(engine):
    out = GovernedAgent(engine).govern(gp(sector="energy", safety_component=True))
    rec = last(engine)["payload"]
    assert rec["decision_id"] == out["action_id"] and re.fullmatch(r"gov-[0-9a-f]{10}", rec["decision_id"])
    assert (rec["jurisdiction"], rec["ai_system"], rec["model_version"]) == ("EU", "soc-llm", "2.1")
    reg = rec["regulatory"]
    assert reg["framework"] == "EU AI Act (Reg. (EU) 2024/1689, amended by Digital Omnibus (EU) 2026/1744)"
    assert (reg["jurisdiction"], reg["label"]) == ("EU", "HIGH")
    assert reg["annex_refs"] == ["Annex III(2) — Critical infrastructure (safety components)"]
    assert set(reg["obligations"]) == {f"Art.{n}" for n in (9, 10, 11, 12, 13, 14, 15)}
    assert reg["rationale"].startswith("High-risk under Art. 6")
    assert {g["gate"] for g in reg["gate_results"]} == {"eu.art14_human_oversight", "eu.art12_record_keeping"}
    assert rec["cai_engine"] == {"state": "MODEL", "decision": "ALLOW", "gate_results": rec["cai_engine"]["gate_results"]}
    assert [g["gate"] for g in rec["cai_engine"]["gate_results"]] == ["policy.state_constraint", "safety.none_triggered"]
    assert (rec["decision"], rec["requires_human_approval"]) == ("ESCALATE", True)
    assert rec["action"]["ai_assisted"] is True and rec["action"]["ai_confidence"] == 0.95


def test_usa_governed_record(engine):
    GovernedAgent(engine).govern(gp(juris="usa", sector="water"))      # jurisdiction is case-insensitive
    reg = last(engine)["payload"]["regulatory"]
    assert reg == {**reg, "framework": "CAI-USA (NIST AI RMF / NIST AI 600-1 / NSM-22)", "jurisdiction": "USA",
                   "label": "CRITICAL_INFRASTRUCTURE", "sector": "Water and Wastewater Systems",
                   "srma": "Environmental Protection Agency", "consequence": "CATASTROPHIC", "ot_intensive": True}
    assert reg["references"][1] == "NSM-22 sector: Water and Wastewater Systems (SRMA: Environmental Protection Agency)"


def test_jurisdiction_argument_overrides_the_proposal(engine):
    GovernedAgent(engine).govern(gp(juris="EU", sector="energy"), jurisdiction="USA")
    assert last(engine)["payload"]["jurisdiction"] == "USA"


def test_default_jurisdiction_is_used_when_absent(engine):
    p = gp()
    del p["jurisdiction"]
    GovernedAgent(engine, default_jurisdiction="usa").govern(p)
    assert last(engine)["payload"]["jurisdiction"] == "USA"


def test_defaults_when_ai_metadata_is_missing(engine):
    p = {"ai": {"confidence": 0.95, "explanation": "because"}, "context": {}, "action": {"category": "OBSERVE"}}
    GovernedAgent(engine).govern(p)
    rec = last(engine)["payload"]
    assert (rec["ai_system"], rec["model_version"]) == ("unknown", "unknown")
    assert rec["action"]["ai_explainable"] is True                 # explanation present -> explainable


def test_missing_explanation_means_not_explainable(engine):
    p = {"jurisdiction": "EU", "ai": {"confidence": 0.95}, "context": {"sector": "energy", "safety_component": True},
         "action": {"category": "OBSERVE"}}
    out = GovernedAgent(engine).govern(p)
    assert out["status"] == "BLOCKED"
    gates = {g["gate"] for g in last(engine)["payload"]["regulatory"]["gate_results"]}
    assert "eu.art13_transparency" in gates
    assert last(engine)["payload"]["action"]["ai_explainable"] is False


def test_missing_confidence_counts_as_zero(engine):
    p = {"ai": {"explanation": "e"}, "context": {}, "action": {"category": "OBSERVE"}}
    assert GovernedAgent(engine).govern(p)["status"] == "BLOCKED"


def test_drift_and_disclosure_are_read_from_the_proposal(engine):
    p = gp(sector="energy", safety_component=True)
    p["ai"]["drift_score"] = 0.5
    assert GovernedAgent(engine).govern(p)["status"] == "BLOCKED"
    q = gp(interacts_with_persons=True)
    q["ai"]["human_disclosed"] = False
    assert GovernedAgent(engine).govern(q)["status"] == "PENDING_APPROVAL"
    q["ai"].pop("human_disclosed")
    assert GovernedAgent(engine).govern(q)["status"] == "PENDING_APPROVAL"   # default: not disclosed


def test_usa_genai_flag_from_ai_or_context(engine):
    p = gp(juris="USA", sector="healthcare")
    p["ai"].update(genai=True, provenance="")
    assert GovernedAgent(engine).govern(p)["status"] == "BLOCKED"
    q = gp(juris="USA", sector="healthcare", generates_content=True)
    q["ai"]["provenance"] = ""
    assert GovernedAgent(engine).govern(q)["status"] == "BLOCKED"


def test_usa_ot_and_destructive_actions_trigger_ot_gate(engine):
    for extra in ({"ot_level": 2}, {"destructive": True}):
        p = gp(juris="USA", sector="energy")
        p["action"].update(extra)
        GovernedAgent(engine).govern(p)
        gates = {g["gate"] for g in last(engine)["payload"]["regulatory"]["gate_results"]}
        assert "usa.ot_ics_safety" in gates, extra


def test_usa_prohibited_context_is_denied(engine):
    out = GovernedAgent(engine).govern(gp(juris="USA", sector="energy", prohibited_practice=True,
                                          prohibited_reason="unlawful"))
    assert out["status"] == "BLOCKED"
    assert last(engine)["payload"]["regulatory"]["gate_results"] == \
           [{"gate": "usa.unlawful_use", "decision": "DENY", "reason": "unlawful"}]


def test_nist_ai_rmf_trace_in_record(engine):
    GovernedAgent(engine).govern(gp(sector="energy", safety_component=True))
    t = last(engine)["payload"]["nist_ai_rmf"]
    assert set(t) == {"GOVERN", "MAP", "MEASURE", "MANAGE"}
    assert t["MAP"] == ("deployment context classified under EU AI Act (Reg. (EU) 2024/1689, amended by "
                        "Digital Omnibus (EU) 2026/1744) (classification = HIGH)")
    assert t["MEASURE"] == "confidence=0.95, drift=0.03, explainable=True"
    assert t["MANAGE"] == ("decision=ESCALATE; human_oversight=required; "
                           "recorded in hash-chained evidence log")


def test_rmf_trace_function():
    t = rmf_trace("MINIMAL", 0.5, 0.1, False, False, "ALLOW")
    assert t == {"GOVERN": "policy, safety and human-authority constraints enforced by the engine",
                 "MAP": "deployment context classified (classification = MINIMAL)",
                 "MEASURE": "confidence=0.50, drift=0.10, explainable=False",
                 "MANAGE": "decision=ALLOW; human_oversight=not required; recorded in hash-chained evidence log"}
