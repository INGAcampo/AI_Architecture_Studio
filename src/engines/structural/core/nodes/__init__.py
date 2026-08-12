from dataclasses import dataclass,field
@dataclass(frozen=True,slots=True)
class NodeRestraint: ux:bool=False; uy:bool=False; uz:bool=False; rx:bool=False; ry:bool=False; rz:bool=False
@dataclass(frozen=True,slots=True)
class StructuralNode: node_id:str; x:float; y:float; z:float; restraint:NodeRestraint=NodeRestraint(); mass:float=0.; metadata:dict=field(default_factory=dict)
class StructuralNodeEngine:
 def __init__(self): self._n={}
 def add(self,n):
  if n.node_id in self._n: raise ValueError('Nodo duplicado')
  self._n[n.node_id]=n; return n
 def get(self,i): return self._n[i]
 def distance(self,a,b):
  from math import dist
  x,y=self.get(a),self.get(b); return dist((x.x,x.y,x.z),(y.x,y.y,y.z))
 def all(self): return tuple(self._n[k] for k in sorted(self._n))
