from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CriticalMember:
    member_id:str
    member_type:str
    unity_ratio:float
    governing_check:str

@dataclass(frozen=True, slots=True)
class SteelFrameDashboard:
    total_members:int
    passed_members:int
    failed_members:int
    maximum_unity:float
    critical_members:tuple[CriticalMember,...]

class CriticalMemberDashboardEngine:
    def build(self,batch,threshold=0.9):
        critical=tuple(
            CriticalMember(r.member_id,r.member_type,r.unity_ratio,r.governing_check)
            for r in sorted(batch.records,key=lambda x:x.unity_ratio,reverse=True)
            if r.unity_ratio>=threshold
        )
        return SteelFrameDashboard(len(batch.records),batch.passed_count,batch.failed_count,batch.maximum_unity,critical)
