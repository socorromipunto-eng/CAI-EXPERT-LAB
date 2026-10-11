"""USA governance profile — sector-aware (CAI-USA baseline).

Aligns to the U.S. stack rather than the EU AI Act:
  - NIST AI RMF 1.0 (GOVERN / MAP / MEASURE / MANAGE)
  - NIST AI 600-1 Generative AI Profile (for generative AI)
  - NSM-22 critical-infrastructure sectors + their SRMA, treated per sector
  - OT/ICS safety gating for cyber-physical sectors

Each sector is treated on its own terms: the assurance strictness scales with
the sector's consequence level, SRMA oversight applies to critical-infrastructure
sectors, and OT safety gating applies to OT-intensive sectors.

Alignment, not compliance: this maps to and enforces proportionate governance;
it does not assert conformity with any U.S. statute, rule, or SRMA directive.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .eu_ai_act import AIContext
from .gates import Decision, GateResult
from .usa_sectors import resolve, Sector


# Minimum AI confidence by sector consequence (NIST AI RMF MEASURE / robustness).
CONFIDENCE_FLOOR = {
    "CATASTROPHIC": 0.95,
    "HIGH": 0.90,
    "MODERATE": 0.80,
    "NON_CRITICAL": 0.70,
}
MAX_DRIFT = 0.15


@dataclass
class USAClassification:
    posture: str                      # CRITICAL_INFRASTRUCTURE | NON_CRITICAL
    sector_key: str
    sector_name: str
    srma: str
    consequence: str
    ot_intensive: bool
    references: list[str] = field(default_factory=list)

    def floor(self) -> float:
        key = self.consequence if self.posture == "CRITICAL_INFRASTRUCTURE" else "NON_CRITICAL"
        return CONFIDENCE_FLOOR[key]


def classify(ctx: AIContext) -> USAClassification:
    sector: Sector | None = resolve(ctx.sector)
    refs = ["NIST AI RMF 1.0"]
    if sector is None:
        return USAClassification("NON_CRITICAL", "", ctx.sector or "unspecified",
                                  "n/a", "MODERATE", False, refs)
    refs.append(f"NSM-22 sector: {sector.name} (SRMA: {sector.srma})")
    return USAClassification(
        "CRITICAL_INFRASTRUCTURE", sector.key, sector.name, sector.srma,
        sector.consequence, sector.ot_intensive, refs)


def usa_gates(cls: USAClassification, *, confidence: float, explainable: bool,
              explanation: str, drift_score: float, genai: bool, provenance: str,
              action_is_ot: bool, action_destructive: bool,
              prohibited: bool, prohibited_reason: str) -> list[GateResult]:
    g: list[GateResult] = []

    # Unlawful / prohibited use — denied outright.
    if prohibited:
        g.append(GateResult("usa.unlawful_use", Decision.DENY,
                            prohibited_reason or "use designated unlawful/prohibited"))
        return g

    # NIST AI RMF — always exercised (informational).
    g.append(GateResult("usa.nist_ai_rmf", Decision.ALLOW,
                        "governed under NIST AI RMF (Govern/Map/Measure/Manage)"))

    # NIST AI 600-1 — Generative AI provenance & transparency.
    if genai:
        if not provenance.strip() or not explanation.strip() or not explainable:
            g.append(GateResult("usa.nist_ai_600_1", Decision.DENY,
                                "generative AI without provenance/explanation (NIST AI 600-1)"))
        else:
            g.append(GateResult("usa.nist_ai_600_1", Decision.ALLOW,
                                "generative AI provenance and explanation present"))

    if cls.posture == "CRITICAL_INFRASTRUCTURE":
        # SRMA oversight — human oversight for critical-infrastructure decisions.
        g.append(GateResult("usa.srma_oversight", Decision.ESCALATE,
                            f"{cls.sector_name}: human oversight under SRMA {cls.srma}"))
        # Accuracy/robustness floor scaled by sector consequence.
        floor = cls.floor()
        if confidence < floor:
            g.append(GateResult("usa.assurance_floor", Decision.DENY,
                                f"confidence {confidence:.2f} < {cls.consequence} floor {floor:.2f}"))
        if drift_score > MAX_DRIFT:
            g.append(GateResult("usa.robustness", Decision.DENY,
                                f"model drift {drift_score:.2f} > maximum {MAX_DRIFT:.2f}"))
        # OT/ICS safety gating for cyber-physical sectors.
        if cls.ot_intensive and (action_is_ot or action_destructive):
            g.append(GateResult("usa.ot_ics_safety", Decision.ESCALATE,
                                f"{cls.sector_name} is OT-intensive: cyber-physical safety approval required"))
    else:
        floor = cls.floor()
        if confidence < floor:
            g.append(GateResult("usa.assurance_floor", Decision.DENY,
                                f"confidence {confidence:.2f} < non-critical floor {floor:.2f}"))

    return g
