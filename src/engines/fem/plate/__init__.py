from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PlateElement4:
    element_id:str
    node_ids:tuple[str,str,str,str]
    area:float
    thickness:float
    elastic_modulus:float
    poisson_ratio:float
    pressure:float=0.0

    def bending_rigidity(self):
        return self.elastic_modulus*self.thickness**3/(12*(1-self.poisson_ratio**2))

    def local_stiffness_matrix(self):
        d=self.bending_rigidity()/max(self.area,1e-12)
        return tuple(tuple((2*d if i==j else -d/3) for j in range(4)) for i in range(4))

    def transformation_matrix(self):
        return tuple(tuple(1.0 if i==j else 0.0 for j in range(4)) for i in range(4))

    def equivalent_nodal_loads(self):
        q=self.pressure*self.area/4
        return (q,q,q,q)

    def recover_internal_forces(self,local_displacements):
        k=self.local_stiffness_matrix()
        return tuple(sum(k[i][j]*local_displacements[j] for j in range(4)) for i in range(4))
