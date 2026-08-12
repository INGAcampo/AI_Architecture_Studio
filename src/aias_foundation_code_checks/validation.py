"""Completeness, numerical and legal-status validation for code checks."""
from __future__ import annotations
import math
from .models import CodePack, DesignInput

REQUIRED_PARAMETERS = {
    "phi_flexure","phi_one_way_shear","phi_punching",
    "min_reinforcement_ratio","max_bar_spacing_mm",
    "one_way_shear_coefficient","punching_shear_coefficient",
    "steel_stress_limit_factor"
}

class CodeCheckValidator:
    """Reject incomplete code packs and physically inconsistent design inputs."""
    def validate_pack(self, pack: CodePack) -> list[str]:
        """Collect missing, nonfinite and legally invalid code-pack parameters."""
        issues=[]
        missing=REQUIRED_PARAMETERS-set(pack.parameters)
        issues.extend(f"missing_parameter:{x}" for x in sorted(missing))
        for k,v in pack.parameters.items():
            if not isinstance(v,(int,float)) or not math.isfinite(float(v)):
                issues.append(f"invalid_parameter:{k}")
        if pack.legal_status not in {"REFERENCE_ONLY","VERIFIED_OFFICIAL","DRAFT"}:
            issues.append("invalid_legal_status")
        return issues

    def validate_input(self, data: DesignInput) -> list[str]:
        """Collect nonphysical geometry, depth and material input conditions."""
        issues=[]
        for name,value in data.__dict__.items() if hasattr(data,"__dict__") else []:
            pass
        positive=[
            data.width_m,data.length_m,data.thickness_m,data.effective_depth_m,
            data.column_width_m,data.column_depth_m,data.concrete_strength_mpa,
            data.steel_yield_strength_mpa,data.cover_m
        ]
        if any((not math.isfinite(v) or v<=0) for v in positive):
            issues.append("invalid_positive_input")
        if data.effective_depth_m>=data.thickness_m:
            issues.append("effective_depth_must_be_less_than_thickness")
        if data.column_width_m>=data.width_m or data.column_depth_m>=data.length_m:
            issues.append("column_must_fit_inside_foundation")
        return issues
