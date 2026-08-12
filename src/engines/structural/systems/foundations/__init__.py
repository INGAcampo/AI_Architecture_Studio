from dataclasses import dataclass
from enum import Enum

class FoundationKind(str,Enum):
    ISOLATED="isolated"
    COMBINED="combined"
    STRIP="strip"
    MAT="mat"
    PILE_CAP="pile_cap"
    PEDESTAL="pedestal"

@dataclass(frozen=True,slots=True)
class FoundationElement:
    foundation_id:str
    kind:FoundationKind
    length:float
    width:float
    thickness:float
    material_id:str
    supported_member_ids:tuple[str,...]=()

@dataclass(frozen=True,slots=True)
class FoundationQuantities:
    area:float
    volume:float

class FoundationEngine:
    def quantities(self,f):
        return FoundationQuantities(f.length*f.width,f.length*f.width*f.thickness)
    def bearing_pressure(self,f,vertical_load):
        return vertical_load/self.quantities(f).area
    def validate(self,f):
        issues=[]
        if min(f.length,f.width,f.thickness)<=0: issues.append("invalid_dimensions")
        if not f.supported_member_ids: issues.append("no_supported_members")
        return tuple(issues)
