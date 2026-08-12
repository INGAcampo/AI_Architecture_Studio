from dataclasses import dataclass
from cad_professional_kernel.entities import CadCircle, CadLine, CadPolyline
from cad_professional_kernel.geometry import Point2D

@dataclass(frozen=True, slots=True)
class Grip:
    point: Point2D
    kind: str
    entity_id: str
    index: int = -1

class GripEngine:
    def grips(self, entity):
        if isinstance(entity, CadLine):
            mid=Point2D((entity.start.x+entity.end.x)/2,(entity.start.y+entity.end.y)/2)
            return (
                Grip(entity.start,"start",entity.entity_id,0),
                Grip(mid,"midpoint",entity.entity_id,1),
                Grip(entity.end,"end",entity.entity_id,2),
            )
        if isinstance(entity, CadCircle):
            c=entity.center; r=entity.radius
            return (
                Grip(c,"center",entity.entity_id,0),
                Grip(Point2D(c.x+r,c.y),"radius",entity.entity_id,1),
            )
        if isinstance(entity, CadPolyline):
            return tuple(Grip(p,"vertex",entity.entity_id,i) for i,p in enumerate(entity.points))
        return ()
