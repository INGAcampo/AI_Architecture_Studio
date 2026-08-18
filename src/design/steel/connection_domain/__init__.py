from dataclasses import dataclass
from enum import Enum
class ConnectionFamily(str,Enum):
    SHEAR="shear"; MOMENT="moment"; SPLICE="splice"; BRACE="brace"; BASE="base"
class ConnectionMethod(str,Enum):
    BOLTED="bolted"; WELDED="welded"; HYBRID="hybrid"
@dataclass(frozen=True,slots=True)
class ConnectionDemand:
    shear:float=0.0; axial:float=0.0; moment:float=0.0; torsion:float=0.0
@dataclass(frozen=True,slots=True)
class SteelConnection:
    connection_id:str; family:ConnectionFamily; method:ConnectionMethod
    beam_profile_id:str; support_profile_id:str; demand:ConnectionDemand
@dataclass(frozen=True,slots=True)
class ConnectionCheck:
    name:str; ratio:float; passed:bool
@dataclass(frozen=True,slots=True)
class ConnectionDesignResult:
    connection_id:str; checks:tuple[ConnectionCheck,...]; unity_ratio:float; passed:bool; governing_check:str
