from dataclasses import dataclass
from design.steel.column_domain import SteelColumn,SteelColumnDemand,ColumnEndCondition
from design.steel.column_design_engine import SteelColumnDesignEngine
from design.steel.column_optimizer import SteelColumnOptimizer
from design.steel.column_reports import SteelColumnReportEngine
from design.steel.column_ai_advisor import SteelColumnAIAdvisor

@dataclass(frozen=True, slots=True)
class SteelColumnWorkflowResult:
    column:object
    design_result:object
    optimization_result:object
    report:object
    advice:object

class SteelColumnVerticalSlice:
    def __init__(self,profile_repository,material_repository):
        self.profiles=profile_repository
        self.materials=material_repository
        self.design=SteelColumnDesignEngine()
        self.optimizer=SteelColumnOptimizer(self.design)
        self.reports=SteelColumnReportEngine()
        self.ai=SteelColumnAIAdvisor()

    def run(self,member_id,profile_id,material_id,length,axial,moment_major=0.0,moment_minor=0.0,
            end_major=ColumnEndCondition.PINNED_PINNED,end_minor=ColumnEndCondition.PINNED_PINNED,target_unity=0.95):
        profile=self.profiles.get(profile_id)
        material=self.materials.get(material_id)
        column=SteelColumn(member_id,profile_id,material_id,length,end_major,end_minor,SteelColumnDemand(axial,moment_major,moment_minor))
        result=self.design.design(column,profile,material)
        optimization=self.optimizer.optimize(column,profile,material,self.profiles.all(),target_unity)
        report=self.reports.build(column,profile,material,result,optimization)
        advice=self.ai.explain(result)
        return SteelColumnWorkflowResult(column,result,optimization,report,advice)
