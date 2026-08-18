from __future__ import annotations

from typing import Any

from .types import ConstraintDefinition, ConstraintPoint, ConstraintSegment


class ConstraintGeometryStore:
    def __init__(self) -> None:
        self._objects: dict[str, dict[str, Any]] = {}
        self.revision = 0

    def set_element(self, object_id: str, element: str, value: Any) -> None:
        if not object_id.strip() or not element.strip():
            raise ValueError("object_id y element son obligatorios")
        bucket = self._objects.setdefault(object_id, {})
        if bucket.get(element) != value:
            bucket[element] = value
            self.revision += 1

    def get_element(self, object_id: str, element: str) -> Any:
        try:
            return self._objects[object_id][element]
        except KeyError as exc:
            raise KeyError(f"Elemento desconocido: {object_id}.{element}") from exc

    def remove_object(self, object_id: str) -> bool:
        if object_id not in self._objects:
            return False
        self._objects.pop(object_id)
        self.revision += 1
        return True

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return {
            object_id: dict(elements)
            for object_id, elements in sorted(self._objects.items())
        }


class ConstraintRepository:
    def __init__(self) -> None:
        self._constraints: dict[str, ConstraintDefinition] = {}
        self.revision = 0

    def add(self, constraint: ConstraintDefinition, *, replace: bool = False) -> None:
        if constraint.constraint_id in self._constraints and not replace:
            raise KeyError(f"Restricción ya existente: {constraint.constraint_id}")
        self._constraints[constraint.constraint_id] = constraint
        self.revision += 1

    def get(self, constraint_id: str) -> ConstraintDefinition:
        try:
            return self._constraints[constraint_id]
        except KeyError as exc:
            raise KeyError(f"Restricción desconocida: {constraint_id}") from exc

    def remove(self, constraint_id: str) -> ConstraintDefinition:
        constraint = self.get(constraint_id)
        self._constraints.pop(constraint_id)
        self.revision += 1
        return constraint

    def all(self) -> tuple[ConstraintDefinition, ...]:
        return tuple(
            sorted(
                self._constraints.values(),
                key=lambda c: (c.priority, c.constraint_id),
            )
        )

    def enabled(self) -> tuple[ConstraintDefinition, ...]:
        return tuple(c for c in self.all() if c.enabled)

    def for_object(self, object_id: str) -> tuple[ConstraintDefinition, ...]:
        return tuple(
            c for c in self.all()
            if any(target.object_id == object_id for target in c.targets)
        )
