"""Focused regression for L3-PRODUCTION-BIM-003D."""
from pathlib import Path

from aias_foundation_delivery.models import IssueStatus
from aias_l3_production_bim.native_coordination import NativeCoordinationBridge
from aias_l3_production_bim.coordinated_project_service import (
    CoordinatedProductionProjectService,
)


def _discovery() -> Path:
    return Path("AIAS_L3_PRODUCTION_BIM_DISCOVERY_CURRENT") / "DISCOVERY.json"


def test_003d_issue_register_exact_contract():
    bridge = NativeCoordinationBridge()

    issue = bridge.add_issue(
        issue_id="ISS-001",
        title="Coordination opening",
        description="Review opening location",
        owner="Architecture",
    )
    assert issue.issue_id == "ISS-001"
    assert issue.status == IssueStatus.OPEN

    bridge.resolve_issue("ISS-001", "Coordinated")
    assert issue.resolution == "Coordinated"


def test_003d_authorities_are_exact_repository_implementations():
    bridge = NativeCoordinationBridge()

    assert bridge.collaboration.__class__.__name__ == "BimCollaborationManager"
    assert bridge.clashes.__class__.__name__ == "ClashDetector"
    assert bridge.validation.__class__.__name__ == "CodeCheckValidator"
    assert bridge.quality.__class__.__name__ == "QualityGateEngine"
    assert bridge.issues.__class__.__name__ == "IssueRegister"
    assert bridge.versions.__class__.__name__ == "VersionStore"
    assert bridge.boq.__class__.__name__ == "BoqEngine"
    assert bridge.ifc.__class__.__name__ == "NeutralIfcSynchronizer"


def test_003d_workspace_projection_exposes_coordination_layer():
    service = CoordinatedProductionProjectService(
        "003D Test",
        discovery_path=_discovery(),
    )
    service.start()

    service.coordination.add_issue(
        issue_id="ISS-001",
        title="Coordination issue",
        description="Review discipline interface",
        owner="BIM",
    )

    projection = service.workspace_projection_with_coordination()
    coordination = projection["multidisciplinary_coordination"]

    assert coordination["issues"] == 1
    assert coordination["clash_runs"] == 0
    assert coordination["ifc_runs"] == 0
