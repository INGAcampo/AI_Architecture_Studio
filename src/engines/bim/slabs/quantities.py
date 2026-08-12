from __future__ import annotations

from dataclasses import dataclass

from .geometry import polygon_area, polygon_perimeter
from .model import IntelligentSlab, SlabType


@dataclass(frozen=True, slots=True)
class SlabQuantities:
    gross_area: float
    opening_area: float
    net_area: float
    perimeter: float
    volume: float
    structural_volume: float


class SlabQuantityCalculator:
    def calculate(self, slab: IntelligentSlab, slab_type: SlabType) -> SlabQuantities:
        gross = polygon_area(slab.boundary)
        opening_area = sum(polygon_area(opening.boundary) for opening in slab.openings)
        net = max(0.0, gross - opening_area)
        perimeter = polygon_perimeter(slab.boundary)
        return SlabQuantities(
            gross_area=gross,
            opening_area=opening_area,
            net_area=net,
            perimeter=perimeter,
            volume=net * slab_type.structure.total_thickness,
            structural_volume=net * slab_type.structure.structural_thickness,
        )
