from __future__ import annotations

from types import MappingProxyType

import pytest

from engines.live_data_graph import (
    GRAPH_CHANGED_EVENT,
    OWNER_REMOVED_EVENT,
    PROPERTY_BOUND_EVENT,
    PROPERTY_CHANGED_EVENT,
    GraphEventBridge,
    LiveDataGraph,
    NodeState,
    PropertyChangeRecord,
    ReactivePropertyService,
)
from engines.property import PropertyDefinition, PropertyType
from kernel.events import EventDispatcher


def make_service() -> ReactivePropertyService:
    service = ReactivePropertyService()
    service.register_definition(
        PropertyDefinition("Height", PropertyType.LENGTH, unit="m")
    )
    service.register_definition(
        PropertyDefinition("Comments", PropertyType.TEXT)
    )
    return service


def test_reactive_service_preserves_property_service_contract() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    previous = service.set_value("wall-01", "Height", 3.2)
    assert previous == 3.0
    assert service.get_value("wall-01", "Height") == 3.2


def test_bind_creates_owner_and_property_nodes() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    assert service.owner_node_id("wall-01") in service.graph
    assert service.property_node_id("wall-01", "Height") in service.graph


def test_property_node_invalidates_owner_node() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    service.set_value("wall-01", "Height", 3.5)
    owner = service.graph.require_node(service.owner_node_id("wall-01"))
    assert owner.state is NodeState.DIRTY
    assert owner.revision == service.graph.revision


def test_bind_publishes_typed_bound_event() -> None:
    service = make_service()
    received = []
    service.dispatcher.subscribe(PROPERTY_BOUND_EVENT, lambda ctx: received.append(ctx.event))
    service.bind("wall-01", "Height", 3.0)
    assert received[0].payload["owner_id"] == "wall-01"
    assert received[0].payload["property_name"] == "Height"


def test_real_change_publishes_graph_and_property_events() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    names = []
    service.dispatcher.subscribe("*", lambda ctx: names.append(ctx.event.name))
    service.set_value("wall-01", "Height", 3.2)
    assert GRAPH_CHANGED_EVENT in names
    assert PROPERTY_CHANGED_EVENT in names


def test_redundant_value_does_not_increment_revision_or_publish_change() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    received = []
    service.dispatcher.subscribe(PROPERTY_CHANGED_EVENT, lambda ctx: received.append(ctx))
    revision = service.graph.revision
    service.set_value("wall-01", "Height", 3.0)
    assert service.graph.revision == revision
    assert received == []


def test_property_change_payload_contains_previous_new_and_revision() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    payloads = []
    service.dispatcher.subscribe(PROPERTY_CHANGED_EVENT, lambda ctx: payloads.append(ctx.event.payload))
    service.set_value("wall-01", "Height", 3.4, metadata={"origin": "inspector"})
    payload = payloads[0]
    assert payload["previous_value"] == 3.0
    assert payload["new_value"] == 3.4
    assert payload["graph_revision"] == service.graph.revision
    assert payload["metadata"]["origin"] == "inspector"


def test_input_unit_conversion_is_reflected_in_event_and_graph() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 1.0)
    payloads = []
    service.dispatcher.subscribe(PROPERTY_CHANGED_EVENT, lambda ctx: payloads.append(ctx.event.payload))
    service.set_value("wall-01", "Height", 10.0, input_unit="ft")
    assert service.graph.require_node(service.property_node_id("wall-01", "Height")).payload == pytest.approx(3.048)
    assert payloads[0]["new_value"] == pytest.approx(3.048)


def test_register_dependent_participates_in_propagation() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    service.register_dependent("wall-01", "Height", "inspector:wall-01", kind="inspector")
    changes = []
    service.dispatcher.subscribe(GRAPH_CHANGED_EVENT, lambda ctx: changes.append(ctx.event.payload))
    service.set_value("wall-01", "Height", 3.3)
    assert "inspector:wall-01" in changes[0]["affected_ids"]


def test_register_existing_dependent_is_supported() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    service.graph.add_node("bim:wall-01", "bim")
    result = service.register_dependent("wall-01", "Height", "bim:wall-01")
    assert result == "bim:wall-01"


def test_remove_owner_removes_graph_nodes_and_publishes_event() -> None:
    service = make_service()
    service.bind("wall-01", "Height", 3.0)
    service.bind("wall-01", "Comments", "Exterior")
    payloads = []
    service.dispatcher.subscribe(OWNER_REMOVED_EVENT, lambda ctx: payloads.append(ctx.event.payload))
    removed = service.remove_owner("wall-01")
    assert len(removed) == 2
    assert service.owner_node_id("wall-01") not in service.graph
    assert payloads[0]["owner_id"] == "wall-01"


def test_remove_unknown_owner_is_silent() -> None:
    service = make_service()
    payloads = []
    service.dispatcher.subscribe(OWNER_REMOVED_EVENT, lambda ctx: payloads.append(ctx))
    assert service.remove_owner("missing") == {}
    assert payloads == []


def test_graph_event_bridge_can_stop_and_restart() -> None:
    graph = LiveDataGraph()
    dispatcher = EventDispatcher()
    bridge = GraphEventBridge(graph, dispatcher)
    events = []
    dispatcher.subscribe(GRAPH_CHANGED_EVENT, lambda ctx: events.append(ctx.event))
    graph.add_node("n1", "test")
    bridge.start()
    graph.mark_dirty("n1")
    bridge.stop()
    graph.mark_dirty("n1")
    bridge.start()
    graph.mark_dirty("n1")
    assert len(events) == 2


def test_property_change_record_is_immutable_and_metadata_is_read_only() -> None:
    record = PropertyChangeRecord("wall-01", "Height", 3.0, 3.2, 1, metadata={"x": 1})
    assert isinstance(record.metadata, MappingProxyType)
    with pytest.raises(TypeError):
        record.metadata["x"] = 2
    with pytest.raises(Exception):
        record.owner_id = "other"


def test_external_dispatcher_and_graph_are_reused() -> None:
    graph = LiveDataGraph()
    dispatcher = EventDispatcher()
    service = ReactivePropertyService(graph=graph, dispatcher=dispatcher)
    assert service.graph is graph
    assert service.dispatcher is dispatcher
