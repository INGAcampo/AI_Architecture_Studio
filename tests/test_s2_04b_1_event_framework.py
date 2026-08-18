from __future__ import annotations

import pytest

from kernel.events import (
    EventDispatchError,
    EventDispatcher,
    EventPriority,
    SystemEvent,
)


def test_system_event_is_immutable_and_payload_is_read_only():
    event = SystemEvent("ObjectModified", {"id": "wall-1"})
    assert event.name == "ObjectModified"
    with pytest.raises(TypeError):
        event.payload["id"] = "wall-2"


def test_event_name_cannot_be_empty():
    with pytest.raises(ValueError):
        SystemEvent("   ")


def test_dispatcher_publishes_payload_and_source():
    dispatcher = EventDispatcher()
    received = []
    dispatcher.subscribe("PropertyChanged", lambda ctx: received.append(ctx.event))
    context = dispatcher.publish("PropertyChanged", {"value": 25}, source="inspector")
    assert received[0].payload["value"] == 25
    assert received[0].source == "inspector"
    assert context.event is received[0]


def test_priority_then_registration_order_is_deterministic():
    dispatcher = EventDispatcher()
    order = []
    dispatcher.subscribe("E", lambda ctx: order.append("normal-1"))
    dispatcher.subscribe("E", lambda ctx: order.append("high"), priority=EventPriority.HIGH)
    dispatcher.subscribe("E", lambda ctx: order.append("normal-2"))
    dispatcher.publish("E")
    assert order == ["high", "normal-1", "normal-2"]


def test_wildcard_subscriber_receives_all_events():
    dispatcher = EventDispatcher()
    names = []
    dispatcher.subscribe("*", lambda ctx: names.append(ctx.event.name))
    dispatcher.publish("A")
    dispatcher.publish("B")
    assert names == ["A", "B"]


def test_unsubscribe_is_idempotent():
    dispatcher = EventDispatcher()
    token = dispatcher.subscribe("E", lambda ctx: None)
    assert dispatcher.unsubscribe(token) is True
    assert dispatcher.unsubscribe(token) is False


def test_once_subscription_runs_only_one_time():
    dispatcher = EventDispatcher()
    calls = []
    dispatcher.subscribe("E", lambda ctx: calls.append(1), once=True)
    dispatcher.publish("E")
    dispatcher.publish("E")
    assert calls == [1]


def test_cancel_stops_remaining_handlers_and_marks_context():
    dispatcher = EventDispatcher()
    calls = []

    def cancel(ctx):
        calls.append("cancel")
        ctx.cancel()

    dispatcher.subscribe("E", cancel, priority=EventPriority.HIGH)
    dispatcher.subscribe("E", lambda ctx: calls.append("late"))
    context = dispatcher.publish("E")
    assert context.cancelled is True
    assert calls == ["cancel"]


def test_handler_responses_are_collected():
    dispatcher = EventDispatcher()
    dispatcher.subscribe("E", lambda ctx: "renderer")
    dispatcher.subscribe("E", lambda ctx: None)
    assert dispatcher.publish("E").responses == ["renderer"]


def test_non_strict_dispatch_collects_errors_and_continues():
    dispatcher = EventDispatcher()
    calls = []

    def broken(ctx):
        raise RuntimeError("boom")

    dispatcher.subscribe("E", broken, priority=EventPriority.HIGH)
    dispatcher.subscribe("E", lambda ctx: calls.append("continued"))
    context = dispatcher.publish("E")
    assert len(context.errors) == 1
    assert calls == ["continued"]


def test_strict_dispatch_raises_aggregate_error():
    dispatcher = EventDispatcher()
    dispatcher.subscribe("E", lambda ctx: (_ for _ in ()).throw(ValueError("bad")))
    with pytest.raises(EventDispatchError) as exc_info:
        dispatcher.publish("E", strict=True)
    assert len(exc_info.value.errors) == 1


def test_reentrant_publications_are_processed_fifo_after_current_event():
    dispatcher = EventDispatcher()
    order = []

    def first(ctx):
        order.append("A:start")
        dispatcher.publish("B")
        order.append("A:end")

    dispatcher.subscribe("A", first)
    dispatcher.subscribe("B", lambda ctx: order.append("B"))
    dispatcher.publish("A")
    assert order == ["A:start", "A:end", "B"]


def test_disabled_dispatcher_does_not_invoke_subscribers():
    dispatcher = EventDispatcher()
    calls = []
    dispatcher.subscribe("E", lambda ctx: calls.append(1))
    dispatcher.set_enabled(False)
    context = dispatcher.publish("E")
    assert calls == []
    assert context.event.name == "E"
