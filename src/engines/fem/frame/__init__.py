from dataclasses import dataclass
from math import dist

@dataclass(frozen=True, slots=True)
class FrameElement2D:
    element_id:str
    node_ids:tuple[str,str]
    start:tuple[float,float]
    end:tuple[float,float]
    area:float
    elastic_modulus:float
    inertia:float

    @property
    def length(self): return dist(self.start,self.end)

    def local_stiffness_matrix(self):
        L=self.length;EA=self.elastic_modulus*self.area;EI=self.elastic_modulus*self.inertia
        a=EA/L;b=12*EI/L**3;c=6*EI/L**2;d=4*EI/L;e=2*EI/L
        return (
            (a,0,0,-a,0,0),
            (0,b,c,0,-b,c),
            (0,c,d,0,-c,e),
            (-a,0,0,a,0,0),
            (0,-b,-c,0,b,-c),
            (0,c,e,0,-c,d),
        )

    def transformation_matrix(self):
        L=self.length;c=(self.end[0]-self.start[0])/L;s=(self.end[1]-self.start[1])/L
        return (
            (c,s,0,0,0,0),(-s,c,0,0,0,0),(0,0,1,0,0,0),
            (0,0,0,c,s,0),(0,0,0,-s,c,0),(0,0,0,0,0,1),
        )

    def equivalent_nodal_loads(self): return (0.0,)*6

    def recover_internal_forces(self,local_displacements):
        k=self.local_stiffness_matrix()
        return tuple(sum(k[i][j]*local_displacements[j] for j in range(6)) for i in range(6))
