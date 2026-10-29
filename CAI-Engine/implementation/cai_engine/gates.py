"""Guards: policy evaluation, safety gating and human oversight.

Order of authority (Safety-Gates.md section 3 and Architecture.md section 5):
    Policy Evaluation  ->  Safety Gates  ->  Human Oversight
Policies constrain what is permissible; they never trigger actions.
Safety gates are AUTHORITATIVE and override policy and automation.
Human authority is final and cannot be delegated to AI or automation.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass

from .core import ALLOWED_ACTIONS, Action, ActionCategory, State


class Decision(str, enum.Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE"   # permitted only with human approval


@dataclass
class GateResult:
    gate: str
    decision: Decision
    reason: str


# Thresholds (conservative defaults; configurable per deployment).
BLAST_RADIUS_ESCALATE = 25          # assets in scope above this -> human approval
AI_MIN_CONFIDENCE = 0.80            # below this, AI output cannot trigger action
OT_SENSITIVE_MAX_LEVEL = 2          # Purdue levels 0-2 are safety-critical


# --------------------------------------------------------------------------
# Policy Evaluation Layer  (Architecture.md 4.3)
# --------------------------------------------------------------------------
def policy_evaluate(action: Action, state: State) -> GateResult:
    cat = action.normalized_category()
    permitted = ALLOWED_ACTIONS.get(state, set())
    if cat not in permitted:
        return GateResult(
            "policy.state_constraint",
            Decision.DENY,
            f"action category {cat.value} is not permitted in state {state.value} "
            f"(permitted: {sorted(c.value for c in permitted)})",
        )
    return GateResult("policy.state_constraint", Decision.ALLOW, "action permitted by state constraints")


# --------------------------------------------------------------------------
# Safety Gating Layer  (Safety-Gates.md section 4) — authoritative
# --------------------------------------------------------------------------
def safety_gates(action: Action) -> list[GateResult]:
    results: list[GateResult] = []
    errors = action.validate()
    if errors:
        return [GateResult("safety.input_validation", Decision.DENY, "; ".join(errors))]

    # 4.4 AI Confidence and Explainability — checked first: low-confidence or
    # non-explainable AI output cannot trigger any action.
    if action.ai_assisted:
        if action.ai_confidence < AI_MIN_CONFIDENCE:
            results.append(GateResult(
                "safety.ai_confidence", Decision.DENY,
                f"AI confidence {action.ai_confidence:.2f} < minimum {AI_MIN_CONFIDENCE:.2f}"))
        if not action.ai_explainable:
            results.append(GateResult(
                "safety.ai_explainability", Decision.DENY,
                "AI output is not explainable; cannot trigger action"))

    # 4.2 OT/ICS Safety Gates — Level 0-2 assets are non-bypassable.
    if action.ot_level is not None and action.ot_level <= OT_SENSITIVE_MAX_LEVEL:
        cat = action.normalized_category()
        if cat in (ActionCategory.CONTAINMENT, ActionCategory.ERADICATION) or action.destructive:
            results.append(GateResult(
                "safety.ot_ics", Decision.ESCALATE,
                f"OT/ICS asset at Purdue level {action.ot_level}: human approval required "
                f"(no uncontrolled isolation/modification of level 0-2)"))

    # 4.1 Operational Impact — destructive actions are never silent.
    if action.destructive:
        results.append(GateResult(
            "safety.operational_impact", Decision.ESCALATE,
            "destructive action: human approval required before execution"))

    # 4.3 Blast Radius Control.
    if action.blast_radius > BLAST_RADIUS_ESCALATE:
        results.append(GateResult(
            "safety.blast_radius", Decision.ESCALATE,
            f"blast radius {action.blast_radius} assets > threshold {BLAST_RADIUS_ESCALATE}"))

    if not results:
        results.append(GateResult("safety.none_triggered", Decision.ALLOW, "no safety gate triggered"))
    return results


# --------------------------------------------------------------------------
# Human Oversight Model  (Safety-Gates.md section 5)
# --------------------------------------------------------------------------
def requires_human_approval(action: Action, state: State, gate_results: list[GateResult]) -> bool:
    """Mandatory human approval scenarios (section 5.1) plus any ESCALATE gate."""
    if any(g.decision == Decision.ESCALATE for g in gate_results):
        return True
    if state == State.EVICT:                       # eviction is always safety-gated + human
        return True
    if action.affects_privileged_accounts:         # privileged credential impact
        return True
    cat = action.normalized_category()
    return cat in (ActionCategory.CONTAINMENT, ActionCategory.RECOVERY)


def summarize(gate_results: list[GateResult]) -> Decision:
    """Combine gate results into one decision. DENY wins, then ESCALATE."""
    if any(g.decision == Decision.DENY for g in gate_results):
        return Decision.DENY
    if any(g.decision == Decision.ESCALATE for g in gate_results):
        return Decision.ESCALATE
    return Decision.ALLOW
