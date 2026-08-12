"""Integración entre Property Engine, Live Data Graph y Event Framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from engines.property.service import PropertyService
from kernel.events import EventDispatcher, SystemEvent

from .graph import LiveDataGraph
from .model import GraphChange


PROPERTY_BOUND_EVENT = "aias.property.bound"
PROPERTY_CHANGED_EVENT = "aias.property.changed"
GRAPH_CHANGED_EVENT = "aias.graph.changed"
OWNER_REMOVED_EVENT = "aias.property.owner_removed"


@dataclass(frozen=True, slots=True)
class PropertyChangeRecord:
    """Cambio inmutable de una propiedad dentro del pipeline reactivo."""

    owner_id: str
    property_name: str
    previous_value: Any
    new_value: Any
    graph_revision: int
    source: str = "property_service"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "owner_id", str(self.owner_id))
        object.__setattr__(self, "property_name", str(self.property_name))
        object.__setattr__(self, "source", str(self.source))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def to_payload(self) -> dict[str, Any]:
        return {
            "owner_id": self.owner_id,
            "property_name": self.property_name,
            "previous_value": self.previous_value,
            "new_value": self.new_value,
            "graph_revision": self.graph_revision,
            "source": self.source,
            "metadata": dict(self.metadata),
        }


class GraphEventBridge:
    """Publica cada propagación del grafo como evento oficial de AIAS."""

    def __init__(self, graph: LiveDataGraph, dispatcher: EventDispatcher) -> None:
        self.graph = graph
        self.dispatcher = dispatcher
        self._active = False
        self._unsubscribe = None

    @property
    def active(self) -> bool:
        return self._active

    def start(self) -> None:
        if not self._active:
            self._unsubscribe = self.graph.subscribe(self._on_graph_change)
            self._active = True

    def stop(self) -> None:
        if self._active:
            if self._unsubscribe is not None:
                self._unsubscribe()
            self._unsubscribe = None
            self._active = False

    def _on_graph_change(self, change: GraphChange) -> None:
        self.dispatcher.publish(
            SystemEvent(
                name=GRAPH_CHANGED_EVENT,
                source="live_data_graph",
                payload={
                    "source_id": change.source_id,
                    "affected_ids": change.affected_ids,
                    "revision": change.revision,
                    "reason": change.reason,
                    "metadata": dict(change.metadata),
                },
            )
        )


class ReactivePropertyService(PropertyService):
    """PropertyService con grafo y eventos, sin romper su API original."""

    def __init__(
        self,
        *args: Any,
        graph: LiveDataGraph | None = None,
        dispatcher: EventDispatcher | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.graph = graph if graph is not None else LiveDataGraph()
        self.dispatcher = dispatcher if dispatcher is not None else EventDispatcher()
        self.graph_bridge = GraphEventBridge(self.graph, self.dispatcher)
        self.graph_bridge.start()

    def bind(
        self,
        owner_id: str,
        definition_name: str,
        value: Any = None,
        *,
        source: str = "instance",
        inherited: bool = False,
        calculated: bool = False,
    ):
        property_value = super().bind(
            owner_id,
            definition_name,
            value,
            source=source,
            inherited=inherited,
            calculated=calculated,
        )
        owner_node = self.owner_node_id(owner_id)
        property_node = self.property_node_id(owner_id, definition_name)
        if owner_node not in self.graph:
            self.graph.add_node(owner_node, "property_owner", payload=str(owner_id))
        if property_node in self.graph:
            self.graph.update_payload(
                property_node,
                property_value.value,
                reason="property_rebound",
                metadata={"owner_id": str(owner_id), "property_name": definition_name},
            )
        else:
            self.graph.add_node(
                property_node,
                "property",
                payload=property_value.value,
                metadata={"owner_id": str(owner_id), "property_name": definition_name},
            )
            self.graph.add_dependency(property_node, owner_node)
        self.dispatcher.publish(
            PROPERTY_BOUND_EVENT,
            {
                "owner_id": str(owner_id),
                "property_name": property_value.definition.name,
                "value": property_value.value,
                "node_id": property_node,
            },
            source="property_service",
        )
        return property_value

    def set_value(
        self,
        owner_id: str,
        name: str,
        value: Any,
        *,
        input_unit: str | None = None,
        force: bool = False,
        change_source: str = "property_service",
        metadata: Mapping[str, Any] | None = None,
    ) -> Any:
        property_value = self.require_property(owner_id, name)
        current = property_value.value
        previous = super().set_value(
            owner_id,
            name,
            value,
            input_unit=input_unit,
            force=force,
        )
        new_value = property_value.value
        if current == new_value:
            return previous

        node_id = self.property_node_id(owner_id, name)
        if node_id not in self.graph:
            self._ensure_existing_binding_node(owner_id, name, new_value)
        change = self.graph.update_payload(
            node_id,
            new_value,
            reason="property_changed",
            metadata={
                "owner_id": str(owner_id),
                "property_name": property_value.definition.name,
                "previous_value": previous,
                "new_value": new_value,
                **dict(metadata or {}),
            },
        )
        record = PropertyChangeRecord(
            owner_id=str(owner_id),
            property_name=property_value.definition.name,
            previous_value=previous,
            new_value=new_value,
            graph_revision=change.revision,
            source=change_source,
            metadata=metadata or {},
        )
        self.dispatcher.publish(
            SystemEvent(
                name=PROPERTY_CHANGED_EVENT,
                source=change_source,
                payload=record.to_payload(),
            )
        )
        return previous

    def remove_owner(self, owner_id: str):
        removed = super().remove_owner(owner_id)
        for property_value in removed.values():
            node_id = self.property_node_id(owner_id, property_value.definition.name)
            if node_id in self.graph:
                self.graph.remove_node(node_id)
        owner_node = self.owner_node_id(owner_id)
        if owner_node in self.graph:
            self.graph.remove_node(owner_node)
        if removed:
            self.dispatcher.publish(
                OWNER_REMOVED_EVENT,
                {
                    "owner_id": str(owner_id),
                    "property_names": tuple(
                        item.definition.name for item in removed.values()
                    ),
                },
                source="property_service",
            )
        return removed

    def register_dependent(
        self,
        owner_id: str,
        name: str,
        dependent_id: str,
        *,
        kind: str = "subscriber",
        payload: Any = None,
    ) -> str:
        source_id = self.property_node_id(owner_id, name)
        self.require_property(owner_id, name)
        if source_id not in self.graph:
            self._ensure_existing_binding_node(owner_id, name, self.get_value(owner_id, name))
        if dependent_id not in self.graph:
            self.graph.add_node(dependent_id, kind, payload=payload)
        self.graph.add_dependency(source_id, dependent_id)
        return dependent_id

    def _ensure_existing_binding_node(self, owner_id: str, name: str, value: Any) -> None:
        owner_node = self.owner_node_id(owner_id)
        property_node = self.property_node_id(owner_id, name)
        if owner_node not in self.graph:
            self.graph.add_node(owner_node, "property_owner", payload=str(owner_id))
        if property_node not in self.graph:
            self.graph.add_node(
                property_node,
                "property",
                payload=value,
                metadata={"owner_id": str(owner_id), "property_name": str(name)},
            )
            self.graph.add_dependency(property_node, owner_node)

    @staticmethod
    def owner_node_id(owner_id: str) -> str:
        return f"property-owner:{str(owner_id).strip()}"

    @staticmethod
    def property_node_id(owner_id: str, name: str) -> str:
        return f"property:{str(owner_id).strip()}:{str(name).strip().casefold()}"
