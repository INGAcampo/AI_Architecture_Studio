"""Material-property validation and typed retrieval services."""
from __future__ import annotations
from .models import Material

class MaterialSystem:
    """Enforce minimum material identity, classification and numeric-property rules."""
    def validate(self, material: Material) -> list[str]:
        """Collect missing identity, classification and nonnumeric property issues."""
        issues=[]
        if not material.material_id:
            issues.append("missing_material_id")
        if not material.name:
            issues.append("missing_material_name")
        if not material.category:
            issues.append("missing_material_category")
        if not material.properties:
            issues.append("missing_material_properties")
        for key, value in material.properties.items():
            if not isinstance(value, (int,float)):
                issues.append(f"non_numeric_property:{key}")
        return issues

    def property(self, material: Material, name: str) -> float:
        """Return a required numeric material property as float."""
        if name not in material.properties:
            raise KeyError(name)
        return float(material.properties[name])
