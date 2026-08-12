from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BeamElement2D:
    element_id:str
    node_ids:tuple[str,str]
    length:float
    elastic_modulus:float
    inertia:float
    distributed_load:float=0.0

    def local_stiffness_matrix(self):
        L=self.length; EI=self.elastic_modulus*self.inertia
        f=EI/L**3
        return (
            (12*f,6*L*f,-12*f,6*L*f),
            (6*L*f,4*L*L*f,-6*L*f,2*L*L*f),
            (-12*f,-6*L*f,12*f,-6*L*f),
            (6*L*f,2*L*L*f,-6*L*f,4*L*L*f),
        )

    def transformation_matrix(self):
        return ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))

    def equivalent_nodal_loads(self):
        q=self.distributed_load;L=self.length
        return (q*L/2,q*L*L/12,q*L/2,-q*L*L/12)

    def recover_internal_forces(self,local_displacements):
        k=self.local_stiffness_matrix()
        return tuple(sum(k[i][j]*local_displacements[j] for j in range(4)) for i in range(4))
