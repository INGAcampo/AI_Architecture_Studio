"""Validated polygon representation and deterministic planar properties."""
from __future__ import annotations
from dataclasses import dataclass
from .primitives import Point2D, BoundingBox2D

@dataclass(frozen=True, slots=True)
class Polygon2D:
    """Ordered closed planar boundary with area, centroid and containment operations."""
    vertices: tuple[Point2D, ...]
    def __post_init__(self):
        if len(self.vertices) < 3:
            raise ValueError("polygon_requires_three_vertices")

    @property
    def signed_area(self) -> float:
        """Return orientation-sensitive area using the shoelace formula."""
        pts = self.vertices
        return 0.5*sum(
            pts[i].x*pts[(i+1)%len(pts)].y - pts[(i+1)%len(pts)].x*pts[i].y
            for i in range(len(pts))
        )

    @property
    def area(self) -> float:
        """Return the nonnegative planar polygon area."""
        return abs(self.signed_area)

    @property
    def perimeter(self) -> float:
        """Return the sum of closed boundary edge lengths."""
        pts = self.vertices
        return sum(pts[i].distance_to(pts[(i+1)%len(pts)]) for i in range(len(pts)))

    @property
    def centroid(self) -> Point2D:
        """Return the area-weighted centroid of a nondegenerate polygon."""
        a = self.signed_area
        if abs(a) < 1e-15:
            raise ValueError("degenerate_polygon")
        pts = self.vertices
        cx = sum((pts[i].x+pts[(i+1)%len(pts)].x) *
                 (pts[i].x*pts[(i+1)%len(pts)].y-pts[(i+1)%len(pts)].x*pts[i].y)
                 for i in range(len(pts))) / (6*a)
        cy = sum((pts[i].y+pts[(i+1)%len(pts)].y) *
                 (pts[i].x*pts[(i+1)%len(pts)].y-pts[(i+1)%len(pts)].x*pts[i].y)
                 for i in range(len(pts))) / (6*a)
        return Point2D(cx,cy)

    @property
    def bounding_box(self) -> BoundingBox2D:
        """Return the smallest axis-aligned box containing all vertices."""
        xs = [p.x for p in self.vertices]
        ys = [p.y for p in self.vertices]
        return BoundingBox2D(Point2D(min(xs),min(ys)),Point2D(max(xs),max(ys)))

    def contains(self, point: Point2D) -> bool:
        """Test point inclusion using a deterministic ray-crossing rule."""
        inside = False
        pts = self.vertices
        j = len(pts)-1
        for i in range(len(pts)):
            pi, pj = pts[i], pts[j]
            intersects = ((pi.y > point.y) != (pj.y > point.y)) and (
                point.x < (pj.x-pi.x)*(point.y-pi.y)/(pj.y-pi.y) + pi.x
            )
            if intersects:
                inside = not inside
            j = i
        return inside
