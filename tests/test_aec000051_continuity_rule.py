import json
import zipfile
from pathlib import Path
import pytest

from aias_context_engine.continuity import create_continuity_package, validate_continuity_package

ROOT = Path(__file__).resolve().parents[1]


def test_constitution_and_policy_activate_aec000051():
    constitution = (ROOT / "engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml").read_text(encoding="utf-8")
    policy = json.loads((ROOT / "engineering/aias/master/CONVERSATION_CONTINUITY_POLICY.json").read_text(encoding="utf-8"))
    assert "AEC-000051" in constitution and "VAL-CONTINUITY-000051" in constitution
    assert policy["status"] == "ACTIVE" and "checksums.sha256" in policy["minimum_contents"]


def test_handoff_package_is_complete_and_verifiable(tmp_path):
    result = create_continuity_package(ROOT / "ACKC", tmp_path / "handoff.zip")
    assert result["status"] == "READY_FOR_VERIFIED_RESUME"
    assert validate_continuity_package(tmp_path / "handoff.zip") == {"valid": True, "errors": []}
    with zipfile.ZipFile(tmp_path / "handoff.zip") as bundle:
        assert {"MASTER_CONTEXT.json", "PROJECT_STATE.json", "NEXT_TASK.yaml", "CONTINUE_PROMPT.md", "EXECUTIVE_ORDERS.md", "MANIFEST.json", "checksums.sha256"} <= set(bundle.namelist())


@pytest.mark.filterwarnings("ignore:Duplicate name:UserWarning")
def test_tampered_handoff_is_rejected(tmp_path):
    package = tmp_path / "handoff.zip"
    create_continuity_package(ROOT / "ACKC", package)
    with zipfile.ZipFile(package, "a") as bundle:
        bundle.writestr("NEXT_TASK.yaml", "tampered")
    assert not validate_continuity_package(package)["valid"]
