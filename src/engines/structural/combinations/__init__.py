from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class LoadFactor:
    case_id:str; factor:float
    def __post_init__(self):
        if not self.case_id.strip(): raise ValueError("case_id obligatorio")
@dataclass(frozen=True, slots=True)
class LoadCombination:
    combination_id:str; factors:tuple[LoadFactor,...]
    def __post_init__(self):
        if not self.combination_id.strip() or not self.factors: raise ValueError("Datos inválidos")
class CombinationEngine:
    def __init__(self): self.items={}
    def add(self, combination):
        if combination.combination_id in self.items: raise KeyError(combination.combination_id)
        self.items[combination.combination_id]=combination; return combination
    def evaluate(self, combination_id, values):
        return sum(f.factor*values.get(f.case_id,0.0) for f in self.items[combination_id].factors)
