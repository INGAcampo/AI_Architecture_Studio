"""Canonical CAD entity identities and geometric entity records."""
from __future__ import annotations
from dataclasses import dataclass, field
from math import pi
from uuid import uuid4
from .geometry import Point, BoundingBox

def new_id() -> str:
    """Issue a unique stable identifier for a newly created CAD entity."""
    return uuid4().hex

@dataclass(slots=True)
class Entity:
    """Base drawable carrying identity, layer and common entity metadata."""
    entity_id: str = field(default_factory=new_id)
    layer: str = "0"
    visible: bool = True
    locked: bool = False

    def bbox(self) -> BoundingBox:
        """Execute the public Entity.bbox operation for the S1 professional CAD foundation program using explicit caller inputs."""
        raise NotImplementedError

@dataclass(slots=True)
class Line(Entity):
    """Finite straight segment between two planar points."""
    start: Point = field(default_factory=lambda: Point(0,0))
    end: Point = field(default_factory=lambda: Point(1,0))

    @property
    def length(self) -> float:
        """Execute the public Line.length operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return self.start.distance_to(self.end)

    def bbox(self) -> BoundingBox:
        """Execute the public Line.bbox operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return BoundingBox(
            min(self.start.x,self.end.x), min(self.start.y,self.end.y),
            max(self.start.x,self.end.x), max(self.start.y,self.end.y),
        )

@dataclass(slots=True)
class Circle(Entity):
    """Circular entity defined by center and positive radius."""
    center: Point = field(default_factory=lambda: Point(0,0))
    radius: float = 1.0

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("Radius must be positive.")

    @property
    def area(self) -> float:
        """Execute the public Circle.area operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return pi * self.radius * self.radius

    def bbox(self) -> BoundingBox:
        """Execute the public Circle.bbox operation for the S1 professional CAD foundation program using explicit caller inputs."""
        r=self.radius
        return BoundingBox(self.center.x-r,self.center.y-r,self.center.x+r,self.center.y+r)

@dataclass(slots=True)
class Arc(Entity):
    """Circular arc defined by center, radius and angular interval."""
    center: Point = field(default_factory=lambda: Point(0,0))
    radius: float = 1.0
    start_angle: float = 0.0
    end_angle: float = 90.0

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("Radius must be positive.")

    def bbox(self) -> BoundingBox:
        """Execute the public Arc.bbox operation for the S1 professional CAD foundation program using explicit caller inputs."""
        r=self.radius
        return BoundingBox(self.center.x-r,self.center.y-r,self.center.x+r,self.center.y+r)

@dataclass(slots=True)
class Polyline(Entity):
    """Ordered open or closed chain of planar vertices."""
    points: list[Point] = field(default_factory=list)
    closed: bool = False

    @property
    def length(self) -> float:
        """Execute the public Polyline.length operation for the S1 professional CAD foundation program using explicit caller inputs."""
        if len(self.points) < 2:
            return 0.0
        total=sum(a.distance_to(b) for a,b in zip(self.points,self.points[1:]))
        if self.closed:
            total += self.points[-1].distance_to(self.points[0])
        return total

    def bbox(self) -> BoundingBox:
        """Execute the public Polyline.bbox operation for the S1 professional CAD foundation program using explicit caller inputs."""
        if not self.points:
            return BoundingBox(0,0,0,0)
        xs=[p.x for p in self.points]; ys=[p.y for p in self.points]
        return BoundingBox(min(xs),min(ys),max(xs),max(ys))

@dataclass(slots=True)
class Ellipse(Entity):
    """Elliptical entity defined by center, principal radii and rotation."""
    center: Point = field(default_factory=lambda: Point(0,0))
    radius_x: float = 2.0
    radius_y: float = 1.0

    def __post_init__(self) -> None:
        if self.radius_x <= 0 or self.radius_y <= 0:
            raise ValueError("Ellipse radii must be positive.")

    @property
    def area(self) -> float:
        """Execute the public Ellipse.area operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return pi * self.radius_x * self.radius_y

    def bbox(self) -> BoundingBox:
        """Execute the public Ellipse.bbox operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return BoundingBox(
            self.center.x-self.radius_x, self.center.y-self.radius_y,
            self.center.x+self.radius_x, self.center.y+self.radius_y,
        )

@dataclass(slots=True)
class Polygon(Entity):
    """Closed multi-vertex planar boundary."""
    points: list[Point] = field(default_factory=list)

    def bbox(self) -> BoundingBox:
        """Execute the public Polygon.bbox operation for the S1 professional CAD foundation program using explicit caller inputs."""
        if not self.points:
            return BoundingBox(0,0,0,0)
        xs=[p.x for p in self.points]; ys=[p.y for p in self.points]
        return BoundingBox(min(xs),min(ys),max(xs),max(ys))
