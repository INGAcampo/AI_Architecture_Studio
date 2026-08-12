from __future__ import annotations

from dataclasses import dataclass

from .geometry import polygon_area, polygon_perimeter, sloped_area
from .model import IntelligentRoof, RoofType


@dataclass(frozen=True, slots=True)
class RoofQuantities:
    projected_area: float
    opening_area: float
    net_projected_area: float
    sloped_area: float
    eave_length: float
    ridge_length: float
    valley_length: float
    hip_length: float
    volume: float
    structural_volume: float


class RoofQuantityCalculator:
    def calculate(self, roof: IntelligentRoof, roof_type: RoofType) -> RoofQuantities:
        gross = polygon_area(roof.boundary)
        opening_area = sum(polygon_area(opening.boundary) for opening in roof.openings)
        net = max(0.0, gross - opening_area)
        actual = sloped_area(net, roof.pitch_degrees)
        return RoofQuantities(
            projected_area=gross,
            opening_area=opening_area,
            net_projected_area=net,
            sloped_area=actual,
            eave_length=polygon_perimeter(roof.boundary) + roof.overhang * 8.0,
            ridge_length=roof.ridge_length,
            valley_length=roof.valley_length,
            hip_length=roof.hip_length,
            volume=actual * roof_type.structure.total_thickness,
            structural_volume=actual * roof_type.structure.structural_thickness,
        )
