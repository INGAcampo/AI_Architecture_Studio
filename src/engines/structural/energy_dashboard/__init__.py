from dataclasses import dataclass
import json

@dataclass(frozen=True, slots=True)
class EnergyKpi:
    kpi_id: str
    label: str
    value: float
    unit: str
    target: float | None = None

    def __post_init__(self):
        if not self.kpi_id.strip() or not self.label.strip() or not self.unit.strip():
            raise ValueError("Datos obligatorios")

    @property
    def meets_target(self):
        return True if self.target is None else self.value <= self.target

class EnergyDashboardReporter:
    def summary(self, kpis):
        kpis = tuple(kpis)
        return {
            "kpi_count": len(kpis),
            "target_count": sum(kpi.target is not None for kpi in kpis),
            "passing_count": sum(kpi.meets_target for kpi in kpis),
        }

    def json_report(self, title, kpis):
        kpis = tuple(kpis)
        return json.dumps({
            "title": title,
            "summary": self.summary(kpis),
            "kpis": [{
                "kpi_id": kpi.kpi_id,
                "label": kpi.label,
                "value": kpi.value,
                "unit": kpi.unit,
                "target": kpi.target,
                "meets_target": kpi.meets_target,
            } for kpi in kpis],
        }, sort_keys=True)
