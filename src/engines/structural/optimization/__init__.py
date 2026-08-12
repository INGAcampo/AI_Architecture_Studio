from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DesignCandidate:
    candidate_id: str
    weight: float
    demand_capacity_ratio: float
    displacement: float
    def __post_init__(self):
        if not self.candidate_id.strip() or self.weight <= 0 or self.demand_capacity_ratio < 0 or self.displacement < 0:
            raise ValueError("Datos inválidos")

class StructuralOptimizationEngine:
    def feasible(self, candidate, max_ratio=1.0, max_displacement=float("inf")):
        return candidate.demand_capacity_ratio <= max_ratio and candidate.displacement <= max_displacement
    def select_lightest(self, candidates, max_ratio=1.0, max_displacement=float("inf")):
        feasible = [c for c in candidates if self.feasible(c, max_ratio, max_displacement)]
        if not feasible:
            raise ValueError("No existen candidatos factibles")
        return min(feasible, key=lambda c: c.weight)
