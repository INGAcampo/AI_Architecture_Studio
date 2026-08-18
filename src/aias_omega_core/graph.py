"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass
from .ids import ObjectId

@dataclass(frozen=True, slots=True)
class Relationship:
    """Execute the public Relationship operation for the Omega application core and shared runtime services using explicit caller inputs."""
    source: ObjectId
    target: ObjectId
    relation_type: str

class ObjectGraph:
    """Execute the public ObjectGraph operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._relationships: set[Relationship] = set()

    def add(self, relationship: Relationship) -> None:
        """Add add to the Omega application core and shared runtime services while enforcing identity constraints."""
        self._relationships.add(relationship)

    def remove(self, relationship: Relationship) -> None:
        """Remove the requested remove from the Omega application core and shared runtime services without affecting unrelated state."""
        self._relationships.discard(relationship)

    def outgoing(self, source: ObjectId, relation_type: str | None = None) -> tuple[Relationship, ...]:
        """Execute the public ObjectGraph.outgoing operation for the Omega application core and shared runtime services using explicit caller inputs."""
        return tuple(
            item for item in self._relationships
            if item.source == source and (relation_type is None or item.relation_type == relation_type)
        )

    def incoming(self, target: ObjectId, relation_type: str | None = None) -> tuple[Relationship, ...]:
        """Execute the public ObjectGraph.incoming operation for the Omega application core and shared runtime services using explicit caller inputs."""
        return tuple(
            item for item in self._relationships
            if item.target == target and (relation_type is None or item.relation_type == relation_type)
        )

    def all(self) -> tuple[Relationship, ...]:
        """Execute the public ObjectGraph.all operation for the Omega application core and shared runtime services using explicit caller inputs."""
        return tuple(self._relationships)
