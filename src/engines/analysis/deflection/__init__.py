from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True,slots=True)
class NodeDeflection:
    node_id:str
    ux:float
    uy:float
    uz:float
    magnitude:float

class DeflectionEngine:
    def build(self,node_ids,translations):
        results=[]
        for node_id,(ux,uy,uz) in zip(node_ids,translations):
            results.append(NodeDeflection(node_id,ux,uy,uz,sqrt(ux*ux+uy*uy+uz*uz)))
        return tuple(results)

    def maximum(self,results):
        return max(results,key=lambda r:r.magnitude)
