from dataclasses import dataclass
from design.steel.frame_connectivity import FrameConnectivityEngine
from design.steel.frame_load_path import FrameLoadPathEngine
from design.steel.frame_batch_design import FrameBatchDesignEngine
from design.steel.critical_dashboard import CriticalMemberDashboardEngine
from design.steel.global_optimizer import GlobalSteelOptimizer
from design.steel.frame_ai_advisor import SteelFrameAIAdvisor
from design.steel.frame_reports import SteelFrameReportEngine

@dataclass(frozen=True, slots=True)
class CompleteSteelFrameWorkflowResult:
    connectivity:object
    load_path:object
    batch:object
    dashboard:object
    optimization:object
    advice:object
    report:object

class CompleteSteelFrameVerticalSlice:
    def run(self,frame,source_node,support_nodes,beam_results,column_results,brace_results,*optimization_results):
        connectivity=FrameConnectivityEngine().analyze(frame)
        load_path=FrameLoadPathEngine().trace(frame,source_node,support_nodes)
        batch=FrameBatchDesignEngine().design(beam_results,column_results,brace_results)
        dashboard=CriticalMemberDashboardEngine().build(batch)
        optimization=GlobalSteelOptimizer().combine(*optimization_results)
        advice=SteelFrameAIAdvisor().advise(dashboard,connectivity,load_path,optimization)
        report=SteelFrameReportEngine().build(frame,dashboard,optimization,advice)
        return CompleteSteelFrameWorkflowResult(connectivity,load_path,batch,dashboard,optimization,advice,report)
