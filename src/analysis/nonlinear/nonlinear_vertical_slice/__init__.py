from dataclasses import dataclass
from analysis.nonlinear.pushover_analysis import PushoverAnalysisEngine
from analysis.nonlinear.performance_evaluation import PerformanceEvaluationEngine
from analysis.nonlinear.nonlinear_diagnostics import NonlinearDiagnosticsEngine
from analysis.nonlinear.nonlinear_ai_advisor import NonlinearAIAdvisor
@dataclass(frozen=True,slots=True)
class NonlinearWorkflowResult: result:object; performance_level:str; diagnostics:object; advice:object; report_markdown:str
class NonlinearVerticalSlice:
 def run(self,k,fy,b,target):
  r=PushoverAnalysisEngine().run(k,fy,b,target);level=PerformanceEvaluationEngine().classify(target,.01,.03,.05);d=NonlinearDiagnosticsEngine().inspect(r);a=NonlinearAIAdvisor().advise(d);report=f'# Nonlinear Structural Analysis Report\n\n- Converged: {r.converged}\n- Steps: {len(r.steps)}\n- Peak load factor: {r.peak_load_factor:.4f}\n- Performance: {level}\n';return NonlinearWorkflowResult(r,level,d,a,report)
