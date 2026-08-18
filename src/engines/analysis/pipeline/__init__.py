from dataclasses import dataclass
from enum import Enum

class StageStatus(str,Enum):
    PENDING="pending";RUNNING="running";COMPLETED="completed";FAILED="failed"

@dataclass(frozen=True,slots=True)
class PipelineStageResult:
    name:str
    status:StageStatus
    output:object=None
    error:str|None=None

@dataclass(frozen=True,slots=True)
class AnalysisPipelineResult:
    stages:tuple[PipelineStageResult,...]
    completed:bool

class AnalysisPipeline:
    def run(self,stages,context):
        results=[]
        for name,func in stages:
            try:
                output=func(context)
                context[name]=output
                results.append(PipelineStageResult(name,StageStatus.COMPLETED,output))
            except Exception as exc:
                results.append(PipelineStageResult(name,StageStatus.FAILED,None,str(exc)))
                return AnalysisPipelineResult(tuple(results),False)
        return AnalysisPipelineResult(tuple(results),True)
