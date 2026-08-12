"""Relaciones explícitas entre elementos BIM."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
from uuid import uuid4


class RelationshipType(str, Enum):
    CONTAINS = "contains"
    HOSTS = "hosts"
    CONNECTS = "connects"
    REFERENCES = "references"
    ASSIGNED_TO = "assigned_to"
    GROUPS = "groups"


@dataclass(frozen=True)
class BimRelationship:
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    relationship_id: str = ""
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.source_id or not self.target_id:
            raise ValueError("Una relación BIM requiere origen y destino.")
        if self.source_id == self.target_id:
            raise ValueError("Una relación BIM no puede apuntar al mismo elemento.")
        if not self.relationship_id:
            object.__setattr__(self, "relationship_id", str(uuid4()))
        object.__setattr__(
            self,
            "relationship_type",
            RelationshipType(self.relationship_type),
        )
        object.__setattr__(self, "metadata", dict(self.metadata or {}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "relationship_id": self.relationship_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
            "metadata": dict(self.metadata or {}),
        }
