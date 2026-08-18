from __future__ import annotations

from .model import HostWallGeometry, Opening, OpeningQuantities


class OpeningQuantityCalculator:
    def calculate(
        self,
        wall: HostWallGeometry,
        openings: tuple[Opening, ...],
    ) -> OpeningQuantities:
        gross_area = wall.length * wall.height
        opening_area = sum(opening.area for opening in openings)
        net_area = max(0.0, gross_area - opening_area)
        opening_volume = opening_area * wall.thickness
        return OpeningQuantities(
            gross_area=gross_area,
            opening_area=opening_area,
            net_area=net_area,
            opening_volume=opening_volume,
        )
