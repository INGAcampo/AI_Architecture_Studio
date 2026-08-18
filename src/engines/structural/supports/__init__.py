from dataclasses import dataclass
from enum import Enum
class SupportKind(str, Enum):
    FIXED="fixed"; PINNED="pinned"; ROLLER="roller"; SPRING="spring"; CUSTOM="custom"
@dataclass(frozen=True, slots=True)
class Support:
    support_id:str; node_id:str; kind:SupportKind
    ux:bool=True; uy:bool=True; uz:bool=True; rx:bool=True; ry:bool=True; rz:bool=True
    def __post_init__(self):
        if not self.support_id.strip() or not self.node_id.strip(): raise ValueError("Identificadores obligatorios")
    @property
    def restrained_dofs(self): return sum((self.ux,self.uy,self.uz,self.rx,self.ry,self.rz))
class SupportEngine:
    def __init__(self): self.items={}
    def add(self, support):
        if support.support_id in self.items: raise KeyError(support.support_id)
        self.items[support.support_id]=support; return support
    def for_node(self,node_id): return tuple(x for x in self.items.values() if x.node_id==node_id)
