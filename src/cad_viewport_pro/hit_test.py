from cad_professional_kernel.entities import CadCircle, CadLine, CadPolyline
from cad_professional_kernel.geometry import Point2D

def point_segment_distance(p, a, b):
    vx, vy = b.x-a.x, b.y-a.y
    wx, wy = p.x-a.x, p.y-a.y
    c2 = vx*vx + vy*vy
    if c2 == 0:
        return p.distance_to(a)
    t = max(0.0, min(1.0, (wx*vx+wy*vy)/c2))
    q = Point2D(a.x+t*vx, a.y+t*vy)
    return p.distance_to(q)

class HitTester:
    def hit(self, entity, point, tolerance):
        if isinstance(entity, CadLine):
            return point_segment_distance(point,entity.start,entity.end) <= tolerance
        if isinstance(entity, CadCircle):
            return abs(point.distance_to(entity.center)-entity.radius) <= tolerance
        if isinstance(entity, CadPolyline):
            pairs=list(zip(entity.points,entity.points[1:]))
            if entity.closed and len(entity.points)>2:
                pairs.append((entity.points[-1],entity.points[0]))
            return any(point_segment_distance(point,a,b)<=tolerance for a,b in pairs)
        return False
