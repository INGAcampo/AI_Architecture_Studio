"""Documento BIM nativo, independiente de la interfaz gráfica."""

from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .categories import BimCategory
from .element import BimElement
from .relationships import BimRelationship, RelationshipType
from .schema import BIM_SCHEMA_VERSION


@dataclass
class BimDocument:
    name: str = "Proyecto BIM"
    document_id: str = field(default_factory=lambda: str(uuid4()))
    schema_version: str = BIM_SCHEMA_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.name = str(self.name).strip() or "Proyecto BIM"
        self._elements: dict[str, BimElement] = {}
        self._relationships: dict[str, BimRelationship] = {}
        self.metadata = dict(self.metadata or {})

    @property
    def element_count(self) -> int:
        return len(self._elements)

    @property
    def relationship_count(self) -> int:
        return len(self._relationships)

    def add_element(self, element: BimElement) -> BimElement:
        if not isinstance(element, BimElement):
            raise TypeError("Solo se pueden registrar objetos BimElement.")
        if element.element_id in self._elements:
            raise ValueError(
                f"Ya existe el elemento BIM {element.element_id!r}."
            )
        self._elements[element.element_id] = element
        return element

    def add_aias_object(
        self,
        source: Any,
        *,
        category: BimCategory | str | None = None,
        level_id: str | None = None,
    ) -> BimElement:
        element = BimElement.from_aias_object(
            source,
            category=category,
            level_id=level_id,
        )
        return self.add_element(element)

    def get_element(self, element_id: str) -> BimElement | None:
        return self._elements.get(str(element_id))

    def require_element(self, element_id: str) -> BimElement:
        element = self.get_element(element_id)
        if element is None:
            raise KeyError(f"Elemento BIM no encontrado: {element_id}")
        return element

    def remove_element(self, element_id: str) -> BimElement:
        element = self.require_element(element_id)
        del self._elements[element.element_id]

        orphan_relationships = [
            relationship_id
            for relationship_id, relationship in self._relationships.items()
            if element.element_id in {
                relationship.source_id,
                relationship.target_id,
            }
        ]
        for relationship_id in orphan_relationships:
            del self._relationships[relationship_id]

        return element

    def elements(
        self,
        *,
        category: BimCategory | str | None = None,
        level_id: str | None = None,
    ) -> tuple[BimElement, ...]:
        values: Iterable[BimElement] = self._elements.values()

        if category is not None:
            resolved = BimCategory.coerce(category)
            values = (
                element
                for element in values
                if element.category is resolved
            )

        if level_id is not None:
            values = (
                element
                for element in values
                if element.level_id == level_id
            )

        return tuple(values)

    def relate(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType | str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> BimRelationship:
        self.require_element(source_id)
        self.require_element(target_id)

        relationship = BimRelationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=RelationshipType(relationship_type),
            metadata=metadata,
        )
        self._relationships[relationship.relationship_id] = relationship
        return relationship

    def relationships_for(
        self,
        element_id: str,
    ) -> tuple[BimRelationship, ...]:
        self.require_element(element_id)
        return tuple(
            relationship
            for relationship in self._relationships.values()
            if element_id in {
                relationship.source_id,
                relationship.target_id,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "name": self.name,
            "schema_version": self.schema_version,
            "metadata": deepcopy(self.metadata),
            "elements": [
                element.to_dict()
                for element in self._elements.values()
            ],
            "relationships": [
                relationship.to_dict()
                for relationship in self._relationships.values()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BimDocument":
        document = cls(
            document_id=data["document_id"],
            name=data["name"],
            schema_version=data.get(
                "schema_version",
                BIM_SCHEMA_VERSION,
            ),
            metadata=data.get("metadata", {}),
        )

        for element_data in data.get("elements", []):
            document.add_element(BimElement.from_dict(element_data))

        for relation_data in data.get("relationships", []):
            relation = BimRelationship(
                relationship_id=relation_data["relationship_id"],
                source_id=relation_data["source_id"],
                target_id=relation_data["target_id"],
                relationship_type=relation_data["relationship_type"],
                metadata=relation_data.get("metadata", {}),
            )
            document._relationships[relation.relationship_id] = relation

        return document
