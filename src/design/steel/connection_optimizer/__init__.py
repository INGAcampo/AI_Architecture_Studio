from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ConnectionOption:
    option_id:str; unity_ratio:float; cost:float; constructability:float; weight:float
@dataclass(frozen=True,slots=True)
class ConnectionOptimizationResult:
    recommended_option_id:str|None; ranked_options:tuple; objective_value:float|None
class ConnectionOptimizer:
    def optimize(self,options):
        feasible=[o for o in options if o.unity_ratio<=1]
        if not feasible:return ConnectionOptimizationResult(None,(),None)
        ranked=tuple(sorted(feasible,key=lambda o:(o.cost+o.weight*0.1-o.constructability*10,o.unity_ratio)))
        best=ranked[0]
        return ConnectionOptimizationResult(best.option_id,ranked,best.cost+best.weight*.1-best.constructability*10)
