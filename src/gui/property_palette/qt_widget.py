from __future__ import annotations

from typing import Any

from .controller import PropertyPaletteController
from .model import PropertyValueType

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QCheckBox,
        QComboBox,
        QDoubleSpinBox,
        QFormLayout,
        QFrame,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QScrollArea,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    Qt = None
    QCheckBox = QComboBox = QDoubleSpinBox = QFormLayout = QFrame = None
    QGroupBox = QHBoxLayout = QLabel = QLineEdit = QScrollArea = None
    QSpinBox = QVBoxLayout = QWidget = None


class QtUnavailableError(RuntimeError):
    pass


def require_qt() -> None:
    if QWidget is None:
        raise QtUnavailableError(
            "PySide6 no está disponible para PropertyPaletteWidget."
        )


class PropertyPaletteWidget(QWidget if QWidget is not None else object):
    def __init__(
        self,
        controller: PropertyPaletteController,
        parent: Any = None,
    ) -> None:
        require_qt()
        super().__init__(parent)
        self.controller = controller
        self._editors: dict[str, QWidget] = {}
        self._syncing = False

        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Buscar propiedades…")
        self.empty_label = QLabel("Seleccione un objeto BIM", self)
        self.empty_label.setAlignment(Qt.AlignCenter)

        self.content = QWidget(self)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(6, 6, 6, 6)
        self.content_layout.addStretch(1)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.content)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.search)
        layout.addWidget(self.empty_label)
        layout.addWidget(self.scroll)

        self.search.textChanged.connect(self.apply_filter)
        self.rebuild()

    def rebuild(self) -> None:
        self._syncing = True
        try:
            while self.content_layout.count():
                item = self.content_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self._editors.clear()

            entries = self.controller.model.entries()
            has_entries = bool(entries)
            self.empty_label.setVisible(not has_entries)
            self.scroll.setVisible(has_entries)

            for group in self.controller.model.groups():
                box = QGroupBox(group, self.content)
                form = QFormLayout(box)
                for entry in self.controller.model.entries_in_group(group):
                    editor = self._create_editor(entry)
                    self._editors[entry.descriptor.property_id] = editor
                    form.addRow(entry.descriptor.label, editor)
                self.content_layout.addWidget(box)

            self.content_layout.addStretch(1)
        finally:
            self._syncing = False

    def _create_editor(self, entry):
        descriptor = entry.descriptor
        kind = descriptor.value_type

        if not descriptor.editable or kind is PropertyValueType.READ_ONLY:
            label = QLabel(entry.display_value(), self.content)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            return label

        if kind is PropertyValueType.BOOLEAN:
            editor = QCheckBox(self.content)
            editor.setTristate(entry.mixed)
            if entry.mixed:
                editor.setCheckState(Qt.PartiallyChecked)
            else:
                editor.setChecked(bool(entry.value))
            editor.stateChanged.connect(
                lambda state, pid=descriptor.property_id:
                    self._commit(pid, state == Qt.Checked)
            )
            return editor

        if kind is PropertyValueType.ENUM:
            editor = QComboBox(self.content)
            editor.addItems(descriptor.enum_values)
            if not entry.mixed and entry.value in descriptor.enum_values:
                editor.setCurrentText(str(entry.value))
            editor.currentTextChanged.connect(
                lambda value, pid=descriptor.property_id:
                    self._commit(pid, value)
            )
            return editor

        if kind is PropertyValueType.INTEGER:
            editor = QSpinBox(self.content)
            editor.setRange(
                int(descriptor.minimum if descriptor.minimum is not None else -2147483648),
                int(descriptor.maximum if descriptor.maximum is not None else 2147483647),
            )
            if not entry.mixed and entry.value is not None:
                editor.setValue(int(entry.value))
            editor.valueChanged.connect(
                lambda value, pid=descriptor.property_id:
                    self._commit(pid, value)
            )
            return editor

        if kind in {
            PropertyValueType.FLOAT,
            PropertyValueType.LENGTH,
            PropertyValueType.AREA,
            PropertyValueType.VOLUME,
        }:
            editor = QDoubleSpinBox(self.content)
            editor.setDecimals(4)
            editor.setRange(
                float(descriptor.minimum if descriptor.minimum is not None else -1e12),
                float(descriptor.maximum if descriptor.maximum is not None else 1e12),
            )
            if descriptor.unit:
                editor.setSuffix(f" {descriptor.unit}")
            if not entry.mixed and entry.value is not None:
                editor.setValue(float(entry.value))
            editor.valueChanged.connect(
                lambda value, pid=descriptor.property_id:
                    self._commit(pid, value)
            )
            return editor

        editor = QLineEdit(self.content)
        editor.setPlaceholderText("<varios>" if entry.mixed else "")
        if not entry.mixed and entry.value is not None:
            editor.setText(str(entry.value))
        editor.editingFinished.connect(
            lambda pid=descriptor.property_id, control=editor:
                self._commit(pid, control.text())
        )
        return editor

    def _commit(self, property_id: str, value: Any) -> None:
        if self._syncing:
            return
        try:
            self.controller.edit_property(property_id, value)
        except (ValueError, PermissionError, RuntimeError) as exc:
            editor = self._editors.get(property_id)
            if editor is not None:
                editor.setToolTip(str(exc))
            return
        self.rebuild()
        self.apply_filter(self.search.text())

    def apply_filter(self, text: str) -> None:
        visible_ids = {
            entry.descriptor.property_id
            for entry in self.controller.model.filter(text)
        }
        for property_id, editor in self._editors.items():
            label = self._label_for_field(editor)
            visible = property_id in visible_ids
            editor.setVisible(visible)
            if label is not None:
                label.setVisible(visible)

    @staticmethod
    def _label_for_field(editor):
        parent = editor.parentWidget()
        if parent is None or parent.layout() is None:
            return None
        form = parent.layout()
        index = form.indexOf(editor)
        if index < 0:
            return None
        row, role = form.getItemPosition(index)
        item = form.itemAt(row, QFormLayout.LabelRole)
        return item.widget() if item is not None else None

    def set_selection(self, objects) -> None:
        self.controller.set_selection(objects)
        self.rebuild()

    def refresh(self) -> None:
        self.controller.refresh()
        self.rebuild()
