from dataclasses import dataclass
from engines.analysis.results_db import StructuralResultsDatabase

@dataclass(frozen=True,slots=True)
class ProfessionalAnalysisResult:
    run_id:str
    completed:bool
    pipeline_result:object
    results_db:StructuralResultsDatabase

class ProfessionalStructuralAnalysisPlatform:
    def __init__(self,analysis_manager):
        self.analysis_manager=analysis_manager

    def analyze(self,run_id,project,stages):
        run=self.analysis_manager.execute(run_id,project,stages)
        db=StructuralResultsDatabase()
        if run.pipeline_result.completed:
            context={s.name:s.output for s in run.pipeline_result.stages}
            for key,value in context.items():
                db.metadata[key]=value
        return ProfessionalAnalysisResult(run_id,run.pipeline_result.completed,run.pipeline_result,db)
