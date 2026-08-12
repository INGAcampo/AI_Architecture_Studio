from dataclasses import dataclass
from enum import Enum

class BucklingAxis(str, Enum):
    MAJOR="major"
    MINOR="minor"

class ColumnEndCondition(str, Enum):
    PINNED_PINNED="pinned_pinned"
    FIXED_FIXED="fixed_fixed"
    FIXED_PINNED="fixed_pinned"
    FIXED_FREE="fixed_free"
    CUSTOM="custom"

@dataclass(frozen=True, slots=True)
class EffectiveLength:
    actual_length: float
    factor_k: float

    @property
    def value(self) -> float:
        return self.actual_length * self.factor_k

@dataclass(frozen=True, slots=True)
class SteelColumnDemand:
    axial: float
    moment_major: float = 0.0
    moment_minor: float = 0.0
    shear_major: float = 0.0
    shear_minor: float = 0.0

@dataclass(frozen=True, slots=True)
class SteelColumn:
    member_id: str
    profile_id: str
    material_id: str
    length: float
    end_condition_major: ColumnEndCondition
    end_condition_minor: ColumnEndCondition
    demand: SteelColumnDemand
    k_major: float | None = None
    k_minor: float | None = None

@dataclass(frozen=True, slots=True)
class SteelColumnDesignResult:
    member_id: str
    slenderness_major: float
    slenderness_minor: float
    critical_axis: BucklingAxis
    compression_capacity: float
    axial_ratio: float
    major_bending_ratio: float
    minor_bending_ratio: float
    interaction_ratio: float
    unity_ratio: float
    passed: bool
    governing_check: str
