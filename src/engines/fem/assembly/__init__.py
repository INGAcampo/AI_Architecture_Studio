from dataclasses import dataclass
from engines.numerical.assembly import ElementMatrixContribution,GlobalMatrixAssembler
from engines.numerical.vectors import DenseVector

@dataclass(frozen=True, slots=True)
class FEMAssemblyResult:
    stiffness:object
    loads:DenseVector

class FEMAssemblyEngine:
    def assemble(self,size,element_equations,elements):
        contributions=[];global_loads=[0.0]*size
        for element in elements:
            eqs=element_equations[element.element_id]
            k=element.local_stiffness_matrix()
            contributions.append(ElementMatrixContribution(eqs,k))
            f=element.equivalent_nodal_loads()
            for i,gi in enumerate(eqs):
                if gi is not None: global_loads[gi]+=f[i]
        K=GlobalMatrixAssembler().assemble(size,tuple(contributions))
        return FEMAssemblyResult(K,DenseVector(tuple(global_loads)))
