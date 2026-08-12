from analysis.matrix.gaussian_solver import GaussianSolver
from analysis.matrix.analysis_domain import AnalysisResult
class LinearStaticSolver:
    def solve(self,K,F):
        u=GaussianSolver().solve(K,F)
        return AnalysisResult(u,tuple(0 for _ in u),True)
