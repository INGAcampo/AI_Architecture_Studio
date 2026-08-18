from dataclasses import dataclass,replace
@dataclass(frozen=True,slots=True)
class WeldOptimizationResult:
    segment_id:str; original_size:float; recommended_size:float|None; unity_ratio:float|None; weld_metal_reduction_percent:float
class WeldOptimizer:
    def __init__(self,engine): self.engine=engine
    def optimize(self,s,d,sizes=(.004,.005,.006,.008,.010,.012),target=.95):
        good=[]
        for z in sizes:
            c=replace(s,size=z); r=self.engine.design(c,d)
            if r.passed and r.unity_ratio<=target: good.append((z*s.length,r.unity_ratio,z))
        if not good:return WeldOptimizationResult(s.segment_id,s.size,None,None,0)
        vol,u,z=min(good); red=max(0,(s.size*s.length-vol)/(s.size*s.length)*100)
        return WeldOptimizationResult(s.segment_id,s.size,z,u,red)
