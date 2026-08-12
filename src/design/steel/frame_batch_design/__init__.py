from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class FrameMemberDesignRecord:
    member_id:str
    member_type:str
    unity_ratio:float
    passed:bool
    governing_check:str

@dataclass(frozen=True, slots=True)
class FrameBatchDesignResult:
    records:tuple[FrameMemberDesignRecord,...]
    passed_count:int
    failed_count:int
    maximum_unity:float

class FrameBatchDesignEngine:
    def design(self,beam_results,column_results,brace_results):
        records=[]
        for kind,items in (("beam",beam_results),("column",column_results),("brace",brace_results)):
            for r in items:
                records.append(FrameMemberDesignRecord(r.member_id,kind,r.unity_ratio,r.passed,r.governing_check))
        passed=sum(1 for r in records if r.passed)
        return FrameBatchDesignResult(tuple(records),passed,len(records)-passed,max((r.unity_ratio for r in records),default=0.0))
