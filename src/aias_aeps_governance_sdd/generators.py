"""Deterministic requirement/specification creation and JSON materialization."""
from dataclasses import asdict
from pathlib import Path
import json
from .models import Requirement, RequirementType, RequirementStatus, Specification

class RequirementGenerator:
    """Create stable draft functional requirements from normalized inputs."""
    def create(self, number: int, title: str, statement: str, rationale: str) -> Requirement:
        """Create a stable draft functional requirement from normalized fields."""
        return Requirement(
            requirement_id=f"REQ-{number:06d}",
            title=title,
            statement=statement,
            requirement_type=RequirementType.FUNCTIONAL,
            status=RequirementStatus.DRAFT,
            rationale=rationale,
        )

class SpecificationGenerator:
    """Create versioned specifications and serialize enum-rich structures safely."""
    def create(self, number: int, title: str, purpose: str, scope: str) -> Specification:
        """Create a semantic-versioned draft specification with stable identity."""
        return Specification(
            specification_id=f"SPEC-{number:06d}",
            title=title,
            version="0.1.0",
            purpose=purpose,
            scope=scope,
        )

    def write_json(self, spec: Specification, path: Path) -> None:
        """Serialize a specification while converting requirement enums to values."""
        row = asdict(spec)
        for req in row["requirements"]:
            req["requirement_type"] = req["requirement_type"].value if hasattr(req["requirement_type"], "value") else req["requirement_type"]
            req["status"] = req["status"].value if hasattr(req["status"], "value") else req["status"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(row, indent=2), encoding="utf-8")
