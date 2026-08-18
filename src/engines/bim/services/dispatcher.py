"""Despachador BIM compatible con el EventBus existente del kernel."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from .events import BimEvent, BimEventName


EventCallback = Callable[[BimEvent], None]


class BimEventDispatcher:
    def __init__(self, external_event_bus: Any | None = None) -> None:
        self._listeners: dict[str, list[EventCallback]] = defaultdict(list)
        self._external_event_bus = external_event_bus

    def subscribe(
        self,
        event_name: BimEventName | str,
        callback: EventCallback,
    ) -> None:
        key = _event_key(event_name)
        if callback not in self._listeners[key]:
            self._listeners[key].append(callback)

    def unsubscribe(
        self,
        event_name: BimEventName | str,
        callback: EventCallback,
    ) -> None:
        key = _event_key(event_name)
        listeners = self._listeners.get(key, [])
        if callback in listeners:
            listeners.remove(callback)

    def emit(self, event: BimEvent) -> None:
        for callback in tuple(self._listeners.get(event.name.value, ())):
            callback(event)

        if self._external_event_bus is not None:
            emit = getattr(self._external_event_bus, "emit", None)
            if callable(emit):
                emit(event.name.value, event)


def _event_key(value: BimEventName | str) -> str:
    return value.value if isinstance(value, BimEventName) else str(value)
