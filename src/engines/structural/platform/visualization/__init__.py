from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class MemberVisual:
    member_id:str
    line:tuple[tuple[float,float,float],tuple[float,float,float]]
    label:str
    utilization:float=0.0

class StructuralVisualizationEngine:
    def member_visual(self,member,utilization=0.0):
        return MemberVisual(member.member_id,(member.start,member.end),f"{member.kind.value}:{member.section_id}",float(utilization))
    def filter_by_utilization(self,visuals,minimum):
        return tuple(v for v in visuals if v.utilization>=minimum)
