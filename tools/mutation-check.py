"""Targeted mutation check for CAI-Engine: does a test suite notice when a rule is broken?

Part of CAI-EXPERT-LAB (owner: Antonio José Socorro Marín).

Each mutant changes one rule of cai_engine in a throw-away copy. A mutant is
"killed" when the suite reports at least one failure. Usage:
    python tools/mutation-check.py CAI-Engine/implementation tests/TEST_SPECIFICATION_MATRIX.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(sys.argv[1])
TESTS = sys.argv[2:]

MUTANTS = [
    ("gates: AI confidence '<' -> '<='", "gates.py", "action.ai_confidence < AI_MIN_CONFIDENCE", "action.ai_confidence <= AI_MIN_CONFIDENCE"),
    ("gates: AI floor 0.80 -> 0.75", "gates.py", "AI_MIN_CONFIDENCE = 0.80", "AI_MIN_CONFIDENCE = 0.75"),
    ("gates: explainability gate removed", "gates.py", "if not action.ai_explainable:", "if False:"),
    ("gates: OT level '<=' -> '<'", "gates.py", "action.ot_level <= OT_SENSITIVE_MAX_LEVEL", "action.ot_level < OT_SENSITIVE_MAX_LEVEL"),
    ("gates: OT gate ignores destructive", "gates.py", "or action.destructive:\n            results.append(GateResult(\n                \"safety.ot_ics\"", ":\n            results.append(GateResult(\n                \"safety.ot_ics\""),
    ("gates: blast radius '>' -> '>='", "gates.py", "action.blast_radius > BLAST_RADIUS_ESCALATE", "action.blast_radius >= BLAST_RADIUS_ESCALATE"),
    ("gates: EVICT no longer needs a human", "gates.py", "if state == State.EVICT:", "if False:"),
    ("gates: privileged accounts no longer need a human", "gates.py", "if action.affects_privileged_accounts:", "if False:"),
    ("gates: RECOVERY no longer needs a human", "gates.py", "(ActionCategory.CONTAINMENT, ActionCategory.RECOVERY)", "(ActionCategory.CONTAINMENT,)"),
    ("gates: ESCALATE beats DENY", "gates.py", "    if any(g.decision == Decision.DENY for g in gate_results):\n        return Decision.DENY\n    if any(g.decision == Decision.ESCALATE for g in gate_results):\n        return Decision.ESCALATE", "    if any(g.decision == Decision.ESCALATE for g in gate_results):\n        return Decision.ESCALATE\n    if any(g.decision == Decision.DENY for g in gate_results):\n        return Decision.DENY"),
    ("core: DETECT permits CONTAINMENT", "core.py", "State.DETECT: {ActionCategory.OBSERVE},", "State.DETECT: {ActionCategory.OBSERVE, ActionCategory.CONTAINMENT},"),
    ("core: MODEL permits HARDENING", "core.py", "State.MODEL: {ActionCategory.OBSERVE},", "State.MODEL: {ActionCategory.OBSERVE, ActionCategory.HARDENING},"),
    ("core: extra transition MODEL->DETECT", "core.py", "State.MODEL: [State.HARDEN],", "State.MODEL: [State.HARDEN, State.DETECT],"),
    ("core: EVICT no longer needs safety_approved", "core.py", '["malicious_presence_confirmed", "safety_approved"]', '["malicious_presence_confirmed"]'),
    ("core: telemetry accepts any domain", "core.py", "if self.domain not in VALID_DOMAINS:", "if False:"),
    ("evidence: prev_hash not checked", "evidence.py", 'if body.get("prev_hash") != prev:', "if False:"),
    ("evidence: record hash not checked", "evidence.py", "if _record_hash(body) != stored:", "if False:"),
    ("eu: high-risk floor 0.90 -> 0.89", "eu_ai_act.py", "HIGH_MIN_CONFIDENCE = 0.90", "HIGH_MIN_CONFIDENCE = 0.89"),
    ("eu: drift limit 0.15 -> 0.16", "eu_ai_act.py", "MAX_DRIFT = 0.15", "MAX_DRIFT = 0.16"),
    ("eu: Annex III(2) ignores safety_component", "eu_ai_act.py", "if ctx.is_critical_infrastructure() and ctx.safety_component:", "if ctx.is_critical_infrastructure():"),
    ("eu: Art. 14 oversight no longer escalates", "eu_ai_act.py", 'g.append(GateResult("eu.art14_human_oversight", Decision.ESCALATE,', 'g.append(GateResult("eu.art14_human_oversight", Decision.ALLOW,'),
    ("eu: Art. 50 disclosure ignored", "eu_ai_act.py", "if not human_disclosed:", "if False:"),
    ("usa: CATASTROPHIC floor 0.95 -> 0.94", "usa.py", '"CATASTROPHIC": 0.95,', '"CATASTROPHIC": 0.94,'),
    ("usa: SRMA oversight no longer escalates", "usa.py", 'g.append(GateResult("usa.srma_oversight", Decision.ESCALATE,', 'g.append(GateResult("usa.srma_oversight", Decision.ALLOW,'),
    ("usa: GenAI provenance not required", "usa.py", "if not provenance.strip() or not explanation.strip() or not explainable:", "if not explanation.strip() or not explainable:"),
    ("usa_sectors: energy not OT-intensive", "usa_sectors.py", '"Department of Energy", "CATASTROPHIC", True)', '"Department of Energy", "CATASTROPHIC", False)'),
    ("usa_sectors: water consequence HIGH", "usa_sectors.py", '"Environmental Protection Agency", "CATASTROPHIC", True)', '"Environmental Protection Agency", "HIGH", True)'),
    ("usa_sectors: alias 'aviation' removed", "usa_sectors.py", '"aviation": "transportation", ', ""),
]


def run(tmp: Path) -> bool:
    res = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *TESTS],
                         cwd=tmp, capture_output=True, text=True, timeout=600)
    return res.returncode != 0          # True = some test failed = mutant killed


killed = 0
for name, fname, old, new in MUTANTS:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / "impl"
        shutil.copytree(SRC, tmp, ignore=shutil.ignore_patterns("__pycache__", "cai_runtime"))
        f = tmp / "cai_engine" / fname
        text = f.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"SKIP  {name}  (pattern found {text.count(old)} times)")
            continue
        f.write_text(text.replace(old, new), encoding="utf-8")
        k = run(tmp)
        killed += k
        print(("KILLED   " if k else "SURVIVED ") + name)
print(f"\nkilled {killed} of {len(MUTANTS)}")
