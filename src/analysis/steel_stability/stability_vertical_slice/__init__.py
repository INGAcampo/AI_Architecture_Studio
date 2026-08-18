from analysis.steel_stability.stability_pipeline import StabilityPipeline
from analysis.steel_stability.stability_diagnostics import StabilityDiagnostics
from analysis.steel_stability.ai_stability_advisor import AiStabilityAdvisor
from analysis.steel_stability.stability_report import StabilityReport
class StabilityVerticalSlice:
    def run(self):
        member_id,slenderness,result=StabilityPipeline().run_demo()
        diagnostics=StabilityDiagnostics().messages(result,slenderness)
        advice=AiStabilityAdvisor().advise(result)
        report=StabilityReport().build(member_id,result,slenderness)
        return member_id,slenderness,result,diagnostics,advice,report
