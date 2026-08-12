"""Physical-domain and family-specific validation for foundation objects."""
from __future__ import annotations
import math
from .models import FoundationObject
from .enums import FoundationType

class FoundationValidator:
    """Collect invalid geometry, soil, material, cover and support conditions."""
    def validate(self, obj: FoundationObject) -> list[str]:
        """Collect geometry, soil, material, cover and family-support violations."""
        issues=[]
        g=obj.geometry
        for name,value in (("width",g.width_m),("length",g.length_m),("thickness",g.thickness_m)):
            if not math.isfinite(value) or value <= 0:
                issues.append(f"invalid_{name}")
        if obj.soil.allowable_bearing_pressure_kpa <= 0:
            issues.append("invalid_allowable_bearing_pressure")
        if obj.concrete_strength_mpa <= 0:
            issues.append("invalid_concrete_strength")
        if obj.steel_yield_strength_mpa <= 0:
            issues.append("invalid_steel_strength")
        if obj.cover_m <= 0 or obj.cover_m >= g.thickness_m:
            issues.append("invalid_cover")
        if not obj.supports and obj.foundation_type != FoundationType.FOUNDATION_BEAM:
            issues.append("missing_supports")
        if obj.foundation_type == FoundationType.COMBINED and len(obj.supports) < 2:
            issues.append("combined_requires_two_supports")
        return issues
