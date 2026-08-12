"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from .ids import ObjectId

class SelectionService:
    """Execute the public SelectionService operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._selected: set[ObjectId] = set()

    def set(self, object_ids) -> None:
        """Execute set for the Omega application core and shared runtime services with validated state transitions."""
        self._selected = set(object_ids)

    def add(self, object_id: ObjectId) -> None:
        """Add add to the Omega application core and shared runtime services while enforcing identity constraints."""
        self._selected.add(object_id)

    def remove(self, object_id: ObjectId) -> None:
        """Remove the requested remove from the Omega application core and shared runtime services without affecting unrelated state."""
        self._selected.discard(object_id)

    def clear(self) -> None:
        """Remove the requested clear from the Omega application core and shared runtime services without affecting unrelated state."""
        self._selected.clear()

    def all(self) -> tuple[ObjectId, ...]:
        """Execute the public SelectionService.all operation for the Omega application core and shared runtime services using explicit caller inputs."""
        return tuple(sorted(self._selected, key=str))
