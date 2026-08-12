from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class AnalyticalMember:
    member_id:str
    start_node_id:str
    end_node_id:str
    length:float
    local_axes:object
    start_release:object
    end_release:object

@dataclass(frozen=True,slots=True)
class AnalyticalModel:
    node_ids:tuple[str,...]
    members:tuple[AnalyticalMember,...]

class AnalyticalModelEngine:
    def build_member(self,member,start_node_id,end_node_id,coordinate_system):
        axes=coordinate_system.member_axes(member.start,member.end)
        return AnalyticalMember(member.member_id,start_node_id,end_node_id,member.length,axes,member.start_release,member.end_release)
    def build_model(self,nodes,members):
        return AnalyticalModel(tuple(sorted(n.node_id for n in nodes)),tuple(sorted(members,key=lambda m:m.member_id)))
