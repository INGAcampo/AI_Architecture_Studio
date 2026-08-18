from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ShellElement4:
    element_id:str
    node_ids:tuple[str,str,str,str]
    area:float
    thickness:float
    elastic_modulus:float
    poisson_ratio:float

    def membrane_stiffness(self):
        return self.elastic_modulus*self.thickness/(1-self.poisson_ratio**2)

    def bending_stiffness(self):
        return self.elastic_modulus*self.thickness**3/(12*(1-self.poisson_ratio**2))

    def local_stiffness_matrix(self):
        m=self.membrane_stiffness()/max(self.area,1e-12)
        b=self.bending_stiffness()/max(self.area,1e-12)
        base=m+b
        return tuple(tuple(base if i==j else -base/7 for j in range(8)) for i in range(8))

    def transformation_matrix(self):
        return tuple(tuple(1.0 if i==j else 0.0 for j in range(8)) for i in range(8))

    def equivalent_nodal_loads(self): return (0.0,)*8

    def recover_internal_forces(self,local_displacements):
        k=self.local_stiffness_matrix()
        return tuple(sum(k[i][j]*local_displacements[j] for j in range(8)) for i in range(8))
