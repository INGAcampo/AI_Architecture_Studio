from dataclasses import dataclass
from enum import Enum
from math import pi
class RcMemberKind(str,Enum): BEAM="beam"; COLUMN="column"; SLAB="slab"; WALL="wall"; FOOTING="footing"
@dataclass(frozen=True,slots=True)
class Rebar:
    bar_id:str; diameter:float; count:int; length:float
    def __post_init__(self):
        if not self.bar_id.strip() or min(self.diameter,self.length)<=0 or self.count<1: raise ValueError("Datos inválidos")
    @property
    def area_each(self): return pi*self.diameter**2/4
    @property
    def total_area(self): return self.area_each*self.count
    @property
    def total_length(self): return self.length*self.count
@dataclass(frozen=True,slots=True)
class RcMember:
    member_id:str; kind:RcMemberKind; concrete_volume:float; rebars:tuple[Rebar,...]
    def __post_init__(self):
        if not self.member_id.strip() or self.concrete_volume<=0: raise ValueError("Datos inválidos")
