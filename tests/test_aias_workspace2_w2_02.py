import json

import pytest

from gui.workspace import DockArea, PanelDescriptor, WorkspaceManager
from gui.workspace2 import SessionIntegrityError, Workspace2SessionAuthority


def authority(tmp_path, events=None):
    return Workspace2SessionAuthority(WorkspaceManager(tmp_path / "layouts", event_dispatcher=events))


def test_complete_session_round_trip(tmp_path):
    events = []
    session = authority(tmp_path, events.append)
    session.workspace.register_panel(PanelDescriptor("project", "Project", DockArea.LEFT))
    session.workspace.panels.activate("project")
    first = session.open_document("model/building.aias")
    session.open_document(title="Calculation")
    session.workspace.activate_document(first.document_id)
    session.workspace.set_selection(["column-01"])
    session.switch_profile("Structure")
    session.shell.set_theme("light")
    path = session.save_recovery(tmp_path / "recovery.aias-session.json")

    restored = authority(tmp_path)
    restored.restore_recovery(path)
    assert restored.shell.profile.name == "Structure"
    assert restored.shell.theme == "light"
    assert restored.active_document.document_id == first.document_id
    assert restored.workspace.state.selection_ids == ("column-01",)
    assert restored.workspace.panels.require("project").area == DockArea.LEFT
    assert events[-1].name == "workspace2.session.saved"


def test_tampered_session_fails_without_mutating_active_state(tmp_path):
    session = authority(tmp_path)
    session.open_document(title="Original")
    path = session.save_recovery(tmp_path / "recovery.json")
    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["payload"]["shell"]["jurisdiction"] = "ALTERED"
    path.write_text(json.dumps(envelope), encoding="utf-8")
    before = session.snapshot()
    with pytest.raises(SessionIntegrityError, match="checksum"):
        session.restore_recovery(path)
    assert session.snapshot() == before


def test_unknown_profile_rejected_transactionally(tmp_path):
    session = authority(tmp_path)
    path = session.save_recovery(tmp_path / "recovery.json")
    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["payload"]["shell"]["profile"] = "Unknown"
    import hashlib
    from gui.workspace2.orchestration import _canonical
    envelope["sha256"] = hashlib.sha256(_canonical(envelope["payload"])).hexdigest()
    path.write_text(json.dumps(envelope), encoding="utf-8")
    with pytest.raises(SessionIntegrityError, match="invalid_session_state"):
        session.restore_recovery(path)


def test_unsaved_document_guard_is_preserved(tmp_path):
    session = authority(tmp_path)
    document = session.open_document(title="Modified")
    document.mark_modified()
    with pytest.raises(RuntimeError, match="sin guardar"):
        session.close_document(document.document_id)
