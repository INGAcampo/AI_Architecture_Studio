from analysis.fem.fem_domain import FemAnalysisResult
class FemSolver:
 def solve(self,K,F):
  if len(K)==1:u=(F[0]/K[0][0],)
  else:
   d=K[0][0]*K[1][1]-K[0][1]*K[1][0];u=((F[0]*K[1][1]-K[0][1]*F[1])/d,(K[0][0]*F[1]-F[0]*K[1][0])/d)
  return FemAnalysisResult(tuple(u),tuple(0 for _ in u),True)
