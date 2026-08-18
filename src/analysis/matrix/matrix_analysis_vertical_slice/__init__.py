from dataclasses import dataclass
from analysis.matrix.linear_static import LinearStaticSolver
from analysis.matrix.reaction_recovery import ReactionRecoveryEngine
from analysis.matrix.diagnostics import StructuralDiagnostics
from analysis.matrix.analysis_report import AnalysisReportEngine
from analysis.matrix.analysis_ai_advisor import AnalysisAIAdvisor
@dataclass(frozen=True,slots=True)
class MatrixAnalysisWorkflowResult:
    result:object; reactions:tuple; diagnostics:object; advice:object; report:object
class MatrixAnalysisVerticalSlice:
    def run(self,K,F,max_drift=0):
        r=LinearStaticSolver().solve(K,F)
        reactions=ReactionRecoveryEngine().recover(K,r.displacements,F)
        d=StructuralDiagnostics().inspect(K)
        a=AnalysisAIAdvisor().advise(r,d,max_drift)
        report=AnalysisReportEngine().build(r,max_drift)
        return MatrixAnalysisWorkflowResult(r,reactions,d,a,report)
