from dataclasses import dataclass
from analysis.composites.puck_criterion import PuckCriterionEngine
from analysis.composites.progressive_damage_loop import ProgressiveDamageLoop
from analysis.composites.delamination_initiation import DelaminationInitiationEngine
from analysis.composites.composite_diagnostics import CompositeDiagnosticsEngine
from analysis.composites.composite_ai_advisor import CompositeAIAdvisor
from analysis.composites.composite_report import CompositeReportEngine
@dataclass(frozen=True,slots=True)
class CompositeWorkflowResult: result:object; delamination_index:float; diagnostics:object; advice:object; report:object
class CompositeVerticalSlice:
    def run(self):
        failure=PuckCriterionEngine().fiber_failure(420.0,600.0,450.0); result=ProgressiveDamageLoop().run(failure)
        delam=DelaminationInitiationEngine().quadratic(5.0,8.0,20.0,25.0)
        d=CompositeDiagnosticsEngine().inspect(result.converged,result.state.fiber_damage,delam)
        return CompositeWorkflowResult(result,delam,d,CompositeAIAdvisor().advise(d),CompositeReportEngine().build(result,delam))
