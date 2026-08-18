from dataclasses import dataclass
from math import dist

@dataclass(frozen=True, slots=True)
class TrussElement:
    element_id:str
    node_ids:tuple[str,str]
    start:tuple[float,float,float]
    end:tuple[float,float,float]
    area:float
    elastic_modulus:float

    @property
    def length(self): return dist(self.start,self.end)

    def local_stiffness_matrix(self):
        k=self.area*self.elastic_modulus/self.length
        return ((k,-k),(-k,k))

    def transformation_matrix(self):
        l=self.length
        c=((self.end[0]-self.start[0])/l,(self.end[1]-self.start[1])/l,(self.end[2]-self.start[2])/l)
        return (c,tuple(-v for v in c))

    def equivalent_nodal_loads(self): return (0.0,0.0)

    def recover_internal_forces(self,local_displacements):
        k=self.area*self.elastic_modulus/self.length
        delta=local_displacements[1]-local_displacements[0]
        n=k*delta
        return (-n,n)
