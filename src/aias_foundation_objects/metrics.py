"""Deterministic service-load, bearing, material-volume and self-weight metrics."""
from __future__ import annotations
from .models import FoundationObject

class FoundationMetrics:
    """Calculate common quantities without performing jurisdictional resistance checks."""
    def total_service_load_kn(self, obj: FoundationObject) -> float:
        """Sum axial service loads from every support in kilonewtons."""
        return sum(s.axial_load_kn for s in obj.supports)

    def gross_bearing_pressure_kpa(self, obj: FoundationObject) -> float:
        """Divide service load by gross area or return infinity for zero area."""
        area=obj.geometry.area_m2
        return self.total_service_load_kn(obj)/area if area > 0 else float("inf")

    def utilization_ratio(self, obj: FoundationObject) -> float:
        """Compare gross pressure with allowable soil bearing pressure."""
        return self.gross_bearing_pressure_kpa(obj)/obj.soil.allowable_bearing_pressure_kpa

    def concrete_volume_m3(self, obj: FoundationObject) -> float:
        """Return gross geometric concrete volume in cubic metres."""
        return obj.geometry.volume_m3

    def estimated_self_weight_kn(self, obj: FoundationObject, concrete_unit_weight_kn_m3: float = 24.0) -> float:
        """Estimate self-weight from volume and supplied concrete unit weight."""
        return self.concrete_volume_m3(obj)*concrete_unit_weight_kn_m3
