"""Governed-agent layer — the point of the CAI Engine for AI.

An AI system (an LLM, an analytics model, an agent) does not act directly.
It submits a *proposal*: a recommended action plus its confidence,
explanation, provenance, drift indicator, deployment context and the
jurisdiction it operates under. The GovernedAgent runs that proposal through
two layers before anything happens:

    1. Regulatory layer — selected by jurisdiction:
         EU  -> EU AI Act (Regulation (EU) 2024/1689): risk tiers + article gates
         USA -> CAI-USA baseline: NIST AI RMF + NIST AI 600-1 + NSM-22 sectors,
                treated per critical-infrastructure sector (SRMA, consequence, OT)
    2. CAI Engine layer — state constraints, safety gates, human oversight.

The FINAL decision is the strictest of the layers (DENY wins, then ESCALATE to
human). AI is advisory only: it can never bypass a gate or force a transition,
and a high-consequence / high-risk decision always requires a human. Every
governed decision is written to the hash-chained evidence log with full
regulatory traceability.
"""
from __future__ import annotations

import uuid

from . import eu_ai_act, usa
from .core import ActionCategory
from .engine import CAIEngine
from .eu_ai_act import AIContext
from .gates import Decision, GateResult
from .nist_ai_rmf import rmf_trace


def _gate_dicts(results: list[GateResult]) -> list[dict]:
    return [{"gate": g.gate, "decision": g.decision.value, "reason": g.reason} for g in results]


def _combine(reg_results: list[GateResult], cai_decision: str, cai_needs_human: bool) -> tuple[str, bool]:
    decisions = [g.decision.value for g in reg_results] + [cai_decision]
    if Decision.DENY.value in decisions:
        final = Decision.DENY.value
    elif Decision.ESCALATE.value in decisions:
        final = Decision.ESCALATE.value
    else:
        final = Decision.ALLOW.value
    needs_human = cai_needs_human or any(g.decision == Decision.ESCALATE for g in reg_results)
    return final, needs_human


class GovernedAgent:
    def __init__(self, engine: CAIEngine, default_jurisdiction: str = "EU"):
        self.engine = engine
        self.default_jurisdiction = default_jurisdiction.upper()

    def _regulatory(self, jurisdiction: str, ctx: AIContext, ai: dict, action) -> tuple[dict, list[GateResult], bool]:
        """Return (regulatory_block, gate_results, force_human)."""
        confidence = float(ai.get("confidence", 0.0))
        explanation = str(ai.get("explanation", ""))
        explainable = bool(ai.get("explainable", bool(explanation.strip())))
        drift = float(ai.get("drift_score", 0.0))

        if jurisdiction == "USA":
            cls = usa.classify(ctx)
            action_is_ot = action.ot_level is not None
            action_destructive = action.destructive or action.normalized_category() in (
                ActionCategory.CONTAINMENT, ActionCategory.ERADICATION)
            results = usa.usa_gates(
                cls, confidence=confidence, explainable=explainable, explanation=explanation,
                drift_score=drift, genai=bool(ai.get("genai", ctx.generates_content)),
                provenance=str(ai.get("provenance", "")),
                action_is_ot=action_is_ot, action_destructive=action_destructive,
                prohibited=ctx.prohibited_practice, prohibited_reason=ctx.prohibited_reason)
            block = {
                "framework": "CAI-USA (NIST AI RMF / NIST AI 600-1 / NSM-22)",
                "jurisdiction": "USA",
                "label": cls.posture,
                "sector": cls.sector_name,
                "srma": cls.srma,
                "consequence": cls.consequence,
                "ot_intensive": cls.ot_intensive,
                "references": cls.references,
                "gate_results": _gate_dicts(results),
            }
            force_human = cls.posture == "CRITICAL_INFRASTRUCTURE"
            return block, results, force_human

        # default: EU
        cls = eu_ai_act.classify(ctx)
        results = eu_ai_act.eu_gates(
            cls, confidence=confidence, explainable=explainable, explanation=explanation,
            drift_score=drift, human_disclosed=bool(ai.get("human_disclosed", False)))
        block = {
            "framework": "EU AI Act (Reg. (EU) 2024/1689, amended by Digital Omnibus (EU) 2026/1744)",
            "jurisdiction": "EU",
            "label": cls.tier.value,
            "rationale": cls.rationale,
            "annex_refs": cls.annex_refs,
            "obligations": cls.obligations,
            "gate_results": _gate_dicts(results),
        }
        force_human = cls.tier == eu_ai_act.RiskTier.HIGH
        return block, results, force_human

    def govern(self, proposal: dict, jurisdiction: str | None = None) -> dict:
        ai = proposal.get("ai", {})
        juris = (jurisdiction or proposal.get("jurisdiction") or self.default_jurisdiction).upper()
        ctx = AIContext(**proposal.get("context", {}))

        action_data = dict(proposal.get("action", {}))
        action_data.update({
            "ai_assisted": True,
            "ai_confidence": float(ai.get("confidence", 0.0)),
            "ai_explainable": bool(ai.get("explainable", bool(str(ai.get("explanation", "")).strip()))),
        })
        action = self.engine._build_action(action_data)

        reg_block, reg_results, force_human = self._regulatory(juris, ctx, ai, action)

        cai = self.engine.evaluate(action)
        final_decision, needs_human = _combine(reg_results, cai["decision"], cai["requires_human_approval"])
        if force_human and final_decision != Decision.DENY.value:
            needs_human = True

        decision_id = "gov-" + uuid.uuid4().hex[:10]
        record = {
            "decision_id": decision_id,
            "jurisdiction": juris,
            "ai_system": ai.get("system", "unknown"),
            "model_version": ai.get("model_version", "unknown"),
            "regulatory": reg_block,
            "cai_engine": {
                "state": cai["state"],
                "gate_results": cai["gate_results"],
                "decision": cai["decision"],
            },
            "nist_ai_rmf": rmf_trace(reg_block["label"], float(ai.get("confidence", 0.0)),
                                     float(ai.get("drift_score", 0.0)),
                                     action.ai_explainable, needs_human, final_decision,
                                     framework=reg_block.get("framework", "")),
            "action": cai["action"],
            "decision": final_decision,
            "requires_human_approval": needs_human,
        }

        return self.engine.commit(
            decision_id, record,
            blocked_event="GOVERNED_DECISION_BLOCKED",
            pending_event="GOVERNED_DECISION_PENDING_APPROVAL",
            executed_event="GOVERNED_DECISION_EXECUTED")
