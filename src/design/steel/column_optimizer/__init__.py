from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ColumnOptimizationCandidate:
    profile_id:str
    weight_per_length:float
    unity_ratio:float
    passed:bool

@dataclass(frozen=True, slots=True)
class ColumnOptimizationResult:
    member_id:str
    current_profile_id:str
    recommended_profile_id:str|None
    candidates:tuple[ColumnOptimizationCandidate,...]
    weight_reduction_percent:float

class SteelColumnOptimizer:
    def __init__(self,design_engine): self.design_engine=design_engine
    def optimize(self,column,current_profile,material,profiles,target_unity=0.95):
        out=[]
        for p in profiles:
            r=self.design_engine.design(column,p,material)
            out.append(ColumnOptimizationCandidate(p.profile_id,p.weight_per_length,r.unity_ratio,r.passed and r.unity_ratio<=target_unity))
        feasible=sorted((c for c in out if c.passed),key=lambda c:(c.weight_per_length,c.unity_ratio))
        best=feasible[0] if feasible else None
        reduction=0.0 if best is None else max(0.0,(current_profile.weight_per_length-best.weight_per_length)/current_profile.weight_per_length*100)
        return ColumnOptimizationResult(column.member_id,current_profile.profile_id,None if best is None else best.profile_id,tuple(out),reduction)
