from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any


class ConstraintKind(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    PARALLEL = "parallel"
    PERPENDICULAR = "perpendicular"
    COINCIDENT = "coincident"
    EQUAL_LENGTH = "equal_length"
    LOCK_POINT = "lock_point"
    DISTANCE = "distance"
    OFFSET = "offset"


class ConstraintStatus(str, Enum):
    PENDING = "pending"
    SATISFIED = "satisfied"
    VIOLATED = "violated"
    CONFLICT = "conflict"
    DISABLED = "disabled"


@dataclass(frozen=True, slots=True)
class ConstraintPoint:
    x: float
    y: float
    z: float = 0.0

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.x, self.y, self.z)):
            raise ValueError("Las coordenadas deben ser finitas")

    def moved(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> "ConstraintPoint":
        return ConstraintPoint(self.x + dx, self.y + dy, self.z + dz)


@dataclass(frozen=True, slots=True)
class ConstraintSegment:
    start: ConstraintPoint
    end: ConstraintPoint

    @property
    def dx(self) -> float:
        return self.end.x - self.start.x

    @property
    def dy(self) -> float:
        return self.end.y - self.start.y

    @property
    def dz(self) -> float:
        return self.end.z - self.start.z

    @property
    def length_squared(self) -> float:
        return self.dx ** 2 + self.dy ** 2 + self.dz ** 2

    @property
    def length(self) -> float:
        return self.length_squared ** 0.5


@dataclass(frozen=True, slots=True)
class ConstraintTarget:
    object_id: str
    element: str

    def __post_init__(self) -> None:
        if not self.object_id.strip():
            raise ValueError("object_id no puede estar vacío")
        if not self.element.strip():
            raise ValueError("element no puede estar vacío")


@dataclass(slots=True)
class ConstraintDefinition:
    constraint_id: str
    kind: ConstraintKind
    targets: tuple[ConstraintTarget, ...]
    value: float | None = None
    enabled: bool = True
    priority: int = 100
    metadata: dict[str, Any] = field(default_factory=dict)
    status: ConstraintStatus = ConstraintStatus.PENDING
    message: str | None = None

    def __post_init__(self) -> None:
        if not self.constraint_id.strip():
            raise ValueError("constraint_id no puede estar vacío")
        if not self.targets:
            raise ValueError("La restricción requiere al menos un target")
        if self.priority < 0:
            raise ValueError("priority no puede ser negativa")
        if self.value is not None and not isfinite(self.value):
            raise ValueError("value debe ser finito")

    def snapshot(self) -> dict[str, Any]:
        return {
            "constraint_id": self.constraint_id,
            "kind": self.kind.value,
            "targets": [
                {"object_id": t.object_id, "element": t.element}
                for t in self.targets
            ],
            "value": self.value,
            "enabled": self.enabled,
            "priority": self.priority,
            "metadata": dict(self.metadata),
            "status": self.status.value,
            "message": self.message,
        }
