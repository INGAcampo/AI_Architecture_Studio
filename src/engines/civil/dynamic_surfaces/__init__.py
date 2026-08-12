from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SurfacePoint:
    x: float
    y: float
    z: float

class DynamicSurface:
    def __init__(self, points):
        self.points = tuple(points)
        if len(self.points) < 3:
            raise ValueError("Se requieren tres puntos")

    def average_elevation(self):
        return sum(p.z for p in self.points)/len(self.points)

    def update_point(self, index, point):
        values = list(self.points)
        values[index] = point
        return DynamicSurface(values)
