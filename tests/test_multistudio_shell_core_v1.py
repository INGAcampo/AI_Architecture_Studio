import pytest
from pathlib import Path
from aias_multistudio_shell.documents import DocumentManager, StudioDocument
from aias_multistudio_shell.events import EventBus, StudioEvent
from aias_multistudio_shell.project_model import AiasProject
from aias_multistudio_shell.services import ShellServices
from aias_multistudio_shell.studios import StudioDescriptor, StudioRegistry
from aias_multistudio_shell.workspace_state import WorkspaceState, WorkspaceStateStore

@pytest.mark.parametrize("i", range(100))
def test_event_bus(i):
    bus = EventBus()
    received = []
    bus.subscribe("x", lambda event: received.append(event.payload["value"]))
    bus.publish(StudioEvent("x", {"value": i}))
    assert received == [i]

@pytest.mark.parametrize("i", range(100))
def test_document_manager(i):
    manager = DocumentManager()
    document = StudioDocument(f"Doc {i}", "cad")
    manager.add(document)
    assert manager.active() is document
    assert manager.close(document.document_id) is document

@pytest.mark.parametrize("i", range(100))
def test_studio_registry(i):
    registry = StudioRegistry()
    registry.register(StudioDescriptor(f"s{i}", f"Studio {i}", "Test", lambda: object()))
    assert registry.get(f"s{i}").name == f"Studio {i}"

@pytest.mark.parametrize("i", range(100))
def test_project_model(i):
    project = AiasProject(f"Project {i}")
    group = project.add_group("Models", "group")
    assert group in project.root_node.children

@pytest.mark.parametrize("i", range(100))
def test_workspace_state(tmp_path, i):
    store = WorkspaceStateStore(tmp_path / f"state_{i}.json")
    state = WorkspaceState(active_studio="cad", open_documents=[{"title": "A"}], geometry=b"abc")
    store.save(state)
    restored = store.load()
    assert restored.active_studio == "cad"
    assert restored.geometry == b"abc"

@pytest.mark.parametrize("i", range(100))
def test_services_default(i):
    services = ShellServices.create_default()
    assert services.project.name == "Untitled Project"
    assert services.documents.active() is None
