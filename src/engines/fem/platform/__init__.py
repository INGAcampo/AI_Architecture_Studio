from dataclasses import dataclass
from engines.numerical.linear_static import LinearStaticNumericalKernel

@dataclass(frozen=True, slots=True)
class FEMAnalysisResult:
    displacements:object
    element_forces:dict[str,tuple]
    equilibrium_ok:bool

class NativeFEMPlatform:
    def __init__(self,assembly_engine):
        self.assembly_engine=assembly_engine
        self.solver=LinearStaticNumericalKernel()

    def analyze(self,size,element_equations,elements,extra_loads=None):
        assembled=self.assembly_engine.assemble(size,element_equations,elements)
        loads=assembled.loads
        if extra_loads is not None:
            loads=loads.add(extra_loads)
        solved=self.solver.solve(assembled.stiffness,loads)
        element_forces={}
        for e in elements:
            eqs=element_equations[e.element_id]
            local=tuple(0.0 if gi is None else solved.displacements[gi] for gi in eqs)
            element_forces[e.element_id]=e.recover_internal_forces(local)
        return FEMAnalysisResult(solved.displacements,element_forces,self.solver.equilibrium_ok(solved))
