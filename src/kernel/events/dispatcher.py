"""Dispatcher síncrono, determinista y desacoplado para eventos AIAS."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from typing import Any

from .exceptions import EventDispatchError
from .model import EventContext, EventPriority, SystemEvent
from .subscription import EventHandler, Subscription, SubscriptionToken


class EventDispatcher:
    """Distribuye eventos por prioridad y orden de registro.

    Las publicaciones reentrantes se encolan y se procesan FIFO después del
    evento actual. Esto evita recursión descontrolada y mantiene un orden
    reproducible entre módulos.
    """

    WILDCARD = "*"

    def __init__(self) -> None:
        self._subscriptions: dict[str, list[Subscription]] = {}
        self._sequence = 0
        self._queue: deque[tuple[SystemEvent, bool, EventContext]] = deque()
        self._dispatching = False
        self._enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
        *,
        priority: EventPriority = EventPriority.NORMAL,
        once: bool = False,
    ) -> SubscriptionToken:
        name = self._normalize_name(event_name, allow_wildcard=True)
        if not callable(handler):
            raise TypeError("handler debe ser invocable.")
        self._sequence += 1
        token = SubscriptionToken.create()
        subscription = Subscription(
            token=token,
            event_name=name,
            handler=handler,
            priority=EventPriority(priority),
            once=bool(once),
            sequence=self._sequence,
        )
        self._subscriptions.setdefault(name, []).append(subscription)
        return token

    def unsubscribe(self, token: SubscriptionToken) -> bool:
        removed = False
        for name in tuple(self._subscriptions):
            current = self._subscriptions[name]
            filtered = [item for item in current if item.token != token]
            if len(filtered) != len(current):
                removed = True
            if filtered:
                self._subscriptions[name] = filtered
            else:
                self._subscriptions.pop(name, None)
        return removed

    def clear(self, event_name: str | None = None) -> int:
        if event_name is None:
            count = sum(len(items) for items in self._subscriptions.values())
            self._subscriptions.clear()
            return count
        name = self._normalize_name(event_name, allow_wildcard=True)
        return len(self._subscriptions.pop(name, ()))

    def subscriber_count(self, event_name: str | None = None) -> int:
        if event_name is None:
            return sum(len(items) for items in self._subscriptions.values())
        name = self._normalize_name(event_name, allow_wildcard=True)
        return len(self._subscriptions.get(name, ()))

    def publish(
        self,
        event: SystemEvent | str,
        payload: dict[str, Any] | None = None,
        *,
        source: str | None = None,
        strict: bool = False,
    ) -> EventContext:
        system_event = (
            event
            if isinstance(event, SystemEvent)
            else SystemEvent(name=event, payload=payload or {}, source=source)
        )
        context = EventContext(system_event)
        if not self._enabled:
            return context

        self._queue.append((system_event, bool(strict), context))
        if self._dispatching:
            return context

        self._dispatching = True
        try:
            while self._queue:
                queued_event, queued_strict, queued_context = self._queue.popleft()
                self._dispatch_one(queued_event, queued_context)
                if queued_strict and queued_context.errors:
                    raise EventDispatchError(queued_event.name, queued_context.errors)
        finally:
            self._dispatching = False
        return context

    def publish_many(
        self,
        events: Iterable[SystemEvent],
        *,
        strict: bool = False,
    ) -> tuple[EventContext, ...]:
        contexts: list[EventContext] = []
        for event in events:
            contexts.append(self.publish(event, strict=strict))
        return tuple(contexts)

    def _dispatch_one(self, event: SystemEvent, context: EventContext) -> None:
        exact = list(self._subscriptions.get(event.name, ()))
        wildcard = list(self._subscriptions.get(self.WILDCARD, ()))
        subscriptions = sorted(
            (*exact, *wildcard),
            key=lambda item: (int(item.priority), item.sequence),
        )
        for subscription in subscriptions:
            if context.propagation_stopped:
                break
            try:
                response = subscription.handler(context)
                if response is not None:
                    context.add_response(response)
            except BaseException as exc:  # se registra; strict decide si propagar
                context.errors.append(exc)
            finally:
                if subscription.once:
                    self.unsubscribe(subscription.token)

    @staticmethod
    def _normalize_name(value: str, *, allow_wildcard: bool) -> str:
        name = str(value).strip()
        if not name:
            raise ValueError("El nombre del evento no puede estar vacío.")
        if name == EventDispatcher.WILDCARD and allow_wildcard:
            return name
        return name
