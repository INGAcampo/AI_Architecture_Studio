from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from time import time


@dataclass(frozen=True, slots=True)
class WorkspaceEvent:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)


class WorkspaceEventSink:
    """Adaptador mínimo compatible con dispatch(event), emit(name, payload) o callable."""

    def __init__(self, target=None) -> None:
        self.target = target

    def publish(self, event_name: str, **payload: Any) -> WorkspaceEvent:
        event = WorkspaceEvent(name=event_name, payload=dict(payload))
        target = self.target
        if target is None:
            return event

        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(event)
            except TypeError:
                dispatch(event_name, dict(payload))
            return event

        emit = getattr(target, "emit", None)
        if callable(emit):
            emit(event_name, dict(payload))
            return event

        if callable(target):
            target(event)
        return event
