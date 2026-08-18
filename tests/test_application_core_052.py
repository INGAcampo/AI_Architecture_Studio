from core.application import ApplicationCore
from core.document_manager import DocumentManager


class DummyDocument:
    def __init__(self):
        self.file_path = None
        self.dirty = False

    def mark_dirty(self):
        self.dirty = True

    def mark_clean(self):
        self.dirty = False


def test_application_core_registers_singletons():
    app = ApplicationCore()
    services = app.kernel.services
    assert services.get("application_core") is app
    assert services.get("scene_manager") is app.scene
    assert services.get("history_manager") is app.history
    assert services.get("document_manager") is app.document_manager
    assert services.get("settings_manager") is app.settings_manager


def test_new_scene_replaces_scene_and_history():
    app = ApplicationCore()
    old_scene = app.scene
    old_history = app.history
    app.new_scene()
    assert app.scene is not old_scene
    assert app.history is not old_history
    assert app.kernel.services.get("scene_manager") is app.scene
    assert app.kernel.services.get("history_manager") is app.history


def test_document_manager_tracks_dirty_state():
    manager = DocumentManager()
    document = DummyDocument()
    manager.set_document(document)
    assert manager.has_document
    manager.mark_dirty()
    assert manager.is_dirty
    manager.mark_clean()
    assert not manager.is_dirty
