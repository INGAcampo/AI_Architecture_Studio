"""Administración centralizada de relaciones BIM."""

from __future__ import annotations

from typing import Any

from ..document import BimDocument
from ..relationships import BimRelationship, RelationshipType


class BimRelationshipManager:
    def __init__(self, document: BimDocument) -> None:
        self.document = document

    def create(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType | str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> BimRelationship:
        resolved = RelationshipType(relationship_type)
        for relationship in self.document.relationships_for(source_id):
            if (
                relationship.source_id == source_id
                and relationship.target_id == target_id
                and relationship.relationship_type is resolved
            ):
                return relationship
        return self.document.relate(
            source_id,
            target_id,
            resolved,
            metadata=metadata,
        )

    def for_element(self, element_id: str) -> tuple[BimRelationship, ...]:
        return self.document.relationships_for(element_id)
