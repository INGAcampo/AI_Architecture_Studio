from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SteelOptimizationResult: member_id:str;current_profile_id:str;recommended_profile_id:str|None;weight_reduction_percent:float
class SteelProfileOptimizer:
 def __init__(self,engine): self.engine=engine
 def optimize(self,b,current,m,profiles,target=.95):
  feasible=[]
  for p in profiles:
   r=self.engine.design(b,p,m)
   if r.passed and r.unity_ratio<=target: feasible.append((p.weight_per_length,p.profile_id))
  if not feasible:return SteelOptimizationResult(b.member_id,current.profile_id,None,0.)
  wt,pid=min(feasible);red=max(0.,(current.weight_per_length-wt)/current.weight_per_length*100);return SteelOptimizationResult(b.member_id,current.profile_id,pid,red)
