from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class LoadFactor:
    case_id:str
    factor:float

@dataclass(frozen=True,slots=True)
class LoadCombination:
    combination_id:str
    name:str
    factors:tuple[LoadFactor,...]
    design_type:str="strength"

class LoadCombinationEngine:
    def evaluate(self,combination,case_results):
        return sum(case_results[f.case_id]*f.factor for f in combination.factors)
    def validate(self,combination,known_case_ids):
        missing=tuple(sorted(f.case_id for f in combination.factors if f.case_id not in known_case_ids))
        return missing
