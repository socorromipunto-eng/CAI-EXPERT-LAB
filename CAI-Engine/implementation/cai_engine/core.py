"""Core domain model: states, valid transitions, actions and telemetry.

This module encodes the normative definitions from the CAI-Engine documents:
  - State-Machine-Execution.md  (states, transitions, entry conditions, constraints)
  - Architecture.md             (execution flow)

The engine NEVER infers a state; states are entered only when their entry
conditions are satisfied and all guards approve the transition.
"""
from __future__ import annotations

import enum
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


# --------------------------------------------------------------------------
# 1. Authoritative state set  (State-Machine-Execution.md, section 4)
# --------------------------------------------------------------------------
class State(str, enum.Enum):
    MODEL = "MODEL"
    HARDEN = "HARDEN"
    DETECT = "DETECT"
    ISOLATE = "ISOLATE"
    DECEIVE = "DECEIVE"
    EVICT = "EVICT"
    RESTORE = "RESTORE"


INITIAL_STATE = State.MODEL

# --------------------------------------------------------------------------
# 2. Valid state transitions  (State-Machine-Execution.md, section 7)
#    All transitions not listed here are invalid and blocked.
# --------------------------------------------------------------------------
VALID_TRANSITIONS: dict[State, list[State]] = {
    State.MODEL: [State.HARDEN],
    State.HARDEN: [State.DETECT],
    State.DETECT: [State.ISOLATE, State.DECEIVE],
    State.ISOLATE: [State.EVICT],
    State.DECEIVE: [State.EVICT],
    State.EVICT: [State.RESTORE],
    State.RESTORE: [State.MODEL],
}

# --------------------------------------------------------------------------
# 3. Entry conditions  (State-Machine-Execution.md, section 5)
#    Each target state requires a set of context facts to be TRUE before
#    the engine will allow entry. Facts are set as the lifecycle progresses.
# --------------------------------------------------------------------------
ENTRY_CONDITIONS: dict[State, list[str]] = {
    State.MODEL: [],
    State.HARDEN: ["assets_discovered", "telemetry_validated"],
    State.DETECT: ["baseline_hardened", "telemetry_active"],
    State.ISOLATE: ["detection_confirmed"],
    State.DECEIVE: ["detection_confirmed", "deception_scope_approved"],
    State.EVICT: ["malicious_presence_confirmed", "safety_approved"],
    State.RESTORE: ["eviction_completed", "clean_baseline_validated"],
}


# --------------------------------------------------------------------------
# 4. Action categories and per-state constraints
#    (State-Machine-Execution.md, section 6 — state execution constraints)
# --------------------------------------------------------------------------
class ActionCategory(str, enum.Enum):
    OBSERVE = "OBSERVE"            # modeling, discovery, monitoring — never operational
    HARDENING = "HARDENING"       # preventive changes
    CONTAINMENT = "CONTAINMENT"   # isolation / segmentation
    DECEPTION = "DECEPTION"       # approved deception assets
    ERADICATION = "ERADICATION"   # eviction / removal
    RECOVERY = "RECOVERY"         # restoration


# OBSERVE is permitted in every state. Each state adds its own permitted set.
ALLOWED_ACTIONS: dict[State, set[ActionCategory]] = {
    State.MODEL: {ActionCategory.OBSERVE},
    State.HARDEN: {ActionCategory.OBSERVE, ActionCategory.HARDENING},
    State.DETECT: {ActionCategory.OBSERVE},
    State.ISOLATE: {ActionCategory.OBSERVE, ActionCategory.CONTAINMENT},
    State.DECEIVE: {ActionCategory.OBSERVE, ActionCategory.DECEPTION},
    State.EVICT: {ActionCategory.OBSERVE, ActionCategory.ERADICATION},
    State.RESTORE: {ActionCategory.OBSERVE, ActionCategory.RECOVERY},
}


# --------------------------------------------------------------------------
# 5. Telemetry  (Architecture.md 4.2 — ingestion & normalization)
#    Non-conforming telemetry is rejected or quarantined; the engine never
#    operates on unnormalized or unverifiable data.
# --------------------------------------------------------------------------
VALID_DOMAINS = {"identity", "device", "network", "application", "data", "ai"}


@dataclass
class TelemetryEvent:
    source: str
    domain: str
    confidence: float
    provenance: str
    timestamp: Optional[float] = None
    id: str = field(default_factory=lambda: "tel-" + uuid.uuid4().hex[:10])

    def validate(self) -> list[str]:
        """Return a list of validation errors. Empty list == conformant."""
        errors: list[str] = []
        if not self.source:
            errors.append("missing source")
        if self.domain not in VALID_DOMAINS:
            errors.append(f"invalid domain '{self.domain}' (allowed: {sorted(VALID_DOMAINS)})")
        if not isinstance(self.confidence, (int, float)) or not (0.0 <= self.confidence <= 1.0):
            errors.append("confidence must be a number in [0.0, 1.0]")
        if not self.provenance:
            errors.append("missing provenance metadata")
        if self.timestamp is None:
            errors.append("missing timestamp")
        return errors


# --------------------------------------------------------------------------
# 6. Action  (the unit of work the engine gates and executes)
# --------------------------------------------------------------------------
@dataclass
class Action:
    category: ActionCategory
    description: str
    target: str = ""
    # Purdue level of the affected asset (0-5) for OT/ICS gating; None = IT.
    ot_level: Optional[int] = None
    # Number of assets in scope — used by the blast-radius gate.
    blast_radius: int = 0
    destructive: bool = False
    # AI-assisted recommendation metadata (AI is advisory only).
    ai_assisted: bool = False
    ai_confidence: float = 1.0
    ai_explainable: bool = True
    # Privileged-identity impact (triggers mandatory human approval).
    affects_privileged_accounts: bool = False
    id: str = field(default_factory=lambda: "act-" + uuid.uuid4().hex[:10])

    def normalized_category(self) -> ActionCategory:
        return self.category if isinstance(self.category, ActionCategory) else ActionCategory(self.category)


def now() -> float:
    return time.time()
