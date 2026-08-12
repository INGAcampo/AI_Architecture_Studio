from dataclasses import dataclass
from analysis.dynamic.modal_analysis_engine import ModalAnalysisEngine
from analysis.dynamic.seismic_base_shear import SeismicBaseShearEngine
from analysis.dynamic.dynamic_diagnostics import DynamicDiagnosticsEngine
from analysis.dynamic.dynamic_ai_advisor import DynamicAIAdvisor
from analysis.dynamic.dynamic_report import DynamicReportEngine
@dataclass(frozen=True,slots=True)
class DynamicWorkflowResult:
    result:object;base_shear:float;diagnostics:object;advice:object;report:object
class DynamicVerticalSlice:
    def run(self,K,M,weight,coefficient,drift):
        r=ModalAnalysisEngine().solve(K,M);b=SeismicBaseShearEngine().calculate(coefficient,weight)
        d=DynamicDiagnosticsEngine().inspect(tuple(m.frequency_hz for m in r.modes),sum(r.effective_mass_ratios),drift)
        a=DynamicAIAdvisor().advise(d);report=DynamicReportEngine().build(r,b,drift)
        return DynamicWorkflowResult(r,b,d,a,report)
