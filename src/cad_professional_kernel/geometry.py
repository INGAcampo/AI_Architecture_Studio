from __future__ import annotations
from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class Point2D:
    x: float
    y: float

    def distance_to(self, other: "Point2D") -> float:
        return hypot(other.x - self.x, other.y - self.y)

@dataclass(frozen=True, slots=True)
class Vector2D:
    x: float
    y: float

    @property
    def length(self) -> float:
        return hypot(self.x, self.y)

    def normalized(self) -> "Vector2D":
        size = self.length
        if size == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return Vector2D(self.x / size, self.y / size)
