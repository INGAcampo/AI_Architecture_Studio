"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

import math

from aias_foundation_code_checks.models import ReinforcementResult
from aias_foundation_objects.models import FoundationObject

from .models import BarMark


class ReinforcementDetailer:
    """Execute the public ReinforcementDetailer operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    DIAMETERS = (12, 16, 20, 25, 32)

    def detail(self, foundation: FoundationObject, reinforcement: ReinforcementResult) -> list[BarMark]:
        """Execute the public ReinforcementDetailer.detail operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
        cover_mm = foundation.cover_m * 1000.0
        clear_x = foundation.geometry.length_m * 1000.0 - 2.0 * cover_mm
        clear_y = foundation.geometry.width_m * 1000.0 - 2.0 * cover_mm
        if clear_x <= 0 or clear_y <= 0:
            raise ValueError("cover_exceeds_foundation_geometry")
        x = self._select("B1", "X", reinforcement.governing_area_x_mm2, clear_y, clear_x)
        y = self._select("B2", "Y", reinforcement.governing_area_y_mm2, clear_x, clear_y)
        return [x, y]

    def _select(self, mark: str, direction: str, required_area_mm2: float, distribution_width_mm: float, bar_length_mm: float) -> BarMark:
        for diameter in self.DIAMETERS:
            area = math.pi * diameter**2 / 4.0
            quantity = max(2, math.ceil(required_area_mm2 / area))
            spacing = math.floor(distribution_width_mm / max(1, quantity - 1))
            if 75 <= spacing <= 300:
                return BarMark(mark, direction, diameter, spacing, quantity, int(round(bar_length_mm)))
        diameter = self.DIAMETERS[-1]
        area = math.pi * diameter**2 / 4.0
        quantity = max(2, math.ceil(required_area_mm2 / area))
        spacing = max(75, min(300, math.floor(distribution_width_mm / max(1, quantity - 1))))
        return BarMark(mark, direction, diameter, spacing, quantity, int(round(bar_length_mm)))
