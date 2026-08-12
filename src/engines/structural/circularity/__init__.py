from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MaterialFlow:
    flow_id: str
    total_mass: float
    reused_mass: float = 0
    recycled_mass: float = 0
    recovered_mass: float = 0
    def __post_init__(self):
        if not self.flow_id.strip() or self.total_mass <= 0:
            raise ValueError("Datos inválidos")

class CircularityEngine:
    def diversion_rate(self, flow):
        diverted = flow.reused_mass + flow.recycled_mass + flow.recovered_mass
        return min(diverted / flow.total_mass, 1.0)
