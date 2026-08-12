"""Modelos tipados del framework de eventos de AI Architecture Studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4


class EventPriority(IntEnum):
    """Prioridad de ejecución. Un valor menor se procesa primero."""

    CRITICAL = 0
    HIGH = 25
    NORMAL = 50
    LOW = 75
    BACKGROUND = 100


@dataclass(frozen=True, slots=True)
class SystemEvent:
    """Evento inmutable publicado dentro de AIAS."""

    name: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    source: str | None = None
    correlation_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        normalized = str(self.name).strip()
        if not normalized:
            raise ValueError("El nombre del evento no puede estar vacío.")
        object.__setattr__(self, "name", normalized)
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        if self.source is not None:
            object.__setattr__(self, "source", str(self.source).strip() or None)
        object.__setattr__(self, "correlation_id", str(self.correlation_id).strip())
        if not self.correlation_id:
            raise ValueError("correlation_id no puede estar vacío.")
        if self.timestamp.tzinfo is None:
            object.__setattr__(self, "timestamp", self.timestamp.replace(tzinfo=timezone.utc))


@dataclass(slots=True)
class EventContext:
    """Contexto mutable de una publicación concreta."""

    event: SystemEvent
    cancelled: bool = False
    propagation_stopped: bool = False
    responses: list[Any] = field(default_factory=list)
    errors: list[BaseException] = field(default_factory=list)

    def cancel(self) -> None:
        """Cancela el evento y detiene los consumidores restantes."""
        self.cancelled = True
        self.propagation_stopped = True

    def stop_propagation(self) -> None:
        """Detiene consumidores restantes sin marcar el evento como cancelado."""
        self.propagation_stopped = True

    def add_response(self, value: Any) -> None:
        self.responses.append(value)
