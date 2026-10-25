"""Core domain model: states, valid transitions, actions and telemetry.

This module encodes the normative definitions from the CAI-Engine documents:
  - State-Machine-Execution.md  (states, transitions, entry conditions, constraints)
  - Architecture.md             (execution flow)

The engine NEVER infers a state; states are entered only when their entry
conditions are satisfied and all guards approve the transition.
"""
from __future__ import annotations

import enum
import math
import time
import uuid
from dataclasses import dataclass, field


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
def is_finite_number(value: object) -> bool:
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except (OverflowError, ValueError):
        return False


VALID_DOMAINS = {"identity", "device", "network", "application", "data", "ai"}


@dataclass
class TelemetryEvent:
    source: str
    domain: str
    confidence: float
    provenance: str
    timestamp: float | None = None
    id: str = field(default_factory=lambda: "tel-" + uuid.uuid4().hex[:10])

    def validate(self) -> list[str]:
        """Return a list of validation errors. Empty list == conformant."""
        errors: list[str] = []
        if isinstance(self.source, str) and not self.source.strip():
            errors.append("missing source")
        elif not isinstance(self.source, str):
            errors.append("source must be a non-empty string")
        if not isinstance(self.domain, str) or self.domain not in VALID_DOMAINS:
            errors.append("domain must be a supported string")
        if not is_finite_number(self.confidence) or not (0.0 <= self.confidence <= 1.0):
            errors.append("confidence must be a number in [0.0, 1.0]")
        if isinstance(self.provenance, str) and not self.provenance.strip():
            errors.append("missing provenance metadata")
        elif not isinstance(self.provenance, str):
            errors.append("provenance must be a non-empty string")
        if self.timestamp is None:
            errors.append("missing timestamp")
        elif not is_finite_number(self.timestamp) or self.timestamp < 0:
            errors.append("timestamp must be a finite non-negative number")
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
    ot_level: int | None = None
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

    def validate(self) -> list[str]:
        errors: list[str] = []
        try:
            self.normalized_category()
        except (ValueError, TypeError):
            errors.append("invalid action category")
        if not isinstance(self.description, str) or not isinstance(self.target, str):
            errors.append("description and target must be strings")
        if self.ot_level is not None and (type(self.ot_level) is not int or not 0 <= self.ot_level <= 5):
            errors.append("ot_level must be an integer in [0, 5] or null")
        if type(self.blast_radius) is not int or self.blast_radius < 0:
            errors.append("blast_radius must be a non-negative integer")
        for name in ("destructive", "ai_assisted", "ai_explainable", "affects_privileged_accounts"):
            if type(getattr(self, name)) is not bool:
                errors.append(name + " must be a boolean")
        if not is_finite_number(self.ai_confidence) or not 0 <= self.ai_confidence <= 1:
            errors.append("ai_confidence must be a finite number in [0, 1]")
        return errors

    def normalized_category(self) -> ActionCategory:
        return self.category if isinstance(self.category, ActionCategory) else ActionCategory(self.category)


def now() -> float:
    return time.time()
