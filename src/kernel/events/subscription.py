"""Suscripciones del framework de eventos AIAS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from uuid import uuid4

from .model import EventContext, EventPriority

EventHandler = Callable[[EventContext], object]


@dataclass(frozen=True, slots=True)
class SubscriptionToken:
    """Identificador opaco utilizado para cancelar una suscripción."""

    value: str

    @classmethod
    def create(cls) -> "SubscriptionToken":
        return cls(uuid4().hex)


@dataclass(slots=True)
class Subscription:
    token: SubscriptionToken
    event_name: str
    handler: EventHandler
    priority: EventPriority
    once: bool
    sequence: int
