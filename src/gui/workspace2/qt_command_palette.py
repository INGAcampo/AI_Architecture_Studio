"""Optional Qt projection of the Workspace 2.0 professional command catalog."""
from __future__ import annotations
from aias_i18n import get_translator

try:
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QLabel, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
except ImportError:  # pragma: no cover
    Signal = None; QLabel = QLineEdit = QListWidget = QListWidgetItem = QVBoxLayout = QWidget = None


class CommandPaletteWidget(QWidget if QWidget is not None else object):
    if Signal is not None:
        command_requested = Signal(str)

    def __init__(self, registry, status, parent=None, translator=None):
        if QWidget is None:
            raise RuntimeError("PySide6_required_for_command_palette")
        super().__init__(parent); self.registry = registry; self.status = status; self.translator = translator or get_translator()
        layout = QVBoxLayout(self); self.search_input = QLineEdit(); self.search_input.setPlaceholderText(self.translator.translate("command.search"))
        self.status_label = QLabel(); self.results = QListWidget(); layout.addWidget(self.search_input); layout.addWidget(self.status_label); layout.addWidget(self.results)
        self.search_input.textChanged.connect(self.refresh); self.results.itemActivated.connect(self._activate); self.refresh("")

    def refresh(self, text=""):
        self.results.clear()
        state = self.status.snapshot(); self.status_label.setText(self.translator.translate("status.professional",**state))
        for command in self.registry.search(text):
            item = QListWidgetItem(f"{command.title}  [{command.availability.value}]"); item.setData(256, command.command_id); item.setToolTip(command.capability_id); self.results.addItem(item)

    def _activate(self, item):
        self.command_requested.emit(item.data(256))
