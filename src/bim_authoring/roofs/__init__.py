from dataclasses import dataclass
from math import cos, radians

@dataclass(frozen=True, slots=True)
class RoofType:
    type_id: str
    name: str
    thickness: float
    material_id: str

@dataclass(frozen=True, slots=True)
class RoofInstance:
    roof_id: str
    roof_type: RoofType
    footprint_area: float
    slope_degrees: float
    elevation: float

@dataclass(frozen=True, slots=True)
class RoofQuantities:
    footprint_area: float
    surface_area: float
    volume: float

class NativeBimRoofEngine:
    def quantities(self, roof):
        if not 0 <= roof.slope_degrees < 89:
            raise ValueError("Pendiente inválida")
        surface = roof.footprint_area / cos(radians(roof.slope_degrees))
        return RoofQuantities(
            roof.footprint_area,
            surface,
            surface * roof.roof_type.thickness,
        )

    def drainage_direction(self, roof):
        return "down_slope"
