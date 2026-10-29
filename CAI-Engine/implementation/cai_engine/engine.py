"""CAI Engine orchestrator.

Implements the execution flow (Architecture.md section 5):
    telemetry ingestion -> normalization/validation -> state evaluation ->
    policy constraint evaluation -> safety gate evaluation ->
    permitted action execution -> evidence generation -> state transition.

State is persisted to a runtime directory so the CLI is stateful across calls:
    <home>/state.json       current state, context facts, pending approvals
    <home>/evidence.jsonl   hash-chained evidence log
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict

from .core import (
    ENTRY_CONDITIONS,
    INITIAL_STATE,
    VALID_TRANSITIONS,
    Action,
    ActionCategory,
    State,
    TelemetryEvent,
)
from .evidence import EvidenceLog
from .gates import (
    Decision,
    policy_evaluate,
    requires_human_approval,
    safety_gates,
    summarize,
)


class EngineError(Exception):
    pass


class CAIEngine:
    def __init__(self, home: str = "cai_runtime"):
        self.home = home
        self.state_path = os.path.join(home, "state.json")
        self.evidence = EvidenceLog(os.path.join(home, "evidence.jsonl"))
        self._state: dict = {}

    # -- persistence -------------------------------------------------------
    def _load(self) -> dict:
        if not os.path.exists(self.state_path):
            raise EngineError("engine not initialized — run `init` first")
        with open(self.state_path, encoding="utf-8") as fh:
            self._state = json.load(fh)
        return self._state

    def _save(self) -> None:
        os.makedirs(self.home, exist_ok=True)
        with open(self.state_path, "w", encoding="utf-8") as fh:
            json.dump(self._state, fh, indent=2, ensure_ascii=False)

    # -- lifecycle ---------------------------------------------------------
    def init(self) -> dict:
        # Refuse reinitialization and incomplete runtimes; preserve evidence.
        if os.path.lexists(self.state_path) or os.path.lexists(self.evidence.path):
            raise EngineError("runtime artifacts already exist; preserve them and perform explicit recovery")
        os.makedirs(self.home, exist_ok=True)
        with open(self.evidence.path, "x", encoding="utf-8"):
            pass
        self._state = {"current_state": INITIAL_STATE.value, "facts": {}, "pending": {}}
        self._save()
        self.evidence.append("ENGINE_INIT", {"initial_state": INITIAL_STATE.value})
        return self._state

    def status(self) -> dict:
        self._load()
        cur = State(self._state["current_state"])
        return {
            "current_state": cur.value,
            "allowed_transitions": [s.value for s in VALID_TRANSITIONS.get(cur, [])],
            "entry_conditions_next": {
                s.value: ENTRY_CONDITIONS.get(s, []) for s in VALID_TRANSITIONS.get(cur, [])
            },
            "facts": self._state.get("facts", {}),
            "pending_approvals": list(self._state.get("pending", {}).keys()),
            "evidence_records": self.evidence.count(),
        }

    # -- context facts -----------------------------------------------------
    def set_fact(self, key: str, value: bool) -> dict:
        self._load()
        if not isinstance(key, str) or not key.strip() or type(value) is not bool:
            self.evidence.append("FACT_INPUT_REJECTED", {"reason_code": "INVALID_FACT_TYPE"})
            raise EngineError("fact key must be a non-empty string and value must be a boolean")
        self._state.setdefault("facts", {})[key] = value
        self._save()
        self.evidence.append("FACT_SET", {"fact": key, "value": bool(value)})
        return {"fact": key, "value": bool(value)}

    # -- telemetry ingestion ----------------------------------------------
    def ingest(self, data: dict) -> dict:
        self._load()
        if not isinstance(data, dict):
            errors = ["telemetry must be an object"]
            self.evidence.append("TELEMETRY_REJECTED", {"errors": errors, "reason_code": "INVALID_INPUT_SHAPE"})
            return {"accepted": False, "errors": errors}
        ev = TelemetryEvent(
            source=data.get("source", ""),
            domain=data.get("domain", ""),
            confidence=data.get("confidence", -1),
            provenance=data.get("provenance", ""),
            timestamp=data.get("timestamp"),
        )
        errors = ev.validate()
        if errors:
            self.evidence.append("TELEMETRY_REJECTED", {"event_id": ev.id, "errors": errors})
            return {"accepted": False, "id": ev.id, "errors": errors}
        self.evidence.append("TELEMETRY_ACCEPTED", {"event": asdict(ev)})
        return {"accepted": True, "id": ev.id}

    # -- action proposal (policy -> safety -> oversight) -------------------
    def _build_action(self, data: dict) -> Action:
        if not isinstance(data, dict):
            raise EngineError("action must be an object")
        allowed = {"category", "description", "target", "ot_level", "blast_radius", "destructive",
                   "ai_assisted", "ai_confidence", "ai_explainable", "affects_privileged_accounts", "id"}
        if any(key not in allowed for key in data):
            raise EngineError("action contains an unknown field")
        try:
            cat = ActionCategory(data["category"])
        except (KeyError, ValueError):
            raise EngineError(
                f"invalid or missing 'category' (allowed: {[c.value for c in ActionCategory]})")
        action = Action(
            category=cat,
            description=data.get("description", ""),
            target=data.get("target", ""),
            ot_level=data.get("ot_level"),
            blast_radius=data.get("blast_radius", 0),
            destructive=data.get("destructive", False),
            ai_assisted=data.get("ai_assisted", False),
            ai_confidence=data.get("ai_confidence", 1.0),
            ai_explainable=data.get("ai_explainable", True),
            affects_privileged_accounts=data.get("affects_privileged_accounts", False),
        )
        errors = action.validate()
        if errors:
            raise EngineError("invalid action: " + "; ".join(errors))
        return action

    def evaluate(self, action: Action) -> dict:
        """Run policy + safety + oversight for an action WITHOUT side effects.

        Returns the gate results, the combined decision and whether human
        approval is required. Used by `propose()` and by the governed-agent
        layer so a regulatory layer can be combined before anything is
        recorded or executed.
        """
        self._load()
        errors = action.validate()
        if errors:
            raise EngineError("invalid action: " + "; ".join(errors))
        cur = State(self._state["current_state"])
        pol = policy_evaluate(action, cur)
        gates = safety_gates(action)
        all_results = [pol] + gates
        decision = summarize(all_results)
        needs_human = requires_human_approval(action, cur, all_results)
        return {
            "action": asdict(action),
            "state": cur.value,
            "gate_results": [asdict(g) for g in all_results],
            "decision": decision.value,
            "requires_human_approval": needs_human,
        }

    def commit(self, action_id: str, record: dict,
               blocked_event: str = "ACTION_BLOCKED",
               pending_event: str = "ACTION_PENDING_APPROVAL",
               executed_event: str = "ACTION_EXECUTED") -> dict:
        """Record and act on a decided `record` (from evaluate / governed layer)."""
        decision = record["decision"]
        needs_human = record["requires_human_approval"]
        if decision == Decision.DENY.value:
            self.evidence.append(blocked_event, record)
            return {"status": "BLOCKED", **record}
        if needs_human:
            self._load()
            self._state.setdefault("pending", {})[action_id] = record
            self._save()
            self.evidence.append(pending_event, record)
            return {"status": "PENDING_APPROVAL", "action_id": action_id, **record}
        self.evidence.append(executed_event, {**record, "approved_by": None})
        return {"status": "EXECUTED", "action_id": action_id, **record}

    def propose(self, data: dict) -> dict:
        try:
            action = self._build_action(data)
            record = self.evaluate(action)
        except (EngineError, TypeError, ValueError, OverflowError) as exc:
            self.evidence.append("ACTION_INPUT_REJECTED", {
                "reason_code": "INVALID_ACTION", "error_type": type(exc).__name__})
            raise EngineError("action rejected: " + str(exc)) from exc
        return self.commit(action.id, record)

    def approve(self, action_id: str, approver: str) -> dict:
        self._load()
        pending = self._state.get("pending", {})
        if action_id not in pending:
            raise EngineError(f"no pending action with id {action_id}")
        if not isinstance(approver, str) or not approver.strip():
            raise EngineError("an approver name is required (human authority is attributed)")
        record = pending[action_id]
        expected_state = record.get("state", record.get("cai_engine", {}).get("state"))
        try:
            if expected_state != self._state["current_state"]:
                raise EngineError("state changed since proposal; submit a new proposal")
            if record.get("decision") not in (Decision.ALLOW.value, Decision.ESCALATE.value):
                raise EngineError("pending record has no admissible original decision")
            if "jurisdiction" in record:
                context = record.get("approval_context")
                if not isinstance(context, dict):
                    raise EngineError("legacy governed proposal lacks revalidation context; resubmit")
                from .governed_agent import GovernedAgent
                refreshed = GovernedAgent(self).evaluate_proposal(
                    context["proposal"], jurisdiction=context["jurisdiction"])
            else:
                refreshed = self.evaluate(Action(**record["action"]))
            if refreshed["decision"] == Decision.DENY.value:
                raise EngineError("current policy or safety gate denies this approval")
            latest = self._load()
            if latest["current_state"] != expected_state or latest.get("pending", {}).get(action_id) != record:
                raise EngineError("proposal or state changed during revalidation; resubmit")
        except (EngineError, KeyError, TypeError, ValueError) as exc:
            self.evidence.append("HUMAN_APPROVAL_REJECTED", {
                "action_id": action_id, "reason": str(exc),
                "current_state": self._state["current_state"], "approved_by": approver})
            raise EngineError("approval revalidation failed: " + str(exc)) from exc
        # Only consume the pending proposal after successful revalidation.
        record = {**record, "approval_revalidation": refreshed}
        self._state["pending"].pop(action_id)
        self._save()
        self.evidence.append("HUMAN_APPROVAL", {"action_id": action_id, "approved_by": approver})
        self.evidence.append("ACTION_EXECUTED", {**record, "approved_by": approver})
        return {"status": "EXECUTED", "action_id": action_id, "approved_by": approver}

    def deny(self, action_id: str, approver: str, reason: str) -> dict:
        self._load()
        pending = self._state.get("pending", {})
        if action_id not in pending:
            raise EngineError(f"no pending action with id {action_id}")
        pending.pop(action_id)
        self._save()
        self.evidence.append("HUMAN_DENIAL",
                             {"action_id": action_id, "denied_by": approver, "reason": reason})
        return {"status": "DENIED_BY_HUMAN", "action_id": action_id}

    # -- state transition --------------------------------------------------
    def transition(self, target_name: str) -> dict:
        self._load()
        cur = State(self._state["current_state"])
        try:
            target = State(target_name.upper())
        except ValueError:
            raise EngineError(f"unknown state '{target_name}' (states: {[s.value for s in State]})")

        if target not in VALID_TRANSITIONS.get(cur, []):
            self.evidence.append("TRANSITION_BLOCKED",
                                 {"from": cur.value, "to": target.value, "reason": "invalid transition"})
            return {"status": "BLOCKED", "from": cur.value, "to": target.value,
                    "reason": f"{cur.value} -> {target.value} is not a valid transition"}

        facts = self._state.get("facts", {})
        missing = [c for c in ENTRY_CONDITIONS.get(target, []) if not facts.get(c)]
        if missing:
            self.evidence.append("TRANSITION_BLOCKED",
                                 {"from": cur.value, "to": target.value, "unmet_entry_conditions": missing})
            return {"status": "BLOCKED", "from": cur.value, "to": target.value,
                    "unmet_entry_conditions": missing}

        self._state["current_state"] = target.value
        self._save()
        self.evidence.append("STATE_TRANSITION", {"from": cur.value, "to": target.value})
        return {"status": "OK", "from": cur.value, "to": target.value}

    # -- audit -------------------------------------------------------------
    def verify(self) -> dict:
        ok, err = self.evidence.verify()
        return {"integrity_ok": ok, "error": err, "records": self.evidence.count()}

    def report(self) -> str:
        self._load()
        lines = ["# CAI-Engine — Execution & Assurance Report", ""]
        lines.append(f"- Current state: **{self._state['current_state']}**")
        lines.append(f"- Context facts: {self._state.get('facts', {})}")
        lines.append(f"- Pending approvals: {list(self._state.get('pending', {}).keys())}")
        ok, err = self.evidence.verify()
        lines.append(f"- Evidence integrity: {'OK (chain verified)' if ok else 'FAILED — ' + str(err)}")
        lines.append("")
        lines.append("## Evidence log (hash-chained)")
        lines.append("")
        lines.append("| seq | event | detail |")
        lines.append("|----:|-------|--------|")
        for rec in self.evidence.records():
            p = rec.get("payload", {})
            detail = ""
            et = rec.get("event_type", "")
            if et in ("STATE_TRANSITION", "TRANSITION_BLOCKED"):
                detail = f"{p.get('from','')} -> {p.get('to','')} {p.get('reason','') or p.get('unmet_entry_conditions','')}"
            elif et.startswith("GOVERNED"):
                reg = p.get("regulatory", {})
                juris = p.get("jurisdiction", "")
                label = reg.get("label", "")
                sector = reg.get("sector", "")
                tag = f"{juris}:{label}" + (f"/{sector}" if sector else "")
                a = p.get("action", {})
                detail = (f"AI[{p.get('ai_system','')}] {tag} "
                          f"{a.get('category','')} decision={p.get('decision','')}")
            elif et.startswith("ACTION") or et == "HUMAN_APPROVAL":
                a = p.get("action", {})
                detail = f"{a.get('category','')} '{a.get('description','')}' decision={p.get('decision','')}"
                if p.get("approved_by"):
                    detail += f" approved_by={p['approved_by']}"
                if p.get("action_id") and not a:
                    detail = f"action_id={p.get('action_id')} by={p.get('approved_by','')}"
            elif et.startswith("TELEMETRY"):
                detail = f"{p.get('event',{}).get('domain','')} {p.get('errors','')}"
            elif et == "FACT_SET":
                detail = f"{p.get('fact','')}={p.get('value','')}"
            lines.append(f"| {rec.get('seq','')} | {et} | {detail} |")
        return "\n".join(lines)
