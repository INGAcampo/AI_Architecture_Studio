"""Input-domain validation for shallow-foundation calculation packages."""
from __future__ import annotations
import math
from .models import FoundationInput

class FoundationCalculationValidator:
    """Collect geometry, material, cover, soil and loading consistency violations."""
    def validate(self, data: FoundationInput) -> list[str]:
        """Collect nonphysical dimensions, cover, material and loading issues."""
        issues=[]
        positive={
            "width_m":data.width_m,"length_m":data.length_m,"thickness_m":data.thickness_m,
            "column_width_m":data.column_width_m,"column_depth_m":data.column_depth_m,
            "allowable_bearing_pressure_kpa":data.allowable_bearing_pressure_kpa,
            "concrete_strength_mpa":data.concrete_strength_mpa,
            "steel_yield_strength_mpa":data.steel_yield_strength_mpa,
        }
        for name,value in positive.items():
            if not math.isfinite(value) or value<=0:
                issues.append(f"invalid_{name}")
        if data.column_width_m>=data.width_m:
            issues.append("column_width_must_be_less_than_footing")
        if data.column_depth_m>=data.length_m:
            issues.append("column_depth_must_be_less_than_footing")
        if data.cover_m<=0 or data.cover_m>=data.thickness_m:
            issues.append("invalid_cover")
        if not data.load_cases:
            issues.append("missing_load_cases")
        if not data.combinations:
            issues.append("missing_combinations")
        return issues
