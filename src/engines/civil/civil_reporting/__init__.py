from dataclasses import dataclass
import json

@dataclass(frozen=True, slots=True)
class CivilQuantity:
    quantity_id: str
    description: str
    value: float
    unit: str

    def __post_init__(self):
        if not self.quantity_id.strip() or not self.description.strip() or not self.unit.strip():
            raise ValueError("Datos obligatorios")

class CivilReportingEngine:
    def total_by_unit(self, quantities):
        result = {}
        for quantity in quantities:
            result[quantity.unit] = result.get(quantity.unit, 0.0) + quantity.value
        return result

    def json_report(self, title, quantities):
        quantities = tuple(quantities)
        return json.dumps({
            "title": title,
            "totals": self.total_by_unit(quantities),
            "quantities": [{
                "quantity_id": q.quantity_id,
                "description": q.description,
                "value": q.value,
                "unit": q.unit,
            } for q in quantities],
        }, sort_keys=True)
