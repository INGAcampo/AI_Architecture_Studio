"""Registro extensible de adaptadores BIM."""

from __future__ import annotations

from typing import Any

from ..document import BimDocument
from ..element import BimElement
from ..relationships import RelationshipType
from .base import BimAdapter
from .native import (
    BeamBimAdapter,
    ColumnBimAdapter,
    DoorBimAdapter,
    FoundationBimAdapter,
    GridBimAdapter,
    LevelBimAdapter,
    RoomBimAdapter,
    SlabBimAdapter,
    WallBimAdapter,
    WindowBimAdapter,
)


class BimAdapterRegistry:
    def __init__(self) -> None:
        self._adapters: list[BimAdapter] = []

    @property
    def adapters(self) -> tuple[BimAdapter, ...]:
        return tuple(self._adapters)

    def register(self, adapter: BimAdapter) -> None:
        if not isinstance(adapter, BimAdapter):
            raise TypeError("El registro solo acepta adaptadores BIM.")
        self._adapters = [
            current
            for current in self._adapters
            if current.__class__ is not adapter.__class__
        ]
        self._adapters.append(adapter)

    def resolve(self, source: Any) -> BimAdapter:
        for adapter in reversed(self._adapters):
            if adapter.supports(source):
                return adapter
        raise TypeError(
            "No existe un adaptador BIM registrado para "
            f"{source.__class__.__module__}.{source.__class__.__name__}."
        )

    def adapt(
        self,
        source: Any,
        *,
        level_id: str | None = None,
    ) -> BimElement:
        return self.resolve(source).to_bim_element(
            source,
            level_id=level_id,
        )

    def add_to_document(
        self,
        document: BimDocument,
        source: Any,
        *,
        level_id: str | None = None,
        infer_relationships: bool = True,
    ) -> BimElement:
        element = self.adapt(source, level_id=level_id)
        document.add_element(element)

        if infer_relationships:
            self._infer_relationships(document, source, element)

        return element

    def _infer_relationships(
        self,
        document: BimDocument,
        source: Any,
        element: BimElement,
    ) -> None:
        host_wall = getattr(source, "host_wall", None)
        if host_wall is not None:
            host_id = _first_identifier(host_wall)
            if host_id and document.get_element(host_id):
                document.relate(
                    host_id,
                    element.element_id,
                    RelationshipType.HOSTS,
                )

        host_room_id = getattr(source, "host_room_id", None)
        if host_room_id and document.get_element(str(host_room_id)):
            document.relate(
                str(host_room_id),
                element.element_id,
                RelationshipType.CONTAINS,
            )


def create_default_bim_adapter_registry() -> BimAdapterRegistry:
    registry = BimAdapterRegistry()
    for adapter_type in (
        LevelBimAdapter,
        GridBimAdapter,
        WallBimAdapter,
        DoorBimAdapter,
        WindowBimAdapter,
        RoomBimAdapter,
        SlabBimAdapter,
        BeamBimAdapter,
        ColumnBimAdapter,
        FoundationBimAdapter,
    ):
        registry.register(adapter_type())
    return registry


def _first_identifier(source: Any) -> str | None:
    for name in (
        "id",
        "door_id",
        "window_id",
        "room_id",
        "slab_id",
    ):
        value = getattr(source, name, None)
        if value:
            return str(value)
    return None
