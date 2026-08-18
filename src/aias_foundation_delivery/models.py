"""Coordination issue, approval, revision and transmittal package contracts."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class IssueStatus(str, Enum):
    """Controlled open or resolved coordination-issue state."""
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"


@dataclass(slots=True)
class CoordinationIssue:
    """Owned delivery-interface issue with explicit resolution evidence."""
    issue_id: str
    title: str
    description: str
    owner: str
    status: IssueStatus = IssueStatus.OPEN
    resolution: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the issue while converting its status enum to a stable value."""
        row = asdict(self)
        row["status"] = self.status.value
        return row


@dataclass(frozen=True, slots=True)
class ApprovalEvidence:
    """Immutable legal and professional evidence required for construction approval."""
    verified_official_code: bool = False
    professional_approval: bool = False
    approver: str | None = None
    license_or_registration: str | None = None
    evidence_reference: str | None = None

    @property
    def construction_approved(self) -> bool:
        """Require verified code, professional identity, registration and evidence."""
        return bool(self.verified_official_code and self.professional_approval and self.approver and self.license_or_registration and self.evidence_reference)


@dataclass(frozen=True, slots=True)
class RevisionManifest:
    """Checksum-protected inventory of every source artifact in a delivery revision."""
    package_id: str
    revision: str
    source_package: str
    created_utc: str
    files: list[dict[str, Any]]
    manifest_sha256: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the immutable revision inventory and canonical checksum."""
        return asdict(self)


@dataclass(slots=True)
class DeliveryPackage:
    """Coordinated transmittal linking completeness, revision, issues and approval."""
    package_id: str
    revision: str
    source_package: str
    delivery_status: str
    completeness: dict[str, Any]
    revision_manifest: RevisionManifest
    issues: list[CoordinationIssue] = field(default_factory=list)
    approval: ApprovalEvidence = field(default_factory=ApprovalEvidence)

    def to_dict(self) -> dict[str, Any]:
        """Serialize transmittal state, manifest, issues and approval evidence."""
        return {
            "package_id": self.package_id,
            "revision": self.revision,
            "source_package": self.source_package,
            "delivery_status": self.delivery_status,
            "completeness": self.completeness,
            "revision_manifest": self.revision_manifest.to_dict(),
            "issues": [issue.to_dict() for issue in self.issues],
            "approval": asdict(self.approval),
        }
