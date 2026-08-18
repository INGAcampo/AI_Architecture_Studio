from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class AdaptivePoint:
    point_id:str;x:float;y:float;z:float=0.0
@dataclass(frozen=True,slots=True)
class AdaptiveComponent:
    component_id:str;points:tuple[AdaptivePoint,...]
class AdaptiveComponentEngine:
    def centroid(self,c):
        n=len(c.points);return (sum(p.x for p in c.points)/n,sum(p.y for p in c.points)/n,sum(p.z for p in c.points)/n)
    def move_point(self,c,pid,x,y,z=0):
        pts=tuple(AdaptivePoint(p.point_id,x,y,z) if p.point_id==pid else p for p in c.points)
        return AdaptiveComponent(c.component_id,pts)
