from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class GlobalOptimizationItem:
    member_id:str
    current_profile_id:str
    recommended_profile_id:str|None
    weight_reduction_percent:float

@dataclass(frozen=True, slots=True)
class GlobalSteelOptimizationResult:
    items:tuple[GlobalOptimizationItem,...]
    average_weight_reduction_percent:float
    optimized_members:int

class GlobalSteelOptimizer:
    def combine(self,*optimization_results):
        items=tuple(
            GlobalOptimizationItem(r.member_id,r.current_profile_id,r.recommended_profile_id,r.weight_reduction_percent)
            for r in optimization_results
        )
        optimized=sum(1 for i in items if i.recommended_profile_id and i.recommended_profile_id!=i.current_profile_id)
        avg=sum(i.weight_reduction_percent for i in items)/len(items) if items else 0.0
        return GlobalSteelOptimizationResult(items,avg,optimized)
