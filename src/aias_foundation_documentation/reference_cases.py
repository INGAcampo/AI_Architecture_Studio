"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

from aias_foundation_calcs.engine import FoundationCalculationEngine
from aias_foundation_calcs.reference_cases import reference_input as calculation_input
from aias_foundation_code_checks.engine import FoundationCodeCheckEngine
from aias_foundation_code_checks.reference_pack import generic_reference_pack, reference_input as check_input
from aias_foundation_objects.reference_cases import reference_objects

from .engine import FoundationDocumentationEngine


def reference_package(workspace):
    """Execute the public reference_package operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    foundation = reference_objects()["isolated"]
    calculation = FoundationCalculationEngine().calculate(calculation_input())
    checks = FoundationCodeCheckEngine().check(check_input(), generic_reference_pack())
    return FoundationDocumentationEngine().generate(foundation, calculation, checks, workspace)


def run_reference_cases(workspace):
    """Execute run reference cases for foundation drawings, schedules and technical documentation with validated state transitions."""
    package = reference_package(workspace)
    return [
        {"id": "FDD-000001", "passed": len(package.bar_schedule) == 2},
        {"id": "FDD-000002", "passed": package.quantities.concrete_m3 > 0},
        {"id": "FDD-000003", "passed": package.quantities.reinforcement_kg > 0},
        {"id": "FDD-000004", "passed": len(package.drawing_manifest) == 2},
        {"id": "FDD-000005", "passed": all(item["path"].endswith(".svg") for item in package.drawing_manifest)},
        {"id": "FDD-000006", "passed": package.traceability["check_source"] == "ECP-000001C"},
        {"id": "FDD-000007", "passed": package.qa["human_review_required"]},
        {"id": "FDD-000008", "passed": package.qa["verified_official_required_for_construction"]},
    ]
