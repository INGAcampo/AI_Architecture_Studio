from dataclasses import dataclass
import json

@dataclass(frozen=True, slots=True)
class GeotechnicalKpi:
    kpi_id: str
    label: str
    value: float
    unit: str

class GeotechnicalDashboard:
    def summary(self, kpis):
        kpis = tuple(kpis)
        return {
            "kpi_count": len(kpis),
            "max_value": max(kpi.value for kpi in kpis),
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
            } for kpi in kpis],
        }, sort_keys=True)
