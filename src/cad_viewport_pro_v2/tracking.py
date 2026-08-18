from dataclasses import dataclass
from math import atan2, cos, radians, sin, hypot
from cad_professional_kernel.geometry import Point2D

@dataclass(frozen=True, slots=True)
class TrackingResult:
    point: Point2D
    mode: str
    angle_degrees: float | None = None

class TrackingEngine:
    def ortho(self, origin: Point2D, target: Point2D) -> TrackingResult:
        dx = target.x-origin.x
        dy = target.y-origin.y
        if abs(dx) >= abs(dy):
            return TrackingResult(Point2D(target.x, origin.y), "ortho", 0.0)
        return TrackingResult(Point2D(origin.x, target.y), "ortho", 90.0)

    def polar(self, origin: Point2D, target: Point2D, increment_degrees: float = 15.0) -> TrackingResult:
        dx = target.x-origin.x
        dy = target.y-origin.y
        length = hypot(dx,dy)
        if length == 0:
            return TrackingResult(target, "polar", 0.0)
        angle = atan2(dy,dx) * 180.0 / 3.141592653589793
        snapped = round(angle/increment_degrees)*increment_degrees
        rad = radians(snapped)
        return TrackingResult(Point2D(origin.x+length*cos(rad), origin.y+length*sin(rad)), "polar", snapped)
