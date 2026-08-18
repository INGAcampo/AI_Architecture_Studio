from dataclasses import dataclass
from enum import Enum
class LoadKind(str, Enum):
    DEAD="dead"; LIVE="live"; WIND="wind"; SEISMIC="seismic"; SNOW="snow"; TEMPERATURE="temperature"
@dataclass(frozen=True, slots=True)
class NodalLoad:
    load_id:str; node_id:str; kind:LoadKind; fx:float=0; fy:float=0; fz:float=0
    def __post_init__(self):
        if not self.load_id.strip() or not self.node_id.strip(): raise ValueError("Identificadores obligatorios")
    @property
    def magnitude(self): return (self.fx**2+self.fy**2+self.fz**2)**0.5
class LoadEngine:
    def __init__(self): self.items={}
    def add(self, load):
        if load.load_id in self.items: raise KeyError(load.load_id)
        self.items[load.load_id]=load; return load
    def resultant(self, node_id):
        items=[x for x in self.items.values() if x.node_id==node_id]
        return (sum(x.fx for x in items),sum(x.fy for x in items),sum(x.fz for x in items))
