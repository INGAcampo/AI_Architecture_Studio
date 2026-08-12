from dataclasses import dataclass
from engines.numerical.vectors import DenseVector

@dataclass(frozen=True, slots=True)
class IterativeSolveResult:
    solution:DenseVector
    iterations:int
    converged:bool
    residual_norm:float

class ConjugateGradientSolver:
    def solve(self,matrix,b,tolerance=1e-10,max_iterations=1000):
        x=DenseVector((0.0,)*len(b)); r=b.subtract(matrix.matvec(x)); p=r
        rsold=r.dot(r)
        if rsold**0.5<=tolerance: return IterativeSolveResult(x,0,True,rsold**0.5)
        for k in range(1,max_iterations+1):
            ap=matrix.matvec(p)
            alpha=rsold/p.dot(ap)
            x=x.add(p.scale(alpha))
            r=r.subtract(ap.scale(alpha))
            rsnew=r.dot(r)
            if rsnew**0.5<=tolerance:
                return IterativeSolveResult(x,k,True,rsnew**0.5)
            p=r.add(p.scale(rsnew/rsold)); rsold=rsnew
        return IterativeSolveResult(x,max_iterations,False,rsold**0.5)
