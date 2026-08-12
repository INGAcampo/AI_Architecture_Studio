from dataclasses import dataclass
from enum import Enum

class BraceBehavior(str, Enum):
    TENSION_ONLY="tension_only"
    COMPRESSION_ONLY="compression_only"
    TENSION_COMPRESSION="tension_compression"

class BraceConfiguration(str, Enum):
    SINGLE_DIAGONAL="single_diagonal"
    X_BRACE="x_brace"
    V_BRACE="v_brace"
    INVERTED_V="inverted_v"
    K_BRACE="k_brace"

@dataclass(frozen=True, slots=True)
class SteelBraceDemand:
    axial: float
    shear: float = 0.0

@dataclass(frozen=True, slots=True)
class SteelBrace:
    member_id: str
    profile_id: str
    material_id: str
    length: float
    effective_length_factor: float
    behavior: BraceBehavior
    configuration: BraceConfiguration
    demand: SteelBraceDemand

@dataclass(frozen=True, slots=True)
class SteelBraceDesignResult:
    member_id: str
    tension_capacity: float
    compression_capacity: float
    slenderness: float
    tension_ratio: float
    compression_ratio: float
    unity_ratio: float
    passed: bool
    governing_check: str
