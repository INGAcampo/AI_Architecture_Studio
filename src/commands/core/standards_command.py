"""Comando STANDARDS / NORMAS 5.2.0."""

from PySide6.QtWidgets import QInputDialog, QMessageBox

from commands.base_command import BaseCommand
from core.standards.standard_manager import StandardManager
from core.standards.standard_registry import StandardRegistry


class StandardsCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "STANDARDS"

    def _window(self, canvas):
        getter = getattr(canvas, "window", None)
        return getter() if callable(getter) else None

    def begin(self, canvas):
        manager = StandardManager.instance()
        profiles = StandardRegistry.built_in_profiles()
        labels = [
            profile.name
            for profile in profiles.values()
        ]
        ids = list(profiles.keys())

        current_name = manager.active_profile.name
        current_index = (
            labels.index(current_name)
            if current_name in labels
            else 0
        )

        selected, ok = QInputDialog.getItem(
            self._window(canvas),
            "Normativa del proyecto",
            "Seleccione el perfil normativo:",
            labels,
            current_index,
            False,
        )

        if not ok:
            print("STANDARDS cancelado")
            self._finish(canvas)
            return

        profile_id = ids[labels.index(selected)]
        manager.set_profile_by_id(profile_id)

        answer = QMessageBox.question(
            self._window(canvas),
            "Normativa del proyecto",
            "¿Desea revisar o editar los campos principales "
            "del perfil seleccionado?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer == QMessageBox.Yes:
            self._edit_profile(canvas, manager)

        print(manager.report())
        self._show_status(canvas, manager)
        self._finish(canvas)

    def _edit_text(self, canvas, title, label, current):
        value, ok = QInputDialog.getText(
            self._window(canvas),
            title,
            label,
            text=str(current or ""),
        )
        if not ok:
            return current
        return value.strip()

    def _edit_profile(self, canvas, manager):
        profile = manager.active_profile

        profile.jurisdiction = self._edit_text(
            canvas,
            "Normativa",
            "Jurisdicción / autoridad competente:",
            profile.jurisdiction,
        )
        profile.structural_basis = self._edit_text(
            canvas,
            "Normativa estructural",
            "Base general de diseño:",
            profile.structural_basis,
        )
        profile.concrete_code = self._edit_text(
            canvas,
            "Normativa de concreto",
            "Código y edición:",
            profile.concrete_code,
        )
        profile.steel_code = self._edit_text(
            canvas,
            "Normativa de acero",
            "Código y edición:",
            profile.steel_code,
        )
        profile.load_code = self._edit_text(
            canvas,
            "Normativa de cargas",
            "Código y edición:",
            profile.load_code,
        )
        profile.seismic_code = self._edit_text(
            canvas,
            "Normativa sísmica",
            "Código y edición:",
            profile.seismic_code,
        )
        profile.wind_code = self._edit_text(
            canvas,
            "Normativa de viento",
            "Código y edición:",
            profile.wind_code,
        )
        profile.geotechnical_code = self._edit_text(
            canvas,
            "Normativa geotécnica",
            "Código / estudio aplicable:",
            profile.geotechnical_code,
        )
        profile.fire_code = self._edit_text(
            canvas,
            "Protección contra incendio",
            "Código y edición:",
            profile.fire_code,
        )
        profile.accessibility_code = self._edit_text(
            canvas,
            "Accesibilidad",
            "Código y edición:",
            profile.accessibility_code,
        )
        profile.quality_code = self._edit_text(
            canvas,
            "Control de calidad",
            "Norma / plan aplicable:",
            profile.quality_code,
        )
        profile.notes = self._edit_text(
            canvas,
            "Notas normativas",
            "Observaciones del proyecto:",
            profile.notes,
        )

        verified = QMessageBox.question(
            self._window(canvas),
            "Verificación profesional",
            "¿Este perfil fue revisado contra los documentos oficiales "
            "aplicables al proyecto?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        profile.verified = verified == QMessageBox.Yes
        manager.save()

    def _show_status(self, canvas, manager):
        validation = manager.validate()
        window_getter = getattr(canvas, "window", None)
        window = window_getter() if callable(window_getter) else None
        if window is not None:
            window.statusBar().showMessage(
                f"NORMAS: {manager.active_profile.name} | "
                f"{'Verificado' if manager.active_profile.verified else 'Pendiente'} | "
                f"Advertencias: {len(validation['warnings'])}"
            )

    def _finish(self, canvas):
        tool_manager = getattr(canvas, "tool_manager", None)
        cancel = getattr(tool_manager, "cancel_current", None)
        if callable(cancel):
            cancel()
