"""Foundation documentation completeness and approval coordination engine."""
from __future__ import annotations

from pathlib import Path

from .models import ApprovalEvidence, CoordinationIssue, DeliveryPackage
from .revisions import create_revision_manifest
from .validation import delivery_status, validate_completeness, validate_construction_approval


class FoundationDeliveryEngine:
    """Create a revisioned delivery only after artifact and professional gates pass."""
    def coordinate(self, source: Path, revision: str = "R00", approval: ApprovalEvidence | None = None, issues: list[CoordinationIssue] | None = None, request_construction_approval: bool = False) -> DeliveryPackage:
        """Validate source completeness and create a revisioned approval-aware package."""
        approval = approval or ApprovalEvidence()
        completeness = validate_completeness(source)
        if not completeness["complete"]:
            raise FileNotFoundError("incomplete_ecp000001d_package:" + ",".join(completeness["missing"]))
        validate_construction_approval(request_construction_approval, approval)
        package_id = f"ECP-000001E-{revision}"
        manifest = create_revision_manifest(source, package_id, revision, "ECP-000001D")
        return DeliveryPackage(package_id, revision, "ECP-000001D", delivery_status(approval), completeness, manifest, list(issues or []), approval)
