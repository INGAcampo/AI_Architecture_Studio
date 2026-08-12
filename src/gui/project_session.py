"""Controlador de documentos .aias para la ventana principal."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PySide6.QtCore import QSettings, QTimer
from PySide6.QtWidgets import QFileDialog, QMessageBox

from storage.object_graph import ObjectGraphCodec
from storage.project_io import ProjectIO
from aias_i18n import get_translator


class ProjectSessionController:
    APP_TITLE = "AI Architecture Studio"

    def __init__(self, window, app_core):
        self.window = window
        self.translator = get_translator()
        self.FILTER = self.translator.translate("project.filter")
        self.app_core = app_core
        self.io = ProjectIO()
        self.codec = ObjectGraphCodec()
        self.document = self.io.new_project(self.translator.translate("document.untitled"))
        self._sync_document_manager()
        self.settings = QSettings("AIAS", "AI Architecture Studio")
        self._baseline = ""
        self._checking = False

        self.timer = QTimer(window)
        self.timer.setInterval(900)
        self.timer.timeout.connect(self.detect_changes)
        self.timer.start()

        self._baseline = self.scene_fingerprint()
        self.update_title()

    def new_project(self, name=None):
        if not self.confirm_discard_changes():
            return False
        if hasattr(self.app_core, "new_scene"):
            self.app_core.new_scene()
        self._bind_scene_to_workspace()
        self.document = self.io.new_project(name or self.translator.translate("document.untitled"))
        self._sync_document_manager()
        self._baseline = self.scene_fingerprint()
        self.document.mark_clean()
        self.window.refresh_project_tree()
        self.window.refresh_layers_panel()
        self.update_title()
        self.window.statusBar().showMessage(self.translator.translate("project.created",name=self.document.metadata.name))
        return True

    def open_dialog(self):
        if not self.confirm_discard_changes():
            return False
        path, _ = QFileDialog.getOpenFileName(
            self.window, self.translator.translate("project.open"), self.last_folder(), self.FILTER
        )
        if not path:
            return False
        return self.open_file(path)

    def open_file(self, path):
        try:
            document = self.io.open(path)
            runtime = document.custom_data.get("runtime_scene")
            if runtime is not None:
                root = self.codec.decode(runtime)
                self.app_core.scene.root = root
            self._restore_layers(document.layers)
            self._restore_camera(document.camera)
            self.document = document
            self._sync_document_manager()
            self.document.mark_clean()
            self._bind_scene_to_workspace()
            self.window.refresh_project_tree()
            self.window.refresh_layers_panel()
            self.window.clear_properties()
            self._baseline = self.scene_fingerprint()
            self.add_recent(path)
            self.update_title()
            self.window.statusBar().showMessage(self.translator.translate("project.opened",name=Path(path).name))
            return True
        except Exception as exc:
            QMessageBox.critical(self.window, self.translator.translate("project.open_failed"), str(exc))
            return False

    def save(self):
        if self.document.file_path is None:
            return self.save_as()
        return self._save_to(self.document.file_path)

    def save_as(self):
        suggested = self.document.metadata.name or "Proyecto"
        if self.document.file_path:
            suggested = str(self.document.file_path)
        else:
            suggested = str(Path(self.last_folder()) / f"{suggested}.aias")
        path, _ = QFileDialog.getSaveFileName(
            self.window, self.translator.translate("project.save"), suggested, self.FILTER
        )
        if not path:
            return False
        return self._save_to(path)

    def _save_to(self, path):
        try:
            self.capture_runtime()
            target = self.io.save(self.document, path)
            self.document.metadata.name = target.stem
            self.document.mark_clean()
            self._baseline = self.scene_fingerprint()
            self.add_recent(target)
            self.update_title()
            self.window.statusBar().showMessage(self.translator.translate("project.saved",name=target.name))
            return True
        except Exception as exc:
            QMessageBox.critical(self.window, self.translator.translate("project.save_failed"), str(exc))
            return False

    def _sync_document_manager(self):
        manager = getattr(self.app_core, "document_manager", None)
        if manager is not None:
            manager.set_document(self.document)

    def capture_runtime(self):
        self.document.custom_data["runtime_scene"] = self.codec.encode(self.app_core.scene.root)
        self.document.layers = self._capture_layers()
        self.document.camera = self._capture_camera()
        self.document.metadata.touch()

    def _capture_layers(self):
        manager = getattr(self.app_core, "layer_manager", None)
        if manager is None:
            return []
        result = []
        current = getattr(getattr(manager, "current_layer", None), "name", None)
        for layer in manager.all_layers():
            result.append({
                "name": layer.name,
                "visible": bool(getattr(layer, "visible", True)),
                "locked": bool(getattr(layer, "locked", False)),
                "color": str(getattr(layer, "color", "#FFFFFF")),
                "lineweight": float(getattr(layer, "lineweight", 0.25)),
                "current": layer.name == current,
            })
        return result

    def _restore_layers(self, layers):
        manager = getattr(self.app_core, "layer_manager", None)
        if manager is None or not layers:
            return
        for data in layers:
            name = data.get("name", "0")
            layer = manager.get_layer(name)
            if layer is None:
                try: layer = manager.create_layer(name)
                except Exception: continue
            try: manager.set_visibility(name, data.get("visible", True))
            except Exception: setattr(layer, "visible", data.get("visible", True))
            try: manager.set_locked(name, data.get("locked", False))
            except Exception: setattr(layer, "locked", data.get("locked", False))
            if data.get("current"):
                try: manager.set_current_layer(name)
                except Exception: pass

    def _capture_camera(self):
        canvas = self.window.workspace.current_canvas()
        camera = getattr(canvas, "camera", None) if canvas else None
        if camera is None:
            return {}
        data = {}
        for name in ("zoom", "rotation", "offset_x", "offset_y", "pan_x", "pan_y"):
            if hasattr(camera, name): data[name] = getattr(camera, name)
        return data

    def _restore_camera(self, data):
        canvas = self.window.workspace.current_canvas()
        camera = getattr(canvas, "camera", None) if canvas else None
        if camera is None:
            return
        for name, value in data.items():
            if hasattr(camera, name): setattr(camera, name, value)

    def _bind_scene_to_workspace(self):
        canvas = self.window.workspace.current_canvas()
        if canvas is not None:
            canvas.scene = self.app_core.scene
            canvas.update()
        self.window.connect_current_canvas()

    def scene_fingerprint(self):
        try:
            payload = self.codec.encode(self.app_core.scene.root)
            raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
            return hashlib.sha256(raw.encode("utf-8")).hexdigest()
        except Exception:
            return ""

    def detect_changes(self):
        if self._checking:
            return
        self._checking = True
        try:
            current = self.scene_fingerprint()
            dirty = bool(current and current != self._baseline)
            if dirty != self.document.dirty:
                self.document.dirty = dirty
                self.update_title()
        finally:
            self._checking = False

    def confirm_discard_changes(self):
        self.detect_changes()
        if not self.document.dirty:
            return True
        answer = QMessageBox.question(
            self.window,
            self.translator.translate("project.unsaved_title"),
            self.translator.translate("project.unsaved_question"),
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save,
        )
        if answer == QMessageBox.Cancel:
            return False
        if answer == QMessageBox.Save:
            return self.save()
        return True

    def update_title(self):
        name = self.document.metadata.name or self.translator.translate("document.untitled")
        marker = " *" if self.document.dirty else ""
        self.window.setWindowTitle(f"{self.APP_TITLE} — {name}{marker}")

    def last_folder(self):
        return self.settings.value("projects/last_folder", str(Path.home()))

    def add_recent(self, path):
        path = str(Path(path).resolve())
        recent = self.recent_projects()
        recent = [p for p in recent if p != path]
        recent.insert(0, path)
        recent = recent[:10]
        self.settings.setValue("projects/recent", recent)
        self.settings.setValue("projects/last_folder", str(Path(path).parent))
        self.window.rebuild_recent_projects_menu()

    def recent_projects(self):
        value = self.settings.value("projects/recent", [])
        if isinstance(value, str):
            return [value]
        return [str(p) for p in value if Path(str(p)).exists()]
