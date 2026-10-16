"""EU AI Act alignment layer.

Instrument: Regulation (EU) 2024/1689, as amended by the Digital Omnibus
(Regulation (EU) 2026/1744, in force 27 July 2026). The amendment changes
application dates and scope (high-risk Annex III deferred to 2 Dec 2027) and
adds two Art. 5 prohibitions (non-consensual intimate imagery; CSAM); the
article obligations this module enforces are unchanged. See REGULATORY-BASIS.md.


This module classifies an AI-assisted decision into the Act's risk tiers and
derives the obligations and enforcement that apply. It implements the
framework's *alignment* stance: it maps to the Regulation's articles and
enforces proportionate governance; it does NOT assert legal compliance,
conformity assessment, or CE marking — those are determined outside this engine.

Tier model (Regulation (EU) 2024/1689):
  - UNACCEPTABLE  Art. 5         prohibited practices            -> forbidden
  - HIGH          Art. 6 + Annex III                             -> Art. 9-15 obligations
  - LIMITED       Art. 50        transparency obligations
  - MINIMAL       no specific obligations
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field

from .gates import Decision, GateResult


class RiskTier(str, enum.Enum):
    UNACCEPTABLE = "UNACCEPTABLE"
    HIGH = "HIGH"
    LIMITED = "LIMITED"
    MINIMAL = "MINIMAL"


# Obligations for high-risk systems, mapped to the Act's articles.
HIGH_RISK_OBLIGATIONS: dict[str, str] = {
    "Art.9": "Risk management system",
    "Art.10": "Data and data governance",
    "Art.11": "Technical documentation",
    "Art.12": "Record-keeping (automatic event logging)",
    "Art.13": "Transparency and information to deployers",
    "Art.14": "Human oversight",
    "Art.15": "Accuracy, robustness and cybersecurity",
}

# Annex III high-risk areas relevant to a cybersecurity AI operating on
# critical systems. (Subset — the full Annex III has eight areas.)
ANNEX_III = {
    "biometrics": "Annex III(1) — Biometrics",
    "critical_infrastructure": "Annex III(2) — Critical infrastructure (safety components)",
    "essential_services": "Annex III(5) — Access to essential private and public services",
    "law_enforcement": "Annex III(6) — Law enforcement",
}

# Sectors treated as critical infrastructure for Annex III(2).
CRITICAL_SECTORS = {
    "energy", "electricity", "gas", "water", "heating",
    "transport", "road_traffic", "communications", "digital_infrastructure",
    "healthcare", "banking", "financial_market",
}

# Enforcement thresholds, proportionate to tier (Art. 15 accuracy/robustness).
HIGH_MIN_CONFIDENCE = 0.90
LIMITED_MIN_CONFIDENCE = 0.70
MAX_DRIFT = 0.15


@dataclass
class AIContext:
    """Deployment context of the AI-assisted decision (what the Act classifies)."""
    sector: str = ""
    safety_component: bool = False          # safety component of the above sector
    biometric: bool = False
    affects_essential_services: bool = False
    law_enforcement: bool = False
    interacts_with_persons: bool = False    # Art. 50 transparency
    generates_content: bool = False         # Art. 50 transparency (synthetic content)
    prohibited_practice: bool = False       # Art. 5
    prohibited_reason: str = ""

    def is_critical_infrastructure(self) -> bool:
        return self.sector.lower() in CRITICAL_SECTORS


@dataclass
class Classification:
    tier: RiskTier
    rationale: str
    annex_refs: list[str] = field(default_factory=list)
    obligations: dict[str, str] = field(default_factory=dict)


def classify(ctx: AIContext) -> Classification:
    """Classify the AI-assisted decision into an EU AI Act risk tier."""
    if ctx.prohibited_practice:
        return Classification(
            RiskTier.UNACCEPTABLE,
            f"Art. 5 prohibited practice: {ctx.prohibited_reason or 'unspecified'}",
            ["Art.5"], {})

    annex: list[str] = []
    if ctx.biometric:
        annex.append(ANNEX_III["biometrics"])
    if ctx.is_critical_infrastructure() and ctx.safety_component:
        annex.append(ANNEX_III["critical_infrastructure"])
    if ctx.affects_essential_services:
        annex.append(ANNEX_III["essential_services"])
    if ctx.law_enforcement:
        annex.append(ANNEX_III["law_enforcement"])

    if annex:
        return Classification(
            RiskTier.HIGH,
            "High-risk under Art. 6 and " + "; ".join(annex),
            annex, dict(HIGH_RISK_OBLIGATIONS))

    if ctx.interacts_with_persons or ctx.generates_content:
        return Classification(
            RiskTier.LIMITED,
            "Limited risk — Art. 50 transparency obligations apply",
            [], {"Art.50": "Transparency obligations"})

    return Classification(RiskTier.MINIMAL, "Minimal risk — no specific obligations", [], {})


def eu_gates(cls: Classification, *, confidence: float, explainable: bool,
             explanation: str, drift_score: float, human_disclosed: bool) -> list[GateResult]:
    """Return EU-AI-Act gate results for the classified decision."""
    g: list[GateResult] = []

    if cls.tier == RiskTier.UNACCEPTABLE:
        g.append(GateResult("eu.art5_prohibited", Decision.DENY, cls.rationale))
        return g

    if cls.tier == RiskTier.HIGH:
        # Art. 14 — human oversight is mandatory for high-risk systems.
        g.append(GateResult("eu.art14_human_oversight", Decision.ESCALATE,
                            "high-risk: human oversight required (Art. 14)"))
        # Art. 15 — accuracy & robustness.
        if confidence < HIGH_MIN_CONFIDENCE:
            g.append(GateResult("eu.art15_accuracy", Decision.DENY,
                                f"confidence {confidence:.2f} < high-risk minimum {HIGH_MIN_CONFIDENCE:.2f}"))
        if drift_score > MAX_DRIFT:
            g.append(GateResult("eu.art15_robustness", Decision.DENY,
                                f"model drift {drift_score:.2f} > maximum {MAX_DRIFT:.2f}"))
        # Art. 13 — transparency / explainability to the deployer.
        if not explainable or not explanation.strip():
            g.append(GateResult("eu.art13_transparency", Decision.DENY,
                                "high-risk decision lacks an explanation (Art. 13)"))
        # Art. 12 — record-keeping is satisfied by the evidence log.
        g.append(GateResult("eu.art12_record_keeping", Decision.ALLOW,
                            "decision recorded in hash-chained evidence log (Art. 12)"))
        return g

    if cls.tier == RiskTier.LIMITED:
        if not human_disclosed:
            g.append(GateResult("eu.art50_transparency", Decision.ESCALATE,
                                "limited risk: AI interaction/content must be disclosed (Art. 50)"))
        if confidence < LIMITED_MIN_CONFIDENCE:
            g.append(GateResult("eu.art50_quality", Decision.DENY,
                                f"confidence {confidence:.2f} < minimum {LIMITED_MIN_CONFIDENCE:.2f}"))
        if not g:
            g.append(GateResult("eu.art50_transparency", Decision.ALLOW, "transparency satisfied"))
        return g

    g.append(GateResult("eu.minimal_risk", Decision.ALLOW, "minimal risk — no EU gate triggered"))
    return g
