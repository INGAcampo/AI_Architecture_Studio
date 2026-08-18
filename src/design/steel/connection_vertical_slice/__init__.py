from dataclasses import dataclass
from design.steel.connection_domain import ConnectionCheck,ConnectionDesignResult
from design.steel.connection_optimizer import ConnectionOptimizer
from design.steel.connection_ai_advisor import ConnectionAIAdvisor
from design.steel.connection_report import ConnectionReportEngine

@dataclass(frozen=True,slots=True)
class CompleteConnectionWorkflowResult:
    design_result:object; optimization_result:object; advice:object; report:object

class CompleteConnectionVerticalSlice:
    def run(self,connection,checks,options=()):
        checks=tuple(checks)
        unity=max((c.ratio for c in checks),default=0.0)
        governing=max(checks,key=lambda c:c.ratio).name if checks else "none"
        result=ConnectionDesignResult(connection.connection_id,checks,unity,unity<=1,governing)
        optimization=ConnectionOptimizer().optimize(tuple(options))
        advice=ConnectionAIAdvisor().advise(result,optimization)
        report=ConnectionReportEngine().build(connection,result,advice)
        return CompleteConnectionWorkflowResult(result,optimization,advice,report)
