from dataclasses import dataclass
from enum import Enum
class AnalyticalObjectKind(str,Enum): NODE="node"; MEMBER="member"; PANEL="panel"; SUPPORT="support"; LOAD="load"
@dataclass(frozen=True,slots=True)
class AnalyticalObject:
    object_id:str; kind:AnalyticalObjectKind; source_id:str; active:bool=True
    def __post_init__(self):
        if not self.object_id.strip() or not self.source_id.strip(): raise ValueError("Identificadores obligatorios")
