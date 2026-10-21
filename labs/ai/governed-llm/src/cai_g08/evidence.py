"""In-memory append-only-in-interface digest chain; no durable/WORM/notary guarantees."""
from __future__ import annotations

import hashlib
from copy import deepcopy
from dataclasses import dataclass
import threading
from .contracts import canonical_local_bytes

GENESIS = "0" * 64


@dataclass(frozen=True)
class Event:
    number: int
    kind: str
    details: dict
    predecessor: str
    digest: str


class EvidenceLog:
    def __init__(self):
        self._events: list[Event] = []
        self._lock = threading.Lock()

    def append(self, kind: str, details: dict) -> Event:
        with self._lock:
            predecessor = self._events[-1].digest if self._events else GENESIS
            number = len(self._events) + 1
            safe = deepcopy(details)
            body = canonical_local_bytes({"n": number, "kind": kind, "details": safe, "prev": predecessor})
            event = Event(number, kind, safe, predecessor, hashlib.sha256(body).hexdigest())
            self._events.append(event)
            return event

    def snapshot(self) -> list[Event]:
        with self._lock:
            return deepcopy(self._events)

    @staticmethod
    def verify(events: list[Event], expected_head: str | None = None) -> bool:
        previous = GENESIS
        for position, event in enumerate(events, 1):
            if event.number != position or event.predecessor != previous:
                return False
            body = canonical_local_bytes({"n": event.number, "kind": event.kind, "details": event.details, "prev": previous})
            if hashlib.sha256(body).hexdigest() != event.digest:
                return False
            previous = event.digest
        return expected_head is None or expected_head == previous

    @property
    def head(self):
        with self._lock:
            return self._events[-1].digest if self._events else GENESIS
