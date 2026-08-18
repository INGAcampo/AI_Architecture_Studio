"""Structural and numerical validation rules for canonical engineering objects."""
from __future__ import annotations
import math
from .models import EngineeringObject
from .identity import EngineeringIdentityService
from .materials import MaterialSystem

class EngineeringObjectValidator:
    """Collect identity, completeness, material and finite-load validation issues."""
    def validate(self, obj: EngineeringObject) -> list[str]:
        """Collect identity, completeness, material and nonfinite-load issues."""
        issues=[]
        if not EngineeringIdentityService().validate(obj.object_id):
            issues.append("invalid_object_id")
        if not obj.object_type.strip():
            issues.append("missing_object_type")
        if not obj.name.strip():
            issues.append("missing_name")
        if not obj.geometry:
            issues.append("missing_geometry")
        if not obj.traceability:
            issues.append("missing_traceability")
        if not obj.materials:
            issues.append("missing_materials")
        for material in obj.materials:
            issues.extend(MaterialSystem().validate(material))
        for load in obj.loads:
            if not math.isfinite(load.magnitude):
                issues.append(f"non_finite_load:{load.load_id}")
        return issues
