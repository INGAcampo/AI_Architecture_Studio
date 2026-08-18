"""Artifact completeness, delivery classification and construction-approval gates."""
from __future__ import annotations

from pathlib import Path

from .models import ApprovalEvidence


REQUIRED_ARTIFACTS = (
    "drawings/foundation_plan.svg",
    "drawings/foundation_section.svg",
    "technical_file/bar_schedule.csv",
    "technical_file/foundation_documentation.json",
    "technical_file/FOUNDATION_TECHNICAL_REPORT.md",
    "qa/reference_cases.json",
)


def validate_completeness(source: Path) -> dict:
    """Report present and missing mandatory drawings, schedules, reports and QA files."""
    present = [item for item in REQUIRED_ARTIFACTS if (source / item).is_file()]
    missing = [item for item in REQUIRED_ARTIFACTS if item not in present]
    return {"complete": not missing, "required_count": len(REQUIRED_ARTIFACTS), "present": present, "missing": missing}


def delivery_status(approval: ApprovalEvidence) -> str:
    """Classify a package without implying construction approval absent full evidence."""
    return "CONSTRUCTION_APPROVED" if approval.construction_approved else "REFERENCE_DELIVERY"


def validate_construction_approval(requested: bool, approval: ApprovalEvidence) -> None:
    """Reject requested construction use unless code and professional evidence are complete."""
    if requested and not approval.construction_approved:
        raise PermissionError("construction_approval_requires_verified_official_code_and_professional_evidence")
