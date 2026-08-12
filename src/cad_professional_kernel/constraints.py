from __future__ import annotations
from dataclasses import dataclass
from .geometry import Point2D

@dataclass(frozen=True, slots=True)
class HorizontalConstraint:
    start: Point2D
    end: Point2D

    def apply(self) -> tuple[Point2D, Point2D]:
        return self.start, Point2D(self.end.x, self.start.y)

@dataclass(frozen=True, slots=True)
class VerticalConstraint:
    start: Point2D
    end: Point2D

    def apply(self) -> tuple[Point2D, Point2D]:
        return self.start, Point2D(self.start.x, self.end.y)
