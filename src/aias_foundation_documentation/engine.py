"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from aias_foundation_calcs.models import CalculationPackage
from aias_foundation_code_checks.models import CodeCheckPackage
from aias_foundation_objects.models import FoundationObject

from .detailing import ReinforcementDetailer
from .drawings import FoundationSvgWriter
from .models import DocumentationPackage
from .quantities import QuantityEngine


class FoundationDocumentationEngine:
    """Execute the public FoundationDocumentationEngine operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    def generate(self, foundation: FoundationObject, calculation: CalculationPackage, checks: CodeCheckPackage, workspace: Path) -> DocumentationPackage:
        """Build the generate required by foundation drawings, schedules and technical documentation from explicit inputs."""
        if not calculation.results:
            raise ValueError("calculation_package_has_no_results")
        if not checks.checks:
            raise ValueError("code_check_package_has_no_checks")
        bars = ReinforcementDetailer().detail(foundation, checks.reinforcement)
        quantities = QuantityEngine().calculate(foundation, bars)
        drawings = workspace / "drawings"
        writer = FoundationSvgWriter()
        plan = writer.write_plan(foundation, bars, drawings / "foundation_plan.svg")
        section = writer.write_section(foundation, bars, drawings / "foundation_section.svg")
        code_status = checks.code_pack.get("legal_status", "UNKNOWN")
        all_checks_passed = all(item.passed for item in checks.checks)
        return DocumentationPackage(
            package_id=f"ECP-D-{foundation.object_id}",
            foundation=foundation.to_dict(),
            calculation=calculation.to_dict(),
            code_checks=checks.to_dict(),
            bar_schedule=bars,
            quantities=quantities,
            drawing_manifest=[{"id": "FND-PLAN-001", "path": str(plan)}, {"id": "FND-SECTION-001", "path": str(section)}],
            notes=["Dimensions shall be verified against the coordinated model.", "Do not scale drawings.", "Construction use requires a verified official code pack and professional approval."],
            traceability={"object_source": "ECP-000001A", "calculation_source": "ECP-000001B", "check_source": "ECP-000001C", "document_source": "ECP-000001D"},
            qa={"all_checks_passed": all_checks_passed, "legal_status": code_status, "human_review_required": True, "verified_official_required_for_construction": code_status != "VERIFIED_OFFICIAL", "drawing_count": 2},
        )
