from dataclasses import dataclass
from engines.analysis.pipeline import AnalysisPipeline

@dataclass(frozen=True,slots=True)
class AnalysisRun:
    run_id:str
    project_id:str
    pipeline_result:object

class AnalysisManager:
    def __init__(self):
        self.pipeline=AnalysisPipeline()
        self.runs={}

    def execute(self,run_id,project,stages):
        result=self.pipeline.run(stages,{"project":project})
        run=AnalysisRun(run_id,project.project_id,result)
        self.runs[run_id]=run
        return run

    def get_run(self,run_id): return self.runs[run_id]
