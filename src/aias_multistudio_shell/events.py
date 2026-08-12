"""Public module supporting the coordinated multi-studio desktop shell."""
from dataclasses import dataclass
from collections import defaultdict
from typing import Callable, Any

@dataclass(frozen=True, slots=True)
class StudioEvent:
    """Execute the public StudioEvent operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    name: str
    payload: dict[str, Any]

class EventBus:
    """Execute the public EventBus operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self) -> None:
        self._handlers = defaultdict(list)

    def subscribe(self, name: str, callback: Callable[[StudioEvent], None]) -> None:
        """Execute the public EventBus.subscribe operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        if callback not in self._handlers[name]:
            self._handlers[name].append(callback)

    def publish(self, event: StudioEvent) -> None:
        """Execute the public EventBus.publish operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        for callback in tuple(self._handlers.get(event.name, ())):
            callback(event)
        for callback in tuple(self._handlers.get("*", ())):
            callback(event)
