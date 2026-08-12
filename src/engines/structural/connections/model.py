from dataclasses import dataclass
from enum import Enum
class ConnectionKind(str,Enum): SHEAR_TAB="shear_tab"; END_PLATE="end_plate"; BASE_PLATE="base_plate"; MOMENT="moment"; SPLICE="splice"
@dataclass(frozen=True,slots=True)
class BoltGroup:
    rows:int; columns:int; diameter:float; spacing_x:float; spacing_y:float
    def __post_init__(self):
        if min(self.rows,self.columns)<1 or min(self.diameter,self.spacing_x,self.spacing_y)<=0: raise ValueError("Datos inválidos")
    @property
    def count(self): return self.rows*self.columns
@dataclass(frozen=True,slots=True)
class SteelConnection:
    connection_id:str; kind:ConnectionKind; member_ids:tuple[str,...]; plate_thickness:float; bolts:BoltGroup
    def __post_init__(self):
        if not self.connection_id.strip() or len(self.member_ids)<2 or self.plate_thickness<=0: raise ValueError("Datos inválidos")
