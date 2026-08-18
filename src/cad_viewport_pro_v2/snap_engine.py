from dataclasses import dataclass
from cad_professional_kernel.entities import CadLine, CadCircle, CadPolyline
from cad_professional_kernel.geometry import Point2D

@dataclass(frozen=True, slots=True)
class SnapCandidate:
    point: Point2D
    kind: str
    entity_id: str

class ProfessionalSnapEngine:
    def candidates(self, entity) -> tuple[SnapCandidate, ...]:
        if isinstance(entity, CadLine):
            mid = Point2D((entity.start.x+entity.end.x)/2, (entity.start.y+entity.end.y)/2)
            return (
                SnapCandidate(entity.start, "endpoint", entity.entity_id),
                SnapCandidate(entity.end, "endpoint", entity.entity_id),
                SnapCandidate(mid, "midpoint", entity.entity_id),
            )
        if isinstance(entity, CadCircle):
            c=entity.center; r=entity.radius
            return (
                SnapCandidate(c,"center",entity.entity_id),
                SnapCandidate(Point2D(c.x+r,c.y),"quadrant",entity.entity_id),
                SnapCandidate(Point2D(c.x-r,c.y),"quadrant",entity.entity_id),
                SnapCandidate(Point2D(c.x,c.y+r),"quadrant",entity.entity_id),
                SnapCandidate(Point2D(c.x,c.y-r),"quadrant",entity.entity_id),
            )
        if isinstance(entity, CadPolyline):
            return tuple(SnapCandidate(p,"vertex",entity.entity_id) for p in entity.points)
        return ()

    def nearest(self, point: Point2D, entities, tolerance_world: float):
        best=None
        best_distance=float("inf")
        for entity in entities:
            for candidate in self.candidates(entity):
                distance=point.distance_to(candidate.point)
                if distance <= tolerance_world and distance < best_distance:
                    best=candidate
                    best_distance=distance
        return best
