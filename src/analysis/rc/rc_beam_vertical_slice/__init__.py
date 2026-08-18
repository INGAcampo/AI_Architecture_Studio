from dataclasses import dataclass
from analysis.rc.rc_domain import RCBeamInput
from analysis.rc.rc_design_pipeline import RCDesignPipeline
from analysis.rc.minimum_reinforcement import MinimumReinforcementEngine
from analysis.rc.neutral_axis_solver import NeutralAxisSolver
from analysis.rc.strain_compatibility import StrainCompatibilityEngine
from analysis.rc.ductility_check import DuctilityCheckEngine
from analysis.rc.serviceability_check import ServiceabilityCheckEngine
from analysis.rc.rc_diagnostics import RCDiagnosticsEngine
from analysis.rc.rc_ai_advisor import RCAIAdvisor
from analysis.rc.rc_report import RCReportEngine
@dataclass(frozen=True,slots=True)
class Workflow:
    beam:object; result:object; minimum_steel:float; serviceable:bool; ductile:bool; diagnostics:object; advice:object; report:object
class RCBeamVerticalSlice:
    def run(self):
        b=RCBeamInput("RC-BEAM-DEMO-001",300,550,500,28,420,180_000_000,80_000)
        r=RCDesignPipeline().design(b)
        amin=MinimumReinforcementEngine().area(b.width,b.effective_depth,b.concrete_strength,b.steel_yield_strength)
        c=NeutralAxisSolver().solve(max(r.steel_area,amin),b.steel_yield_strength,b.width,b.concrete_strength)
        duct=DuctilityCheckEngine().tension_controlled(StrainCompatibilityEngine().steel_strain(c,b.effective_depth))
        serv=ServiceabilityCheckEngine().check(8,15,.25,.30)
        d=RCDiagnosticsEngine().inspect(r.utilization,serv,duct)
        return Workflow(b,r,amin,serv,duct,d,RCAIAdvisor().advise(d),RCReportEngine().build(b,r))
