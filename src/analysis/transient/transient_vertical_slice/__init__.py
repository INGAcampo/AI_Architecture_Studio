from dataclasses import dataclass
from analysis.transient.transient_solver_pipeline import TransientSolverPipeline
from analysis.transient.peak_response import PeakResponseEngine
from analysis.transient.energy_balance import EnergyBalanceEngine
from analysis.transient.critical_time_step import CriticalTimeStepEngine
from analysis.transient.explicit_stability import ExplicitStabilityEngine
from analysis.transient.cpu_gpu_transient_scheduler import CPUGPUTransientScheduler
from analysis.transient.transient_diagnostics import TransientDiagnosticsEngine
from analysis.transient.transient_ai_advisor import TransientAIAdvisor
from analysis.transient.transient_report import TransientReportEngine
@dataclass(frozen=True,slots=True)
class Workflow:
    result:object; peak_displacement:float; peak_velocity:float; energy_error:float; backend:str; diagnostics:object; advice:object; report:object
class TransientVerticalSlice:
    def run(self):
        result=TransientSolverPipeline().solve_sdof((0,10,20,10,0),.01,2,.2,100)
        pu=PeakResponseEngine().peak(tuple(s.displacement for s in result.steps))
        pv=PeakResponseEngine().peak(tuple(s.velocity for s in result.steps))
        error=EnergyBalanceEngine().error(1,.4,.4,.19)
        stable=ExplicitStabilityEngine().stable(.01,CriticalTimeStepEngine().calculate(2,100))
        backend=CPUGPUTransientScheduler().choose(1000,len(result.steps))
        d=TransientDiagnosticsEngine().inspect(True,error,stable)
        return Workflow(result,pu,pv,error,backend,d,TransientAIAdvisor().advise(d),TransientReportEngine().build(result,pu,pv,error,backend))
