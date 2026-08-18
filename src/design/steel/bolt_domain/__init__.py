from dataclasses import dataclass
from enum import Enum

class BoltGrade(str, Enum):
    A325="A325"
    A490="A490"
    ISO_8_8="8.8"
    ISO_10_9="10.9"

class BoltHoleType(str, Enum):
    STANDARD="standard"
    OVERSIZED="oversized"
    SHORT_SLOT="short_slot"
    LONG_SLOT="long_slot"

class BoltConnectionType(str, Enum):
    BEARING="bearing"
    SLIP_CRITICAL="slip_critical"

@dataclass(frozen=True, slots=True)
class BoltMaterial:
    grade:BoltGrade
    nominal_tensile_strength:float
    nominal_shear_strength:float

@dataclass(frozen=True, slots=True)
class Bolt:
    bolt_id:str
    diameter:float
    material:BoltMaterial
    hole_type:BoltHoleType=BoltHoleType.STANDARD
    connection_type:BoltConnectionType=BoltConnectionType.BEARING
    threads_in_shear_plane:bool=True

@dataclass(frozen=True, slots=True)
class BoltGroupDemand:
    shear_x:float=0.0
    shear_y:float=0.0
    tension:float=0.0
    moment:float=0.0

@dataclass(frozen=True, slots=True)
class BoltDesignResult:
    bolt_id:str
    shear_capacity:float
    tension_capacity:float
    bearing_capacity:float
    slip_capacity:float
    shear_ratio:float
    tension_ratio:float
    interaction_ratio:float
    unity_ratio:float
    passed:bool
    governing_check:str
