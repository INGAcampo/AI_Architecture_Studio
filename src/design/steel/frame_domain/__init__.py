from dataclasses import dataclass, field
from enum import Enum

class FrameMemberType(str, Enum):
    BEAM="beam"
    COLUMN="column"
    BRACE="brace"

@dataclass(frozen=True, slots=True)
class FrameNode:
    node_id:str
    x:float
    y:float
    z:float

@dataclass(frozen=True, slots=True)
class FrameMemberRef:
    member_id:str
    member_type:FrameMemberType
    start_node_id:str
    end_node_id:str
    profile_id:str
    material_id:str

@dataclass(slots=True)
class SteelFrame:
    frame_id:str
    nodes:dict[str,FrameNode]=field(default_factory=dict)
    members:dict[str,FrameMemberRef]=field(default_factory=dict)

    def add_node(self,node):
        self.nodes[node.node_id]=node
        return node

    def add_member(self,member):
        if member.start_node_id not in self.nodes or member.end_node_id not in self.nodes:
            raise ValueError("Nodos del miembro no registrados")
        self.members[member.member_id]=member
        return member

    def members_by_type(self,member_type):
        return tuple(m for m in self.members.values() if m.member_type is member_type)
