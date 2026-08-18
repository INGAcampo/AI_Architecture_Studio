"""End-to-end delivery acceptance cases including mandatory approval rejection."""
from __future__ import annotations

from pathlib import Path

from aias_foundation_documentation.orchestrator import FoundationDocumentationOrchestrator

from .engine import FoundationDeliveryEngine
from .issues import IssueRegister
from .models import ApprovalEvidence, CoordinationIssue
from .validation import validate_completeness


def run_reference_cases(workspace: Path) -> list[dict]:
    """Generate source documentation and verify revision, issues and legal boundaries."""
    source = workspace / "source"
    FoundationDocumentationOrchestrator().execute(source)
    issue = CoordinationIssue("CI-001", "Reference coordination", "Review interface", "Structural")
    register = IssueRegister([issue]); register.resolve("CI-001", "Reviewed")
    package = FoundationDeliveryEngine().coordinate(source, issues=register.issues)
    blocked = False
    try: FoundationDeliveryEngine().coordinate(source, request_construction_approval=True)
    except PermissionError: blocked = True
    return [
        {"id": "FCD-000001", "passed": validate_completeness(source)["complete"]},
        {"id": "FCD-000002", "passed": package.source_package == "ECP-000001D"},
        {"id": "FCD-000003", "passed": len(package.revision_manifest.files) >= 6},
        {"id": "FCD-000004", "passed": len(package.revision_manifest.manifest_sha256) == 64},
        {"id": "FCD-000005", "passed": register.open_count == 0},
        {"id": "FCD-000006", "passed": package.delivery_status == "REFERENCE_DELIVERY"},
        {"id": "FCD-000007", "passed": blocked},
        {"id": "FCD-000008", "passed": ApprovalEvidence(True, True, "Engineer", "REG-001", "APP-001").construction_approved},
    ]
