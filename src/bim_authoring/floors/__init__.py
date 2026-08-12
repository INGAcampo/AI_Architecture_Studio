from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class FloorLayer:
    layer_id: str
    material_id: str
    thickness: float
    function: str = "structure"

@dataclass(frozen=True, slots=True)
class FloorType:
    type_id: str
    name: str
    layers: tuple[FloorLayer, ...]

    @property
    def thickness(self):
        return sum(layer.thickness for layer in self.layers)

@dataclass(frozen=True, slots=True)
class FloorProfile:
    outer: tuple[tuple[float, float], ...]
    openings: tuple[tuple[tuple[float, float], ...], ...] = ()

@dataclass(frozen=True, slots=True)
class FloorInstance:
    floor_id: str
    floor_type: FloorType
    profile: FloorProfile
    elevation: float
    revision: int = 0

@dataclass(frozen=True, slots=True)
class FloorQuantities:
    gross_area: float
    opening_area: float
    net_area: float
    perimeter: float
    volume: float

class NativeBimFloorEngine:
    def polygon_area(self, points):
        return abs(sum(
            points[i][0]*points[(i+1)%len(points)][1] -
            points[(i+1)%len(points)][0]*points[i][1]
            for i in range(len(points))
        )) / 2

    def perimeter(self, points):
        return sum(
            hypot(
                points[(i+1)%len(points)][0]-points[i][0],
                points[(i+1)%len(points)][1]-points[i][1],
            )
            for i in range(len(points))
        )

    def quantities(self, floor):
        gross = self.polygon_area(floor.profile.outer)
        openings = sum(self.polygon_area(loop) for loop in floor.profile.openings)
        net = max(0.0, gross-openings)
        return FloorQuantities(
            gross, openings, net,
            self.perimeter(floor.profile.outer),
            net * floor.floor_type.thickness,
        )

    def validate(self, floor):
        issues = []
        if len(floor.profile.outer) < 3:
            issues.append("invalid_profile")
        if floor.floor_type.thickness <= 0:
            issues.append("invalid_thickness")
        return tuple(issues)
