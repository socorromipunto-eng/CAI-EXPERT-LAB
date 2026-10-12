"""Specification test matrix for the CAI-Engine reference implementation.

Part of CAI-EXPERT-LAB (owner: Antonio José Socorro Marín).

Purpose
    test_cai_engine.py checks representative behaviour. This module checks the
    engine against the CAI specifications case by case: every state, every
    action category, every transition, every NSM-22 sector, every EU AI Act
    tier, every gate threshold at its boundary, and every way of tampering with
    the evidence log. Expected values are written out from the specifications,
    not read back from the code under test, so a test cannot pass by agreeing
    with a wrong table.

Sources (cited per test group)
    SME  CAI-Engine/CAI-Engine-State-Machine-Execution.md
    SGH  CAI-Engine/CAI-Engine-Safety-Gates-and-Human-Oversight.md
    TAX  docs/CORE/CAI-Core-Taxonomy.md  (section 8.6: decision integrity condition)
    EU   Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744
    USA  NSM-22 (2024) sector list; NIST AI RMF 1.0; NIST AI 600-1

Known gaps
    Tests marked `xfail(strict=True)` describe behaviour the specifications
    require and engine 0.4.2 does not yet provide. Each carries the finding ID.
    `strict=True` makes the suite FAIL when a gap is fixed, so the marker must
    then be removed: a known gap can never silently disappear from the record.

Run (from CAI-Engine/implementation):  python -m pytest -q tests/TEST_SPECIFICATION_MATRIX.py
"""
from __future__ import annotations

import itertools
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import pytest

from cai_engine import eu_ai_act, usa, usa_sectors
from cai_engine.core import Action, ActionCategory, State, TelemetryEvent
from cai_engine.engine import CAIEngine, EngineError
from cai_engine.evidence import EvidenceLog
from cai_engine.gates import (Decision, GateResult, policy_evaluate, requires_human_approval,
                              safety_gates, summarize)
from cai_engine.governed_agent import GovernedAgent

HERE = Path(__file__).resolve().parent
IMPL = HERE.parent
EXAMPLES = IMPL / "examples"

C = ActionCategory
S = State
ALL_FACTS = ("assets_discovered", "telemetry_validated", "baseline_hardened", "telemetry_active",
             "detection_confirmed", "deception_scope_approved", "malicious_presence_confirmed",
             "safety_approved", "eviction_completed", "clean_baseline_validated")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
@pytest.fixture
def engine(tmp_path):
    eng = CAIEngine(home=str(tmp_path / "rt"))
    eng.init()
    return eng


# Shortest valid path from MODEL to each state (SME section 7).
PATH_TO = {
    S.MODEL: [],
    S.HARDEN: [S.HARDEN],
    S.DETECT: [S.HARDEN, S.DETECT],
    S.ISOLATE: [S.HARDEN, S.DETECT, S.ISOLATE],
    S.DECEIVE: [S.HARDEN, S.DETECT, S.DECEIVE],
    S.EVICT: [S.HARDEN, S.DETECT, S.ISOLATE, S.EVICT],
    S.RESTORE: [S.HARDEN, S.DETECT, S.ISOLATE, S.EVICT, S.RESTORE],
}


def drive(eng: CAIEngine, target: State) -> None:
    for f in ALL_FACTS:
        eng.set_fact(f, True)
    for s in PATH_TO[target]:
        out = eng.transition(s.value)
        assert out["status"] == "OK", out
    assert eng.status()["current_state"] == target.value


def action(cat: C, **kw) -> Action:
    return Action(category=cat, description="test", target="t", **kw)


def decisions(results: list[GateResult]) -> set[str]:
    return {g.decision.value for g in results}


def proposal(*, juris="EU", conf=0.95, sector="", category="OBSERVE", drift=0.0, explanation="why",
             explainable=True, provenance="cces://x", disclosed=True, **ctx) -> dict:
    return {"jurisdiction": juris,
            "ai": {"system": "t", "model_version": "1", "confidence": conf, "explanation": explanation,
                   "explainable": explainable, "provenance": provenance, "drift_score": drift,
                   "human_disclosed": disclosed},
            "context": {"sector": sector, **ctx},
            "action": {"category": category, "description": "d", "target": "t"}}


# ==========================================================================
# 1. Policy: state x action category  (SME section 6)              42 cases
# ==========================================================================
# MODEL "no operational actions"; DETECT "no containment or eradication" (the
# engine is stricter and allows OBSERVE only); ISOLATE "containment only";
# DECEIVE "approved deception assets"; EVICT eradication; RESTORE recovery;
# HARDEN hardening. OBSERVE is never operational and is allowed everywhere.
ALLOWED = {
    S.MODEL: {C.OBSERVE},
    S.HARDEN: {C.OBSERVE, C.HARDENING},
    S.DETECT: {C.OBSERVE},
    S.ISOLATE: {C.OBSERVE, C.CONTAINMENT},
    S.DECEIVE: {C.OBSERVE, C.DECEPTION},
    S.EVICT: {C.OBSERVE, C.ERADICATION},
    S.RESTORE: {C.OBSERVE, C.RECOVERY},
}


@pytest.mark.parametrize("state,cat", list(itertools.product(S, C)),
                         ids=lambda v: v.value)
def test_policy_state_constraint(state, cat):
    g = policy_evaluate(action(cat), state)
    expected = Decision.ALLOW if cat in ALLOWED[state] else Decision.DENY
    assert g.decision == expected, g.reason


# Hard invariants stated literally in SME section 6 (independent of the table above).
@pytest.mark.parametrize("cat", [c for c in C if c != C.OBSERVE], ids=lambda v: v.value)
def test_model_permits_no_operational_action(cat):
    assert policy_evaluate(action(cat), S.MODEL).decision == Decision.DENY


@pytest.mark.parametrize("cat", [C.CONTAINMENT, C.ERADICATION], ids=lambda v: v.value)
def test_detect_permits_no_containment_or_eradication(cat):
    assert policy_evaluate(action(cat), S.DETECT).decision == Decision.DENY


# ==========================================================================
# 2. Transitions: every ordered pair of states  (SME section 7)    49 cases
# ==========================================================================
VALID = {(S.MODEL, S.HARDEN), (S.HARDEN, S.DETECT), (S.DETECT, S.ISOLATE), (S.DETECT, S.DECEIVE),
         (S.ISOLATE, S.EVICT), (S.DECEIVE, S.EVICT), (S.EVICT, S.RESTORE), (S.RESTORE, S.MODEL)}


@pytest.mark.parametrize("src,dst", list(itertools.product(S, S)), ids=lambda v: v.value)
def test_transition_matrix(engine, src, dst):
    drive(engine, src)
    before = engine.evidence.count()
    out = engine.transition(dst.value)
    if (src, dst) in VALID:
        assert out["status"] == "OK"
        assert engine.status()["current_state"] == dst.value
    else:
        assert out["status"] == "BLOCKED"
        assert engine.status()["current_state"] == src.value      # SME 9: stays in last valid state
    assert engine.evidence.count() == before + 1                  # every attempt is evidenced


# ==========================================================================
# 3. Entry conditions: each required fact missing  (SME section 5)  13 cases
# ==========================================================================
REQUIRED = {
    S.HARDEN: ["assets_discovered", "telemetry_validated"],
    S.DETECT: ["baseline_hardened", "telemetry_active"],
    S.ISOLATE: ["detection_confirmed"],
    S.DECEIVE: ["detection_confirmed", "deception_scope_approved"],
    S.EVICT: ["malicious_presence_confirmed", "safety_approved"],
    S.RESTORE: ["eviction_completed", "clean_baseline_validated"],
}
ENTRY_CASES = [(src, dst, fact) for (src, dst) in sorted(VALID, key=lambda p: (p[0].value, p[1].value))
               for fact in REQUIRED.get(dst, [])]


@pytest.mark.parametrize("src,dst,fact", ENTRY_CASES,
                         ids=[f"{a.value}-{b.value}-{f}" for a, b, f in ENTRY_CASES])
def test_entry_condition_missing_blocks(engine, src, dst, fact):
    drive(engine, src)
    engine.set_fact(fact, False)
    out = engine.transition(dst.value)
    assert out["status"] == "BLOCKED"
    assert fact in out["unmet_entry_conditions"]
    assert engine.status()["current_state"] == src.value


# ==========================================================================
# 4. AI confidence and explainability gate  (SGH 4.4)              17 cases
# ==========================================================================
AI_FLOOR = 0.80


@pytest.mark.parametrize("conf", [0.0, 0.1, 0.5, 0.65, 0.79, 0.7999, 0.80, 0.8001, 0.9, 0.95, 1.0])
def test_ai_confidence_floor(conf):
    res = safety_gates(action(C.OBSERVE, ai_assisted=True, ai_confidence=conf))
    denied = any(g.gate == "safety.ai_confidence" and g.decision == Decision.DENY for g in res)
    assert denied == (conf < AI_FLOOR)


@pytest.mark.parametrize("conf", [0.0, 0.5, 0.79])
def test_confidence_gate_ignores_non_ai_actions(conf):
    res = safety_gates(action(C.OBSERVE, ai_assisted=False, ai_confidence=conf))
    assert "DENY" not in decisions(res)


@pytest.mark.parametrize("conf", [0.85, 0.99, 1.0])
def test_non_explainable_ai_output_is_denied(conf):
    res = safety_gates(action(C.OBSERVE, ai_assisted=True, ai_confidence=conf, ai_explainable=False))
    assert any(g.gate == "safety.ai_explainability" and g.decision == Decision.DENY for g in res)


# ==========================================================================
# 5. OT/ICS gate: Purdue level x category x destructive  (SGH 4.2)  84 cases
# ==========================================================================
@pytest.mark.parametrize("level,cat,destructive",
                         list(itertools.product([None, 0, 1, 2, 3, 4, 5], C, [False, True])),
                         ids=lambda v: str(v.value if isinstance(v, C) else v))
def test_ot_ics_gate(level, cat, destructive):
    res = safety_gates(action(cat, ot_level=level, destructive=destructive))
    ot = [g for g in res if g.gate == "safety.ot_ics"]
    sensitive = level is not None and level <= 2
    expected = sensitive and (cat in (C.CONTAINMENT, C.ERADICATION) or destructive)
    assert bool(ot) == expected
    if ot:
        assert ot[0].decision == Decision.ESCALATE


# ==========================================================================
# 6. Blast radius and operational impact  (SGH 4.1, 4.3)            10 cases
# ==========================================================================
@pytest.mark.parametrize("radius", [0, 1, 10, 24, 25, 26, 100, 10_000])
def test_blast_radius_gate(radius):
    res = safety_gates(action(C.HARDENING, blast_radius=radius))
    escalated = any(g.gate == "safety.blast_radius" for g in res)
    assert escalated == (radius > 25)


@pytest.mark.parametrize("cat", [C.HARDENING, C.RECOVERY])
def test_destructive_action_is_escalated(cat):
    res = safety_gates(action(cat, destructive=True))
    assert any(g.gate == "safety.operational_impact" and g.decision == Decision.ESCALATE for g in res)


# ==========================================================================
# 7. Mandatory human approval  (SGH 5.1)                            48 cases
# ==========================================================================
@pytest.mark.parametrize("state,cat", list(itertools.product(S, C)), ids=lambda v: v.value)
def test_human_approval_by_state_and_category(state, cat):
    a = action(cat)
    gates = [policy_evaluate(a, state)] + safety_gates(a)
    expected = state == S.EVICT or cat in (C.CONTAINMENT, C.RECOVERY)
    assert requires_human_approval(a, state, gates) == expected


@pytest.mark.parametrize("cat", list(C), ids=lambda v: v.value)
def test_privileged_account_impact_needs_human(cat):
    a = action(cat, affects_privileged_accounts=True)
    assert requires_human_approval(a, S.HARDEN, safety_gates(a)) is True


# ==========================================================================
# 8. Combination rule: DENY > ESCALATE > ALLOW  (SME 8)              27 cases
# ==========================================================================
@pytest.mark.parametrize("triple", list(itertools.product(Decision, repeat=3)),
                         ids=lambda t: "-".join(d.value for d in t))
def test_summarize_is_conservative(triple):
    res = [GateResult(f"g{i}", d, "") for i, d in enumerate(triple)]
    got = summarize(res)
    if Decision.DENY in triple:
        assert got == Decision.DENY
    elif Decision.ESCALATE in triple:
        assert got == Decision.ESCALATE
    else:
        assert got == Decision.ALLOW


# ==========================================================================
# 9. EU AI Act classification  (EU Art. 5, 6, Annex III, Art. 50)   40 cases
# ==========================================================================
EU_CRITICAL = sorted(eu_ai_act.CRITICAL_SECTORS)
EU_NON_CRITICAL = ["corporate_it", "retail", "media", "education", ""]


@pytest.mark.parametrize("sector,safety", list(itertools.product(EU_CRITICAL + EU_NON_CRITICAL, [False, True])))
def test_eu_annex_iii_2_critical_infrastructure(sector, safety):
    cls = eu_ai_act.classify(eu_ai_act.AIContext(sector=sector, safety_component=safety))
    high = sector in eu_ai_act.CRITICAL_SECTORS and safety
    assert (cls.tier == eu_ai_act.RiskTier.HIGH) == high
    if high:
        assert set(cls.obligations) == {f"Art.{n}" for n in (9, 10, 11, 12, 13, 14, 15)}


@pytest.mark.parametrize("flags,tier", [
    ({"prohibited_practice": True}, "UNACCEPTABLE"),
    ({"prohibited_practice": True, "biometric": True}, "UNACCEPTABLE"),   # Art. 5 dominates
    ({"biometric": True}, "HIGH"),
    ({"affects_essential_services": True}, "HIGH"),
    ({"law_enforcement": True}, "HIGH"),
    ({"interacts_with_persons": True}, "LIMITED"),
    ({"generates_content": True}, "LIMITED"),
    ({"biometric": True, "interacts_with_persons": True}, "HIGH"),        # higher tier wins
    ({}, "MINIMAL"),
    ({"sector": "energy"}, "MINIMAL"),                                     # sector alone is not Annex III(2)
])
def test_eu_tiers(flags, tier):
    assert eu_ai_act.classify(eu_ai_act.AIContext(**flags)).tier.value == tier


# ==========================================================================
# 10. EU gates at their thresholds  (EU Art. 13, 14, 15, 50)        18 cases
# ==========================================================================
HIGH_CLS = eu_ai_act.classify(eu_ai_act.AIContext(sector="energy", safety_component=True))
LIM_CLS = eu_ai_act.classify(eu_ai_act.AIContext(interacts_with_persons=True))


@pytest.mark.parametrize("conf", [0.5, 0.89, 0.8999, 0.90, 0.95, 1.0])
def test_eu_high_risk_accuracy_floor(conf):
    g = eu_ai_act.eu_gates(HIGH_CLS, confidence=conf, explainable=True, explanation="e",
                           drift_score=0.0, human_disclosed=True)
    assert any(x.gate == "eu.art15_accuracy" for x in g) == (conf < 0.90)
    assert any(x.gate == "eu.art14_human_oversight" and x.decision == Decision.ESCALATE for x in g)


@pytest.mark.parametrize("drift", [0.0, 0.10, 0.15, 0.1501, 0.5])
def test_eu_high_risk_drift_limit(drift):
    g = eu_ai_act.eu_gates(HIGH_CLS, confidence=0.95, explainable=True, explanation="e",
                           drift_score=drift, human_disclosed=True)
    assert any(x.gate == "eu.art15_robustness" for x in g) == (drift > 0.15)


@pytest.mark.parametrize("explainable,explanation", [(False, "e"), (True, ""), (True, "   ")])
def test_eu_high_risk_needs_explanation(explainable, explanation):
    g = eu_ai_act.eu_gates(HIGH_CLS, confidence=0.95, explainable=explainable, explanation=explanation,
                           drift_score=0.0, human_disclosed=True)
    assert any(x.gate == "eu.art13_transparency" and x.decision == Decision.DENY for x in g)


@pytest.mark.parametrize("conf,disclosed,expect", [
    (0.69, True, "DENY"), (0.70, True, "ALLOW"), (0.95, False, "ESCALATE"), (0.60, False, "DENY")])
def test_eu_limited_risk(conf, disclosed, expect):
    g = eu_ai_act.eu_gates(LIM_CLS, confidence=conf, explainable=True, explanation="e",
                           drift_score=0.0, human_disclosed=disclosed)
    assert summarize(g).value == expect


# ==========================================================================
# 11. USA: the 16 NSM-22 sectors  (USA)                             ~90 cases
# ==========================================================================
NSM22 = {  # sector key -> (Sector Risk Management Agency, consequence, OT-intensive)
    "chemical": ("CISA (DHS)", "CATASTROPHIC", True),
    "commercial_facilities": ("CISA (DHS)", "MODERATE", False),
    "communications": ("CISA (DHS)", "HIGH", True),
    "critical_manufacturing": ("CISA (DHS)", "HIGH", True),
    "dams": ("CISA (DHS)", "CATASTROPHIC", True),
    "defense_industrial_base": ("Department of Defense", "HIGH", True),
    "emergency_services": ("CISA (DHS)", "HIGH", False),
    "energy": ("Department of Energy", "CATASTROPHIC", True),
    "financial_services": ("Department of the Treasury", "HIGH", False),
    "food_agriculture": ("USDA and HHS (FDA)", "HIGH", True),
    "government_facilities": ("CISA (DHS) and GSA", "HIGH", False),
    "healthcare": ("Department of Health and Human Services", "HIGH", False),
    "information_technology": ("CISA (DHS)", "HIGH", False),
    "nuclear": ("CISA (DHS)", "CATASTROPHIC", True),
    "transportation": ("TSA and U.S. Coast Guard (DHS)", "CATASTROPHIC", True),
    "water": ("Environmental Protection Agency", "CATASTROPHIC", True),
}
FLOOR = {"CATASTROPHIC": 0.95, "HIGH": 0.90, "MODERATE": 0.80, "NON_CRITICAL": 0.70}


def test_exactly_sixteen_nsm22_sectors():
    assert set(usa_sectors.SECTORS) == set(NSM22)


@pytest.mark.parametrize("key", sorted(NSM22))
def test_usa_sector_profile(key):
    srma, consequence, ot = NSM22[key]
    s = usa_sectors.resolve(key)
    assert (s.srma, s.consequence, s.ot_intensive) == (srma, consequence, ot)


@pytest.mark.parametrize("key,offset", list(itertools.product(sorted(NSM22), [-0.01, 0.0])))
def test_usa_assurance_floor_per_sector(key, offset):
    cls = usa.classify(eu_ai_act.AIContext(sector=key))
    conf = round(FLOOR[NSM22[key][1]] + offset, 4)
    g = usa.usa_gates(cls, confidence=conf, explainable=True, explanation="e", drift_score=0.0,
                      genai=False, provenance="p", action_is_ot=False, action_destructive=False,
                      prohibited=False, prohibited_reason="")
    assert any(x.gate == "usa.assurance_floor" for x in g) == (offset < 0)
    assert any(x.gate == "usa.srma_oversight" and x.decision == Decision.ESCALATE for x in g)


@pytest.mark.parametrize("key,is_ot", list(itertools.product(sorted(NSM22), [False, True])))
def test_usa_ot_safety_escalation(key, is_ot):
    cls = usa.classify(eu_ai_act.AIContext(sector=key))
    g = usa.usa_gates(cls, confidence=0.99, explainable=True, explanation="e", drift_score=0.0,
                      genai=False, provenance="p", action_is_ot=is_ot, action_destructive=False,
                      prohibited=False, prohibited_reason="")
    assert any(x.gate == "usa.ot_ics_safety" for x in g) == (NSM22[key][2] and is_ot)


@pytest.mark.parametrize("alias,key", [
    ("electricity", "energy"), ("power", "energy"), ("gas", "energy"), ("oil", "energy"),
    ("aviation", "transportation"), ("rail", "transportation"), ("maritime", "transportation"),
    ("transit", "transportation"), ("wastewater", "water"), ("drinking_water", "water"),
    ("it", "information_technology"), ("telecom", "communications"), ("bank", "financial_services"),
    ("banking", "financial_services"), ("hospital", "healthcare"), ("public_health", "healthcare"),
    ("manufacturing", "critical_manufacturing"), ("Financial Services", "financial_services"),
    ("defense-industrial-base", "defense_industrial_base"), ("  ENERGY ", "energy"),
])
def test_usa_sector_aliases(alias, key):
    assert usa_sectors.resolve(alias).key == key


@pytest.mark.parametrize("name", ["corporate_it", "retail", "unknown", ""])
def test_usa_non_critical_floor(name):
    cls = usa.classify(eu_ai_act.AIContext(sector=name))
    assert cls.posture == "NON_CRITICAL" and cls.floor() == FLOOR["NON_CRITICAL"]


@pytest.mark.parametrize("drift", [0.0, 0.15, 0.1501, 0.4])
def test_usa_drift_limit(drift):
    cls = usa.classify(eu_ai_act.AIContext(sector="energy"))
    g = usa.usa_gates(cls, confidence=0.99, explainable=True, explanation="e", drift_score=drift,
                      genai=False, provenance="p", action_is_ot=False, action_destructive=False,
                      prohibited=False, prohibited_reason="")
    assert any(x.gate == "usa.robustness" for x in g) == (drift > 0.15)


@pytest.mark.parametrize("provenance,explanation,explainable,denied", [
    ("cces://x", "e", True, False), ("", "e", True, True), ("cces://x", "", True, True),
    ("cces://x", "e", False, True)])
def test_usa_generative_ai_provenance(provenance, explanation, explainable, denied):
    cls = usa.classify(eu_ai_act.AIContext(sector="healthcare"))
    g = usa.usa_gates(cls, confidence=0.99, explainable=explainable, explanation=explanation,
                      drift_score=0.0, genai=True, provenance=provenance, action_is_ot=False,
                      action_destructive=False, prohibited=False, prohibited_reason="")
    assert any(x.gate == "usa.nist_ai_600_1" and x.decision == Decision.DENY for x in g) == denied


# ==========================================================================
# 12. Governed path end to end, both jurisdictions                 ~40 cases
# ==========================================================================
@pytest.mark.parametrize("key", sorted(NSM22))
def test_usa_critical_sector_always_needs_a_human(engine, key):
    out = GovernedAgent(engine).govern(proposal(juris="USA", sector=key, conf=0.99))
    assert out["status"] == "PENDING_APPROVAL"


@pytest.mark.parametrize("key", sorted(NSM22))
def test_usa_below_floor_is_blocked_and_never_pending(engine, key):
    conf = round(FLOOR[NSM22[key][1]] - 0.01, 4)
    out = GovernedAgent(engine).govern(proposal(juris="USA", sector=key, conf=conf))
    assert out["status"] == "BLOCKED"
    assert engine.status()["pending_approvals"] == []


@pytest.mark.parametrize("ctx,status", [
    ({"prohibited_practice": True, "prohibited_reason": "social scoring"}, "BLOCKED"),
    ({"sector": "energy", "safety_component": True}, "PENDING_APPROVAL"),
    ({"biometric": True}, "PENDING_APPROVAL"),
    ({}, "EXECUTED"),
])
def test_eu_governed_outcomes(engine, ctx, status):
    assert GovernedAgent(engine).govern(proposal(juris="EU", **ctx))["status"] == status


@pytest.mark.parametrize("category", ["CONTAINMENT", "ERADICATION", "RECOVERY", "DECEPTION", "HARDENING"])
def test_governed_proposal_respects_state_policy(engine, category):
    out = GovernedAgent(engine).govern(proposal(juris="EU", category=category))   # engine is in MODEL
    assert out["status"] == "BLOCKED"


# ==========================================================================
# 13. Evidence log: tampering, by record  (SGH 8; TAX)             ~25 cases
# ==========================================================================
def _populated(tmp_path, n=8) -> EvidenceLog:
    log = EvidenceLog(str(tmp_path / "ev.jsonl"))
    for i in range(n):
        log.append(f"E{i}", {"i": i, "note": "x"})
    return log


def _lines(log):
    return Path(log.path).read_text(encoding="utf-8").splitlines(keepends=True)


def _write(log, lines):
    Path(log.path).write_text("".join(lines), encoding="utf-8")


def test_clean_log_verifies(tmp_path):
    assert _populated(tmp_path).verify() == (True, None)


@pytest.mark.parametrize("i", range(8))
def test_editing_any_record_is_detected(tmp_path, i):
    log = _populated(tmp_path)
    lines = _lines(log)
    rec = json.loads(lines[i])
    rec["payload"]["note"] = "edited"
    lines[i] = json.dumps(rec, ensure_ascii=False) + "\n"
    _write(log, lines)
    assert log.verify()[0] is False


@pytest.mark.parametrize("i", range(7))
def test_deleting_any_non_final_record_is_detected(tmp_path, i):
    log = _populated(tmp_path)
    lines = _lines(log)
    del lines[i]
    _write(log, lines)
    assert log.verify()[0] is False


@pytest.mark.parametrize("i", range(7))
def test_swapping_adjacent_records_is_detected(tmp_path, i):
    log = _populated(tmp_path)
    lines = _lines(log)
    lines[i], lines[i + 1] = lines[i + 1], lines[i]
    _write(log, lines)
    assert log.verify()[0] is False


@pytest.mark.xfail(strict=True, reason="NEW-06: truncating the last records is not detected "
                                       "(chain head is not signed or anchored)")
@pytest.mark.parametrize("k", [1, 2, 4])
def test_truncating_the_tail_is_detected(tmp_path, k):
    log = _populated(tmp_path)
    _write(log, _lines(log)[:-k])
    assert log.verify()[0] is False


@pytest.mark.xfail(strict=True, reason="T-08 (paper): a writer who rewrites the whole chain produces "
                                       "a log that verifies; needs a signed or anchored head")
def test_rewriting_the_whole_chain_is_detected(tmp_path):
    log = _populated(tmp_path)
    recs = [json.loads(x) for x in _lines(log)]
    forged = EvidenceLog(str(tmp_path / "forged.jsonl"))
    for r in recs:
        forged.append(r["event_type"], {**r["payload"], "note": "rewritten"})
    os.replace(forged.path, log.path)
    assert log.verify()[0] is False


# ==========================================================================
# 14. Telemetry validation  (Architecture 4.2)                     ~14 cases
# ==========================================================================
GOOD_TEL = dict(source="edr", domain="device", confidence=0.9, provenance="p", timestamp=1.0)


@pytest.mark.parametrize("field,value", [
    ("source", ""), ("domain", "weather"), ("domain", ""), ("confidence", -0.01), ("confidence", 1.01),
    ("confidence", "high"), ("provenance", ""), ("timestamp", None)])
def test_invalid_telemetry_is_rejected(field, value):
    assert TelemetryEvent(**{**GOOD_TEL, field: value}).validate() != []


@pytest.mark.parametrize("domain", ["identity", "device", "network", "application", "data", "ai"])
def test_each_valid_domain_is_accepted(domain):
    assert TelemetryEvent(**{**GOOD_TEL, "domain": domain}).validate() == []


# ==========================================================================
# 15. Determinism and interface consistency                        ~20 cases
# ==========================================================================
@pytest.mark.parametrize("name", sorted(p.name for p in EXAMPLES.glob("*.json")
                                        if json.loads(p.read_text(encoding="utf-8")).get("ai")))
def test_governed_examples_are_deterministic(tmp_path, name):
    data = json.loads((EXAMPLES / name).read_text(encoding="utf-8"))
    seen = set()
    for i in range(5):
        eng = CAIEngine(home=str(tmp_path / f"rt{i}"))
        eng.init()
        out = GovernedAgent(eng).govern(data)
        seen.add((out["status"], out["decision"], out["requires_human_approval"]))
    assert len(seen) == 1


def _cli(home, *args):
    return subprocess.run([sys.executable, "-m", "cai_engine", "--home", str(home), *args],
                          cwd=str(IMPL), capture_output=True, text=True, timeout=60)


@pytest.mark.parametrize("args", [("status",), ("verify",), ("report",),
                                  ("govern", str(EXAMPLES / "ai_minimal.json")),
                                  ("govern", str(EXAMPLES / "ai_prohibited.json"))])
def test_cli_commands_run(tmp_path, args):
    assert _cli(tmp_path, "init").returncode == 0
    res = _cli(tmp_path, *args)
    assert res.returncode == 0, res.stderr


def test_cli_and_api_agree(tmp_path):
    _cli(tmp_path / "cli", "init")
    res = _cli(tmp_path / "cli", "govern", str(EXAMPLES / "ai_highrisk_energy.json"))
    eng = CAIEngine(home=str(tmp_path / "api"))
    eng.init()
    api = GovernedAgent(eng).govern(json.loads((EXAMPLES / "ai_highrisk_energy.json").read_text(encoding="utf-8")))
    assert api["status"] in res.stdout


def test_mcp_exposes_no_approval_tool(monkeypatch, tmp_path):
    pytest.importorskip("mcp")
    monkeypatch.setenv("CAI_HOME", str(tmp_path / "rt"))
    import importlib
    m = importlib.import_module("cai_engine.mcp_server")
    names = {n for n in dir(m) if n.startswith("cai_")}
    assert names and not any(w in n for n in names for w in ("approve", "deny", "transition", "set_fact"))


# ==========================================================================
# 16. Known gaps against the specifications (xfail, strict)
# ==========================================================================
@pytest.mark.xfail(strict=True, reason="T-09 / NEW-05: approve() executes a pending action without "
                                       "re-evaluating it in the current state (TAX 8.6)")
def test_approval_revalidates_after_state_change(engine):
    drive(engine, S.ISOLATE)
    out = engine.propose({"category": "CONTAINMENT", "description": "isolate host", "target": "h"})
    assert out["status"] == "PENDING_APPROVAL"
    assert engine.transition("EVICT")["status"] == "OK"
    res = engine.approve(out["action_id"], "operator")
    assert res["status"] != "EXECUTED"


@pytest.mark.xfail(strict=True, reason="F-02: a NaN confidence passes every '<' threshold comparison")
@pytest.mark.parametrize("juris", ["EU", "USA"])
def test_nan_confidence_is_never_authorized(engine, juris):
    out = GovernedAgent(engine).govern(proposal(juris=juris, conf=math.nan))
    assert out["status"] != "EXECUTED"


@pytest.mark.xfail(strict=True, reason="F-01: risk context is supplied by the AI; omitting the sector "
                                       "of an OT target removes the human-oversight requirement")
def test_omitting_sector_does_not_remove_oversight(engine):
    p = proposal(juris="USA", sector="", conf=0.99)
    p["action"].update(target="substation-relay-7", ot_level=0)
    assert GovernedAgent(engine).govern(p)["status"] != "EXECUTED"


@pytest.mark.xfail(strict=True, reason="JUR: an unknown jurisdiction is silently evaluated as EU "
                                       "instead of being rejected")
def test_unknown_jurisdiction_is_rejected(engine):
    with pytest.raises((EngineError, ValueError)):
        GovernedAgent(engine).govern(proposal(juris="MX"))


@pytest.mark.xfail(strict=True, reason="F-02b: a boolean is accepted as a confidence (True -> 1.0)")
def test_boolean_confidence_is_rejected(engine):
    with pytest.raises((EngineError, ValueError, TypeError)):
        GovernedAgent(engine).govern(proposal(juris="EU", conf=True))


@pytest.mark.xfail(strict=True, reason="F-03: init() truncates an existing evidence log")
def test_init_preserves_existing_evidence(engine):
    engine.set_fact("assets_discovered", True)
    before = engine.evidence.count()
    try:
        engine.init()
    except EngineError:
        pass
    assert engine.evidence.count() >= before


@pytest.mark.xfail(strict=True, reason="SGH 5.2: approval timeout is specified but not implemented")
def test_pending_approval_expires(engine):
    drive(engine, S.ISOLATE)
    out = engine.propose({"category": "CONTAINMENT", "description": "x", "target": "h"})
    st = json.loads(Path(engine.state_path).read_text(encoding="utf-8"))
    assert any(k in json.dumps(st["pending"][out["action_id"]]) for k in ("expires", "deadline", "ttl"))


@pytest.mark.xfail(strict=True, reason="AUD-07 / TAX 8.5: accepted telemetry does not enter any decision "
                                       "(ESA is not consumed); stale telemetry is accepted")
def test_stale_telemetry_is_rejected(engine):
    out = engine.ingest({**GOOD_TEL, "timestamp": 0.0})      # 1 January 1970
    assert out["accepted"] is False
