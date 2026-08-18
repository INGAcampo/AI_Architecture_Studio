"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True, slots=True)
class Event:
    """Execute the public Event operation for the Omega application core and shared runtime services using explicit caller inputs."""
    name: str
    payload: dict[str, Any]

class EventBus:
    """Execute the public EventBus operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._handlers = defaultdict(list)
        self._queue = deque()
        self._dispatching = False

    def subscribe(self, name: str, callback: Callable[[Event], None]) -> None:
        """Execute the public EventBus.subscribe operation for the Omega application core and shared runtime services using explicit caller inputs."""
        if callback not in self._handlers[name]:
            self._handlers[name].append(callback)

    def publish(self, event: Event) -> None:
        """Execute the public EventBus.publish operation for the Omega application core and shared runtime services using explicit caller inputs."""
        self._queue.append(event)
        if self._dispatching:
            return
        self._dispatching = True
        try:
            while self._queue:
                current = self._queue.popleft()
                for callback in tuple(self._handlers.get(current.name, ())):
                    callback(current)
                for callback in tuple(self._handlers.get("*", ())):
                    callback(current)
        finally:
            self._dispatching = False
