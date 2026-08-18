"""Servicio BIM central para el documento activo de AIAS."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..adapters import BimAdapterRegistry, create_default_bim_adapter_registry
from ..document import BimDocument
from ..element import BimElement
from ..relationships import BimRelationship, RelationshipType
from .dispatcher import BimEventDispatcher
from .events import BimEvent, BimEventName
from .parameter_manager import BimParameterManager
from .relationship_manager import BimRelationshipManager
from .repository import BimDocumentRepository


class BimService:
    """Fachada estable para registrar, consultar y persistir BIM."""

    def __init__(
        self,
        document: BimDocument | None = None,
        *,
        adapter_registry: BimAdapterRegistry | None = None,
        event_bus: Any | None = None,
        repository: BimDocumentRepository | None = None,
    ) -> None:
        self._document = document or BimDocument()
        self.adapters = adapter_registry or create_default_bim_adapter_registry()
        self.events = BimEventDispatcher(event_bus)
        self.repository = repository or BimDocumentRepository()
        self._source_objects: dict[str, Any] = {}
        self._refresh_managers()

    @property
    def document(self) -> BimDocument:
        return self._document

    @property
    def element_count(self) -> int:
        return self._document.element_count

    def register(
        self,
        source: Any,
        *,
        level_id: str | None = None,
        infer_relationships: bool = True,
    ) -> BimElement:
        candidate = (
            source
            if isinstance(source, BimElement)
            else self.adapters.adapt(source, level_id=level_id)
        )

        existing = self._document.get_element(candidate.element_id)
        if existing is not None:
            return self.update(
                source,
                level_id=level_id,
                infer_relationships=infer_relationships,
            )

        self._document.add_element(candidate)
        if not isinstance(source, BimElement):
            self._source_objects[candidate.element_id] = source

        if infer_relationships and not isinstance(source, BimElement):
            self._infer_relationships(source, candidate)

        self._emit(BimEventName.ELEMENT_REGISTERED, candidate.element_id)
        self._emit(BimEventName.DOCUMENT_CHANGED, candidate.element_id)
        return candidate

    def register_many(
        self,
        sources: list[Any] | tuple[Any, ...],
        *,
        level_id: str | None = None,
    ) -> tuple[BimElement, ...]:
        return tuple(
            self.register(source, level_id=level_id)
            for source in sources
        )

    def find(self, element_id: str) -> BimElement | None:
        return self._document.get_element(element_id)

    def require(self, element_id: str) -> BimElement:
        return self._document.require_element(element_id)

    def update(
        self,
        source: Any,
        *,
        level_id: str | None = None,
        infer_relationships: bool = True,
    ) -> BimElement:
        candidate = (
            source
            if isinstance(source, BimElement)
            else self.adapters.adapt(source, level_id=level_id)
        )
        current = self._document.require_element(candidate.element_id)

        current.name = candidate.name
        current.category = candidate.category
        current.type_name = candidate.type_name
        current.level_id = candidate.level_id
        current.geometry_ref = candidate.geometry_ref
        current.source_object_id = candidate.source_object_id
        current.parameters = candidate.parameters
        current.metadata = candidate.metadata

        if not isinstance(source, BimElement):
            self._source_objects[current.element_id] = source
            if infer_relationships:
                self._infer_relationships(source, current)

        self._emit(BimEventName.ELEMENT_UPDATED, current.element_id)
        self._emit(BimEventName.DOCUMENT_CHANGED, current.element_id)
        return current

    def remove(self, element_id: str) -> BimElement:
        removed = self._document.remove_element(element_id)
        self._source_objects.pop(removed.element_id, None)
        self._emit(BimEventName.ELEMENT_REMOVED, removed.element_id)
        self._emit(BimEventName.DOCUMENT_CHANGED, removed.element_id)
        return removed

    def set_parameter(
        self,
        element_id: str,
        name: str,
        value: Any,
        *,
        unit: str | None = None,
        group: str = "General",
        sync_source: bool = True,
    ) -> Any:
        previous = self.parameters.set(
            element_id,
            name,
            value,
            unit=unit,
            group=group,
        )

        if sync_source:
            source = self._source_objects.get(element_id)
            properties = getattr(source, "properties", None)
            if isinstance(properties, dict):
                properties[name] = value

        self._emit(
            BimEventName.PARAMETER_CHANGED,
            element_id,
            {"name": name, "value": value, "previous": previous},
        )
        self._emit(BimEventName.DOCUMENT_CHANGED, element_id)
        return previous

    def relate(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType | str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> BimRelationship:
        relationship = self.relationships.create(
            source_id,
            target_id,
            relationship_type,
            metadata=metadata,
        )
        self._emit(
            BimEventName.RELATIONSHIP_CREATED,
            source_id,
            {"relationship": relationship.to_dict()},
        )
        self._emit(BimEventName.DOCUMENT_CHANGED, source_id)
        return relationship

    def save(self, path: str | Path) -> Path:
        saved = self.repository.save(self._document, path)
        self._emit(
            BimEventName.DOCUMENT_SAVED,
            payload={"path": str(saved)},
        )
        return saved

    def load(self, path: str | Path) -> BimDocument:
        self._document = self.repository.load(path)
        self._source_objects.clear()
        self._refresh_managers()
        self._emit(
            BimEventName.DOCUMENT_LOADED,
            payload={"path": str(path)},
        )
        self._emit(BimEventName.DOCUMENT_CHANGED)
        return self._document

    def new_document(self, name: str = "Proyecto BIM") -> BimDocument:
        self._document = BimDocument(name)
        self._source_objects.clear()
        self._refresh_managers()
        self._emit(BimEventName.DOCUMENT_CHANGED)
        return self._document

    def _refresh_managers(self) -> None:
        self.parameters = BimParameterManager(self._document)
        self.relationships = BimRelationshipManager(self._document)

    def _infer_relationships(
        self,
        source: Any,
        element: BimElement,
    ) -> None:
        host_wall = getattr(source, "host_wall", None)
        if host_wall is not None:
            host_id = _source_identifier(host_wall)
            if host_id and self._document.get_element(host_id):
                self.relationships.create(
                    host_id,
                    element.element_id,
                    RelationshipType.HOSTS,
                )

        host_room_id = getattr(source, "host_room_id", None)
        if host_room_id and self._document.get_element(str(host_room_id)):
            self.relationships.create(
                str(host_room_id),
                element.element_id,
                RelationshipType.CONTAINS,
            )

    def _emit(
        self,
        name: BimEventName,
        element_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.events.emit(
            BimEvent(
                name=name,
                document_id=self._document.document_id,
                element_id=element_id,
                payload=payload,
            )
        )


def _source_identifier(source: Any) -> str | None:
    for name in (
        "id",
        "door_id",
        "window_id",
        "room_id",
        "slab_id",
        "beam_id",
        "column_id",
        "foundation_id",
    ):
        value = getattr(source, name, None)
        if value:
            return str(value)
    return None
