from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BraceOptimizationResult:
    member_id:str
    current_profile_id:str
    recommended_profile_id:str|None
    unity_ratio:float|None
    weight_reduction_percent:float

class SteelBraceOptimizer:
    def __init__(self,design_engine): self.design_engine=design_engine

    def optimize(self,brace,current_profile,material,profiles,target_unity=0.95):
        feasible=[]
        for p in profiles:
            r=self.design_engine.design(brace,p,material)
            if r.passed and r.unity_ratio<=target_unity:
                feasible.append((p.weight_per_length,r.unity_ratio,p.profile_id))
        if not feasible:
            return BraceOptimizationResult(brace.member_id,current_profile.profile_id,None,None,0.0)
        weight,unity,pid=min(feasible)
        reduction=max(0.0,(current_profile.weight_per_length-weight)/current_profile.weight_per_length*100)
        return BraceOptimizationResult(brace.member_id,current_profile.profile_id,pid,unity,reduction)
