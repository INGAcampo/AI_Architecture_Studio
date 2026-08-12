"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

from aias_foundation_objects.models import FoundationObject

from .models import BarMark, QuantitySummary


class QuantityEngine:
    """Execute the public QuantityEngine operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    def calculate(self, foundation: FoundationObject, bars: list[BarMark]) -> QuantitySummary:
        """Execute the public QuantityEngine.calculate operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
        g = foundation.geometry
        concrete = g.volume_m3
        formwork = 2.0 * (g.width_m + g.length_m) * g.thickness_m
        excavation = g.width_m * g.length_m * (g.thickness_m + max(0.20, g.embedment_m))
        reinforcement = sum(bar.total_weight_kg for bar in bars)
        return QuantitySummary(round(concrete, 4), round(formwork, 4), round(excavation, 4), round(reinforcement, 3))
