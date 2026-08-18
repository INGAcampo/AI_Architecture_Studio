from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ConstraintResult:
    satisfied:bool
    violations:tuple[str,...]

class StructuralConstraintSolver:
    def solve(self,objects,constraints):
        violations=[]
        for cid,predicate,message in constraints:
            if not predicate(objects): violations.append(f"{cid}:{message}")
        return ConstraintResult(not violations,tuple(violations))
    def aligned(self,a,b,tol=1e-6):
        return all(abs(x-y)<=tol for x,y in zip(a,b))
