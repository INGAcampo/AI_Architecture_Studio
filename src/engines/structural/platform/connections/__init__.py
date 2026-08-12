from dataclasses import dataclass
from enum import Enum

class ConnectionType(str,Enum):
    RIGID="rigid";PINNED="pinned";SEMI_RIGID="semi_rigid"

@dataclass(frozen=True,slots=True)
class StructuralConnection:
    connection_id:str
    node_id:str
    member_ids:tuple[str,...]
    connection_type:ConnectionType
    rotational_stiffness:float=0.0

class StructuralConnectionEngine:
    def __init__(self): self._connections={}
    def add(self,c):
        if c.connection_id in self._connections: raise ValueError("Conexión duplicada")
        if len(c.member_ids)<2: raise ValueError("Se requieren al menos dos miembros")
        self._connections[c.connection_id]=c;return c
    def for_member(self,member_id):
        return tuple(sorted((c for c in self._connections.values() if member_id in c.member_ids),key=lambda c:c.connection_id))
    def validate(self,c):
        issues=[]
        if c.connection_type is ConnectionType.SEMI_RIGID and c.rotational_stiffness<=0: issues.append("missing_rotational_stiffness")
        return tuple(issues)
