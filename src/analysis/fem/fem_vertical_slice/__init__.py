from dataclasses import dataclass
from analysis.fem.fem_solver import FemSolver
from analysis.fem.reaction_recovery import ReactionRecovery
from analysis.fem.fem_diagnostics import FemDiagnostics
from analysis.fem.fem_report import FemReportEngine
@dataclass(frozen=True,slots=True)
class FemWorkflow: result:object; reactions:tuple; diagnostics:object; report:object
class FemVerticalSlice:
 def run(self,K,F,n,e,q=.8,vm=0):
  r=FemSolver().solve(K,F);rx=ReactionRecovery().recover(K,r.displacements,F);d=FemDiagnostics().inspect(K,q);rep=FemReportEngine().build(r,n,e,vm);return FemWorkflow(r,rx,d,rep)
