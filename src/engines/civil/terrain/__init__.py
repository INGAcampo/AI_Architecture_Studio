from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TerrainPoint:
    point_id: str
    x: float
    y: float
    z: float

    def __post_init__(self):
        if not self.point_id.strip():
            raise ValueError("point_id obligatorio")

class DigitalTerrainModel:
    def __init__(self, points):
        self.points = tuple(points)
        if len(self.points) < 3:
            raise ValueError("Se requieren al menos tres puntos")

    def elevation_range(self):
        elevations = [point.z for point in self.points]
        return min(elevations), max(elevations)

    def average_elevation(self):
        return sum(point.z for point in self.points) / len(self.points)

    def nearest_point(self, x, y):
        return min(
            self.points,
            key=lambda point: (point.x-x)**2 + (point.y-y)**2,
        )
