from dataclasses import dataclass
from engines.numerical.vectors import DenseVector
from engines.numerical.conjugate_gradient import ConjugateGradientSolver

@dataclass(frozen=True, slots=True)
class LinearStaticResult:
    displacements:DenseVector
    residual:DenseVector
    converged:bool

class LinearStaticNumericalKernel:
    def solve(self,stiffness,loads,tolerance=1e-10):
        iterative=ConjugateGradientSolver().solve(stiffness,loads,tolerance=tolerance)
        residual=stiffness.matvec(iterative.solution).subtract(loads)
        return LinearStaticResult(iterative.solution,residual,iterative.converged)

    def equilibrium_ok(self,result,tolerance=1e-8):
        return result.converged and result.residual.norm()<=tolerance
