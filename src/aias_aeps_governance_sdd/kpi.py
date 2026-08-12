"""Evidence-classifiable productivity, automation and reuse KPI calculations."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ProductivitySnapshot:
    """Compute sustainable time reduction and compare it with the 45 percent target."""
    baseline_hours: float
    actual_hours: float
    automated_hours: float
    reused_assets: int
    total_assets: int

    @property
    def time_reduction(self) -> float:
        """Return fractional time saved against a positive baseline."""
        if self.baseline_hours <= 0:
            return 0.0
        return 1.0 - (self.actual_hours / self.baseline_hours)

    @property
    def automation_ratio(self) -> float:
        """Return automated work as a fraction of actual delivery hours."""
        if self.actual_hours <= 0:
            return 0.0
        return self.automated_hours / self.actual_hours

    @property
    def reuse_ratio(self) -> float:
        """Return reused assets as a fraction of all consumed assets."""
        if self.total_assets <= 0:
            return 0.0
        return self.reused_assets / self.total_assets

    @property
    def meets_acceleration_target(self) -> bool:
        """Return whether measured reduction reaches the constitutional 45 percent."""
        return self.time_reduction >= 0.45
