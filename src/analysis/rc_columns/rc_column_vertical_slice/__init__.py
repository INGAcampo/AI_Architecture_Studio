from dataclasses import dataclass
from analysis.rc_columns.rc_column_domain import RCColumnInput
from analysis.rc_columns.column_design_pipeline import ColumnDesignPipeline
from analysis.rc_columns.longitudinal_rebar_ratio import LongitudinalRebarRatioEngine
from analysis.rc_columns.strong_column_weak_beam import StrongColumnWeakBeamEngine
from analysis.rc_columns.column_diagnostics import ColumnDiagnosticsEngine
from analysis.rc_columns.column_ai_advisor import ColumnAIAdvisor
from analysis.rc_columns.column_report import ColumnReportEngine
@dataclass(frozen=True,slots=True)
class Workflow:
    column:object; result:object; reinforcement_ratio:float; seismic_ok:bool; diagnostics:object; advice:object; report:object
class RCColumnVerticalSlice:
    def run(self):
        c=RCColumnInput("RC-COLUMN-DEMO-001",450,450,3500,35,420,5000,2_000_000,100_000_000,80_000_000)
        r=ColumnDesignPipeline().design(c)
        ratio=LongitudinalRebarRatioEngine().ratio(c.steel_area,c.width*c.depth)
        ratio_ok=LongitudinalRebarRatioEngine().acceptable(ratio)
        seismic_ok=StrongColumnWeakBeamEngine().passes((400,400),(300,300))
        d=ColumnDiagnosticsEngine().inspect(r.interaction_ratio,r.slenderness_ratio,ratio_ok,seismic_ok)
        return Workflow(c,r,ratio,seismic_ok,d,ColumnAIAdvisor().advise(d),ColumnReportEngine().build(c,r))
