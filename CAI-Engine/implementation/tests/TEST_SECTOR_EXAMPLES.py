"""Worked sector examples used by docs/USA/sector-frameworks.

Each file in examples/sectors/ holds a synthetic AI proposal, the lifecycle
state in which it is evaluated and the outcome the engine produces. The sector
framework documents quote these outcomes; this test keeps the documents and
the engine in agreement. If the engine changes an outcome, this test fails
until the example and the document that cites it are updated in the same
change.
"""
from __future__ import annotations

import json
import pathlib

import pytest

from cai_engine.engine import CAIEngine
from cai_engine.governed_agent import GovernedAgent
from cai_engine.usa_sectors import SECTORS

HERE = pathlib.Path(__file__).resolve()
EXAMPLES = sorted((HERE.parent.parent / "examples" / "sectors").glob("*.json"))
DOCS = HERE.parents[3] / "docs" / "USA" / "sector-frameworks"
PATH = {
    "MODEL": [],
    "HARDEN": ["HARDEN"],
    "DETECT": ["HARDEN", "DETECT"],
    "ISOLATE": ["HARDEN", "DETECT", "ISOLATE"],
}
FACTS = ["assets_discovered", "telemetry_validated", "baseline_hardened", "telemetry_active",
         "detection_confirmed"]


def _value(decision) -> str:
    return str(getattr(decision, "value", decision))


SECTOR_DOCS = {
    "chemical": "CAI-USA-Chemical-Framework-Application.md",
    "commercial_facilities": "CAI-USA-Commercial-Facilities-Framework-Application.md",
    "communications": "CAI-USA-Communications-Framework-Application.md",
    "critical_manufacturing": "CAI-USA-Critical-Manufacturing-Framework-Application.md",
    "dams": "CAI-USA-Dams-Framework-Application.md",
    "defense_industrial_base": "CAI-USA-Defense-Industrial-Base-Framework-Application.md",
    "emergency_services": "CAI-USA-Emergency-Services-Framework-Application.md",
    "energy": "CAI-USA-Energy-Framework-Application.md",
    "financial_services": "CAI-USA-Financial-Services-Framework-Application.md",
    "food_agriculture": "CAI-USA-Food-and-Agriculture-Framework-Application.md",
    "government_facilities": "CAI-USA-Government-Facilities-Framework-Application.md",
    "healthcare": "CAI-USA-Healthcare-Framework-Application.md",
    "information_technology": "CAI-USA-Information-Technology-Framework-Application.md",
    "nuclear": "CAI-USA-Nuclear-Framework-Application.md",
    "transportation": "CAI-USA-Transportation-Framework-Application.md",
    "water": "CAI-USA-Water-Framework-Application.md",
}


def test_examples_exist():
    """Require two illustrative fixtures and one profile document per NSM-22 key."""
    counts = dict.fromkeys(SECTORS, 0)
    for path in EXAMPLES:
        ex = json.loads(path.read_text(encoding="utf-8"))
        key = ex["proposal"]["context"].get("sector")
        assert key in counts, (path.name, key)
        counts[key] += 1
    assert counts == dict.fromkeys(SECTORS, 2)
    assert set(SECTOR_DOCS) == set(SECTORS)
    assert {p.name for p in DOCS.glob("CAI-USA-*-Framework-Application.md")} == set(SECTOR_DOCS.values())


@pytest.mark.parametrize("path", EXAMPLES, ids=[p.stem for p in EXAMPLES])
def test_sector_example_outcome(path, tmp_path):
    ex = json.loads(path.read_text(encoding="utf-8"))
    engine = CAIEngine(str(tmp_path / "rt"))
    engine.init()
    for fact in FACTS:
        engine.set_fact(fact, True)
    for state in PATH[ex["lifecycle_state"]]:
        assert engine.transition(state)["status"] == "OK"
    result = GovernedAgent(engine).govern(ex["proposal"])
    gates = [[g["gate"], _value(g["decision"])]
             for g in result["regulatory"]["gate_results"] + result["cai_engine"]["gate_results"]]
    assert result["status"] == ex["expected"]["status"]
    assert result["decision"] == ex["expected"]["decision"]
    assert gates == ex["expected"]["gates"]
    assert engine.verify()["integrity_ok"]


def test_documents_quote_the_example_outcomes():
    """Every example is cited by exactly one sector document, with its state, outcome and gates."""
    rows = {}
    for doc in sorted(DOCS.glob("CAI-USA-*-Framework-Application.md")):
        for line in doc.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0].startswith("`") and cells[0].endswith(".json`"):
                rows.setdefault(cells[0].strip("`"), []).append((doc.name, cells))
    for path in EXAMPLES:
        ex = json.loads(path.read_text(encoding="utf-8"))
        found = rows.get(path.name, [])
        assert len(found) == 1, (path.name, [d for d, _ in found])
        _, cells = found[0]
        assert cells[4] == f"{ex['expected']['status']} ({ex['expected']['decision']})", (path.name, cells[4])
        assert cells[2] == ex["lifecycle_state"], path.name
        not_allowed = "; ".join(f"{g} = {d}" for g, d in ex["expected"]["gates"] if d != "ALLOW")
        assert cells[5] == not_allowed, (path.name, cells[5])
