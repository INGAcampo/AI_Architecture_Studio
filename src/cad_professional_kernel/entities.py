from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
from .geometry import Point2D

def new_id() -> str:
    return uuid4().hex

@dataclass(slots=True)
class CadEntity:
    entity_id: str = field(default_factory=new_id)
    layer: str = "0"
    visible: bool = True
    locked: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class CadLine(CadEntity):
    start: Point2D = field(default_factory=lambda: Point2D(0.0, 0.0))
    end: Point2D = field(default_factory=lambda: Point2D(1.0, 0.0))

    @property
    def length(self) -> float:
        return self.start.distance_to(self.end)

@dataclass(slots=True)
class CadCircle(CadEntity):
    center: Point2D = field(default_factory=lambda: Point2D(0.0, 0.0))
    radius: float = 1.0

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("Radius must be positive.")

@dataclass(slots=True)
class CadPolyline(CadEntity):
    points: list[Point2D] = field(default_factory=list)
    closed: bool = False

    @property
    def length(self) -> float:
        if len(self.points) < 2:
            return 0.0
        total = sum(a.distance_to(b) for a, b in zip(self.points, self.points[1:]))
        if self.closed:
            total += self.points[-1].distance_to(self.points[0])
        return total
