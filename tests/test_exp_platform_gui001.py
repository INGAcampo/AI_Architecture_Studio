import json
from pathlib import Path

from gui.workspace import WorkspaceManager
from gui.workspace2 import CapabilityCenter, core_command_catalog, register_capability_center, render_capability_center

ROOT = Path(__file__).resolve().parents[1]


def test_center_derives_repository_evidence_and_never_claims_signature():
    snapshot = CapabilityCenter(ROOT).snapshot()
    assert snapshot["components"] >= 119
    assert snapshot["source_packages"] >= 134
    assert snapshot["installers"]["total"] >= 70
    assert snapshot["installers"]["integrity_invalid"] == 0
    assert snapshot["distribution"]["publisher_signed"] is False
    install = next(item for item in snapshot["actions"] if item["action_id"] == "PLAN_INSTALL")
    assert install["enabled"] is False and "publisher_signature_unverified" in install["blockers"]


def test_center_registers_single_workspace_panel(tmp_path):
    manager = WorkspaceManager(tmp_path)
    center = register_capability_center(manager, ROOT)
    register_capability_center(manager, ROOT)
    descriptor = manager.registry.get(center.PANEL_ID)
    assert descriptor.metadata["read_only_evidence"] is True
    assert len(manager.registry.all()) == 1


def test_command_catalog_exposes_capability_center_with_handler():
    called = []
    registry = core_command_catalog({"CAPABILITY-CENTER": lambda: called.append(True)})
    assert registry.resolve("CAPACIDADES").capability_id == "EXP-PLATFORM-GUI-001"
    registry.execute("PLATAFORMA")
    assert called == [True]


def test_rendered_center_is_accessible_and_truthful():
    html = render_capability_center(CapabilityCenter(ROOT).snapshot())
    assert "<title>AIAS Capability Center</title>" in html
    assert "role='status'" in html
    assert "no instala ni publica" in html


def test_checksum_traversal_fails_closed(tmp_path):
    installer = tmp_path / "AIAS_BAD_INSTALLER"; installer.mkdir()
    (installer / "manifest.json").write_text(json.dumps({"pack_id":"BAD"}), encoding="utf-8")
    (installer / "checksums.sha256").write_text("0" * 64 + "  ../outside.txt\n", encoding="utf-8")
    assert CapabilityCenter._verify_checksums(installer) == (False, 0)
