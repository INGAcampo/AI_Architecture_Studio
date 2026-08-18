"""Public module supporting the second Omega integrated product release."""
from __future__ import annotations
from dataclasses import dataclass
from aias_omega_core.project import EngineeringProject

@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Execute the public ValidationIssue operation for the second Omega integrated product release using explicit caller inputs."""
    severity: str
    code: str
    message: str
    object_id: str = ""

class ProjectValidator:
    """Execute the public ProjectValidator operation for the second Omega integrated product release using explicit caller inputs."""
    def validate(self, project: EngineeringProject) -> tuple[ValidationIssue, ...]:
        """Validate validate for the second Omega integrated product release and report explicit issues."""
        issues = []
        known_materials = {m.material_id for m in project.materials.all()}

        for object_id, obj in project.objects.items():
            if obj.material_id and obj.material_id not in known_materials:
                issues.append(ValidationIssue(
                    "error",
                    "MATERIAL_MISSING",
                    f"Unknown material: {obj.material_id}",
                    str(object_id),
                ))

            if obj.object_type == "bim_wall":
                for key in ("length_m", "height_m", "thickness_m"):
                    if float(obj.properties.get(key, 0.0)) <= 0:
                        issues.append(ValidationIssue(
                            "error",
                            "WALL_DIMENSION_INVALID",
                            f"{key} must be positive.",
                            str(object_id),
                        ))

            if obj.object_type == "structural_member":
                if float(obj.properties.get("area_m2", 0.0)) <= 0:
                    issues.append(ValidationIssue(
                        "error",
                        "STRUCTURAL_AREA_INVALID",
                        "Structural area must be positive.",
                        str(object_id),
                    ))

        object_ids = set(project.objects)
        for relation in project.graph.all():
            if relation.source not in object_ids or relation.target not in object_ids:
                issues.append(ValidationIssue(
                    "error",
                    "BROKEN_RELATIONSHIP",
                    "Relationship references a missing object.",
                ))

        return tuple(issues)
