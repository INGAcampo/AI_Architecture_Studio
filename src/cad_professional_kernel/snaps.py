from __future__ import annotations
from dataclasses import dataclass
from .entities import CadLine, CadCircle, CadEntity
from .geometry import Point2D

@dataclass(frozen=True, slots=True)
class SnapResult:
    point: Point2D
    kind: str
    entity_id: str

class SnapEngine:
    def endpoints(self, entity: CadEntity) -> tuple[SnapResult, ...]:
        if isinstance(entity, CadLine):
            return (
                SnapResult(entity.start, "endpoint", entity.entity_id),
                SnapResult(entity.end, "endpoint", entity.entity_id),
            )
        return ()

    def center(self, entity: CadEntity) -> tuple[SnapResult, ...]:
        if isinstance(entity, CadCircle):
            return (SnapResult(entity.center, "center", entity.entity_id),)
        return ()

    def nearest(self, cursor: Point2D, candidates: tuple[SnapResult, ...]) -> SnapResult | None:
        if not candidates:
            return None
        return min(candidates, key=lambda result: cursor.distance_to(result.point))
