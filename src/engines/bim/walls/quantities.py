from __future__ import annotations

from dataclasses import dataclass

from .model import IntelligentWall, WallType


@dataclass(frozen=True, slots=True)
class WallQuantities:
    gross_area: float
    net_area: float
    volume: float
    core_volume: float


class WallQuantityCalculator:
    def calculate(
        self,
        wall: IntelligentWall,
        wall_type: WallType,
        *,
        opening_area: float = 0.0,
    ) -> WallQuantities:
        gross = wall.length * wall.height
        net = max(0.0, gross - opening_area)
        volume = net * wall_type.structure.total_thickness
        core_volume = net * wall_type.structure.core_thickness
        return WallQuantities(gross, net, volume, core_volume)
