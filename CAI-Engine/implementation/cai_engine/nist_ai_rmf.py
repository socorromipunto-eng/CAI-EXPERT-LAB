"""NIST AI RMF 1.0 traceability mapping.

For each governed decision, record which of the four NIST AI RMF functions
were exercised, so the evidence log is traceable to both EU AI Act articles
and NIST AI RMF functions (GOVERN, MAP, MEASURE, MANAGE).
"""
from __future__ import annotations


def rmf_trace(classification: str, confidence: float, drift_score: float,
              explainable: bool, needs_human: bool, final_decision: str,
              framework: str = "") -> dict:
    where = f" under {framework}" if framework else ""
    return {
        "GOVERN": "policy, safety and human-authority constraints enforced by the engine",
        "MAP": f"deployment context classified{where} (classification = {classification})",
        "MEASURE": (f"confidence={confidence:.2f}, drift={drift_score:.2f}, "
                    f"explainable={explainable}"),
        "MANAGE": (f"decision={final_decision}; "
                   f"human_oversight={'required' if needs_human else 'not required'}; "
                   f"recorded in immutable evidence log"),
    }
