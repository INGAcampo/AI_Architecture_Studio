from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ElementForceResult:
    element_id:str
    forces:tuple[float,...]

class InternalForceRecovery:
    def recover(self,elements,element_equations,global_displacements):
        out=[]
        for e in elements:
            local=tuple(0.0 if gi is None else global_displacements[gi] for gi in element_equations[e.element_id])
            out.append(ElementForceResult(e.element_id,tuple(e.recover_internal_forces(local))))
        return tuple(out)

    def by_element(self,results):
        return {r.element_id:r for r in results}
