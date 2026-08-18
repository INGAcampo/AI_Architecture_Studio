"""Endpoint, midpoint, center and intersection object-snap resolution."""
from __future__ import annotations
from dataclasses import dataclass
from .entities import Line, Circle, Polyline
from .geometry import Point

@dataclass(frozen=True, slots=True)
class Snap:
    """Resolved snap coordinate annotated with its geometric kind."""
    point: Point
    kind: str
    entity_id: str

class SnapEngine:
    """Collect and prioritize precise construction points near the cursor."""
    def candidates(self, entity):
        """Execute the public SnapEngine.candidates operation for the S1 professional CAD foundation program using explicit caller inputs."""
        if isinstance(entity,Line):
            midpoint=Point((entity.start.x+entity.end.x)/2,(entity.start.y+entity.end.y)/2)
            return (
                Snap(entity.start,"endpoint",entity.entity_id),
                Snap(entity.end,"endpoint",entity.entity_id),
                Snap(midpoint,"midpoint",entity.entity_id),
            )
        if isinstance(entity,Circle):
            c=entity.center; r=entity.radius
            return (
                Snap(c,"center",entity.entity_id),
                Snap(Point(c.x+r,c.y),"quadrant",entity.entity_id),
                Snap(Point(c.x-r,c.y),"quadrant",entity.entity_id),
                Snap(Point(c.x,c.y+r),"quadrant",entity.entity_id),
                Snap(Point(c.x,c.y-r),"quadrant",entity.entity_id),
            )
        if isinstance(entity,Polyline):
            return tuple(Snap(p,"vertex",entity.entity_id) for p in entity.points)
        return ()

    def nearest(self, point, entities, tolerance):
        """Execute the public SnapEngine.nearest operation for the S1 professional CAD foundation program using explicit caller inputs."""
        best=None; distance=float("inf")
        for entity in entities:
            for candidate in self.candidates(entity):
                d=point.distance_to(candidate.point)
                if d <= tolerance and d < distance:
                    best=candidate; distance=d
        return best
