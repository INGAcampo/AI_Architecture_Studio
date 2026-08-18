"""Normative-pack, design-input and code-check result contracts for foundations."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class CodePack:
    """Versioned jurisdictional parameter set with legal status and source metadata."""
    code_id: str
    title: str
    jurisdiction: str
    edition: str
    legal_status: str
    parameters: dict[str, float]
    applicability: list[str]
    source_metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class DesignInput:
    """Factored geometry, material strengths and structural demands in explicit units."""
    width_m: float
    length_m: float
    thickness_m: float
    effective_depth_m: float
    column_width_m: float
    column_depth_m: float
    concrete_strength_mpa: float
    steel_yield_strength_mpa: float
    cover_m: float
    factored_moment_x_knm: float
    factored_moment_y_knm: float
    factored_one_way_shear_x_kn: float
    factored_one_way_shear_y_kn: float
    factored_punching_shear_kn: float

@dataclass(slots=True)
class CheckResult:
    """Equation-traceable demand-capacity comparison and utilization outcome."""
    check_id: str
    demand: float
    capacity: float
    utilization: float
    passed: bool
    units: str
    equation_id: str
    notes: list[str] = field(default_factory=list)

@dataclass(slots=True)
class ReinforcementResult:
    """Required, minimum and governing reinforcement areas for both footing axes."""
    required_area_x_mm2: float
    required_area_y_mm2: float
    minimum_area_x_mm2: float
    minimum_area_y_mm2: float
    governing_area_x_mm2: float
    governing_area_y_mm2: float
    suggested_spacing_x_mm: float | None
    suggested_spacing_y_mm: float | None

@dataclass(slots=True)
class CodeCheckPackage:
    """Code-pack snapshot, checks, reinforcement design and QA/legal declarations."""
    code_pack: dict[str, Any]
    checks: list[CheckResult]
    reinforcement: ReinforcementResult
    qa: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Serialize code provenance, checks, reinforcement and QA recursively."""
        return asdict(self)
