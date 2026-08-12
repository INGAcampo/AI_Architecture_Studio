"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ProductivityReport:
    """Execute the public ProductivityReport operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    baseline_hours: float
    actual_hours: float
    automation_hours_saved: float
    reuse_hours_saved: float
    quality_passed: bool

    @property
    def reduction_ratio(self) -> float:
        """Execute the public ProductivityReport.reduction_ratio operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        if self.baseline_hours <= 0:
            return 0.0
        return 1.0 - self.actual_hours / self.baseline_hours

    @property
    def meets_45_percent_target(self) -> bool:
        """Execute the public ProductivityReport.meets_45_percent_target operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        return self.quality_passed and self.reduction_ratio >= 0.45

class ProductivityMeasurementEngine:
    """Execute the public ProductivityMeasurementEngine operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    def measure(
        self,
        baseline_hours: float,
        manual_hours: float,
        automation_hours_saved: float,
        reuse_hours_saved: float,
        quality_passed: bool,
    ) -> ProductivityReport:
        """Execute the public ProductivityMeasurementEngine.measure operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        actual = max(0.0, manual_hours)
        return ProductivityReport(
            baseline_hours,
            actual,
            automation_hours_saved,
            reuse_hours_saved,
            quality_passed,
        )
