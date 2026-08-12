import json
import zipfile

import pytest

from aias_foundation_documentation.orchestrator import FoundationDocumentationOrchestrator
from aias_foundation_delivery.engine import FoundationDeliveryEngine
from aias_foundation_delivery.issues import IssueRegister
from aias_foundation_delivery.models import ApprovalEvidence, CoordinationIssue
from aias_foundation_delivery.orchestrator import FoundationDeliveryOrchestrator
from aias_foundation_delivery.revisions import create_revision_manifest
from aias_foundation_delivery.validation import validate_completeness


@pytest.fixture()
def source(tmp_path):
    path = tmp_path / "ecpd"; FoundationDocumentationOrchestrator().execute(path); return path


def test_complete_ecpd_package(source): assert validate_completeness(source)["complete"]
def test_incomplete_package_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError): FoundationDeliveryEngine().coordinate(tmp_path)
def test_revision_manifest_has_checksums(source):
    result = create_revision_manifest(source, "PKG", "R00", "ECP-000001D"); assert result.files and all(len(row["sha256"]) == 64 for row in result.files)
def test_manifest_is_deterministic_for_same_content(source):
    a = create_revision_manifest(source, "PKG", "R00", "D"); b = create_revision_manifest(source, "PKG", "R00", "D"); assert a.manifest_sha256 == b.manifest_sha256
def test_issue_register_lifecycle():
    register = IssueRegister(); register.add(CoordinationIssue("CI-1", "Title", "Description", "Owner")); assert register.open_count == 1; register.resolve("CI-1", "Done"); assert register.open_count == 0
def test_duplicate_issue_is_rejected():
    issue = CoordinationIssue("CI-1", "Title", "Description", "Owner"); register = IssueRegister([issue])
    with pytest.raises(ValueError): register.add(issue)
def test_default_delivery_is_reference_only(source): assert FoundationDeliveryEngine().coordinate(source).delivery_status == "REFERENCE_DELIVERY"
def test_unsubstantiated_construction_approval_is_blocked(source):
    with pytest.raises(PermissionError): FoundationDeliveryEngine().coordinate(source, request_construction_approval=True)
def test_complete_approval_evidence_allows_status(source):
    approval = ApprovalEvidence(True, True, "Licensed Engineer", "REG-001", "SIGNED-001"); assert FoundationDeliveryEngine().coordinate(source, approval=approval, request_construction_approval=True).delivery_status == "CONSTRUCTION_APPROVED"
def test_orchestrator_creates_transmittal_and_archive(tmp_path):
    result = FoundationDeliveryOrchestrator().execute(tmp_path / "delivery")
    archive = tmp_path / "delivery" / "release" / "ECP-000001E_FOUNDATION_COORDINATION_DELIVERY_1.0.0_R00.zip"
    assert result["validated"] and archive.is_file() and len(result["sha256"]) == 64
    with zipfile.ZipFile(archive) as bundle: assert "TRANSMITTAL_MANIFEST.json" in bundle.namelist()
    assert json.loads((tmp_path / "delivery" / "transmittal" / "TRANSMITTAL_MANIFEST.json").read_text())["source_package"] == "ECP-000001D"
