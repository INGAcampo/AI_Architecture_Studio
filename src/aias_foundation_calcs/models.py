"""Typed inputs and results for the shallow-foundation calculation pipeline."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class LoadCase:
    """Named axial, biaxial moment and bidirectional shear action set."""
    name: str
    axial_kn: float
    moment_x_knm: float = 0.0
    moment_y_knm: float = 0.0
    shear_x_kn: float = 0.0
    shear_y_kn: float = 0.0

@dataclass(slots=True)
class LoadCombination:
    """Named mapping of load-case identifiers to scalar combination factors."""
    name: str
    factors: dict[str, float]

@dataclass(slots=True)
class FoundationInput:
    """Geometry, material, soil and loading inputs using explicit SI-derived units."""
    width_m: float
    length_m: float
    thickness_m: float
    column_width_m: float
    column_depth_m: float
    allowable_bearing_pressure_kpa: float
    concrete_unit_weight_kn_m3: float = 24.0
    concrete_strength_mpa: float = 30.0
    steel_yield_strength_mpa: float = 420.0
    cover_m: float = 0.075
    soil_modulus_mpa: float | None = None
    poisson_ratio: float = 0.30
    load_cases: dict[str, LoadCase] = field(default_factory=dict)
    combinations: list[LoadCombination] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class BearingResult:
    """Computed soil pressures, eccentricities and service acceptance indicators."""
    q_avg_kpa: float
    q_max_kpa: float
    q_min_kpa: float
    eccentricity_x_m: float
    eccentricity_y_m: float
    kern_ok: bool
    allowable_ok: bool

@dataclass(slots=True)
class DemandResult:
    """Generic one-way shear, punching and biaxial moment demand envelope values."""
    one_way_shear_x_kn: float
    one_way_shear_y_kn: float
    punching_shear_kn: float
    moment_x_knm: float
    moment_y_knm: float

@dataclass(slots=True)
class SettlementResult:
    """Immediate-settlement estimate plus method and availability classification."""
    immediate_settlement_mm: float | None
    method: str
    available: bool

@dataclass(slots=True)
class CombinationResult:
    """Complete resultant, bearing, demand and settlement record for one combination."""
    combination: str
    resultant: LoadCase
    bearing: BearingResult
    demands: DemandResult
    settlement: SettlementResult

@dataclass(slots=True)
class CalculationPackage:
    """All combination results, governing cases and quality-boundary declarations."""
    results: list[CombinationResult]
    governing: dict[str, str]
    qa: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Recursively serialize combination results and quality declarations."""
        return asdict(self)
