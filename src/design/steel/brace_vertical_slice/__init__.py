from dataclasses import dataclass
from design.steel.brace_domain import SteelBrace,SteelBraceDemand,BraceBehavior,BraceConfiguration
from design.steel.brace_design_engine import SteelBraceDesignEngine
from design.steel.brace_optimizer import SteelBraceOptimizer
from design.steel.stability_index import StabilityIndexEngine
from design.steel.brace_report_advisor import BraceReportAdvisor

@dataclass(frozen=True, slots=True)
class BraceStabilityWorkflowResult:
    brace:object
    design_result:object
    optimization_result:object
    story_stability:object
    report:object
    advice:object

class BraceStabilityVerticalSlice:
    def __init__(self,profiles,materials):
        self.profiles=profiles; self.materials=materials
        self.design=SteelBraceDesignEngine()
        self.optimizer=SteelBraceOptimizer(self.design)
        self.stability=StabilityIndexEngine()
        self.report_advisor=BraceReportAdvisor()

    def run(self,member_id,profile_id,material_id,length,axial,vertical_load,drift,story_shear,story_height):
        brace=SteelBrace(member_id,profile_id,material_id,length,1.0,BraceBehavior.TENSION_COMPRESSION,BraceConfiguration.X_BRACE,SteelBraceDemand(axial))
        profile=self.profiles.get(profile_id); material=self.materials.get(material_id)
        design=self.design.design(brace,profile,material)
        optimization=self.optimizer.optimize(brace,profile,material,self.profiles.all())
        stability=self.stability.calculate("STORY-1",vertical_load,drift,story_shear,story_height)
        batch=type("Batch",(),{"results":(design,),"passed_count":1 if design.passed else 0,"failed_count":0 if design.passed else 1,"maximum_unity":design.unity_ratio})()
        report=self.report_advisor.build_report(batch)
        advice=self.report_advisor.advise(batch)
        return BraceStabilityWorkflowResult(brace,design,optimization,stability,report,advice)
