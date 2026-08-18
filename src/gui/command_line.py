"""
AI Architecture Studio
Command Line

Dynamic Input v1
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QWidget,
)


class CommandInput(QLineEdit):

    escape_pressed = Signal()
    history_previous = Signal()
    history_next = Signal()
    tab_pressed = Signal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.escape_pressed.emit()
            return

        if event.key() == Qt.Key_Up:
            self.history_previous.emit()
            return

        if event.key() == Qt.Key_Down:
            self.history_next.emit()
            return
        
        if event.key() == Qt.Key_Tab:
            self.tab_pressed.emit()
            return

        super().keyPressEvent(event)


class CommandLine(QWidget):

    command_submitted = Signal(str)
    escape_requested = Signal()
    tab_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.history = []
        self.history_index = 0

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)

        self.prompt_label = QLabel("Comando:")
        self.input = CommandInput()

        self.input.setPlaceholderText(
            "LINE, 10,5, @10,0, @5<45 o distancia"
        )

        layout.addWidget(self.prompt_label)
        layout.addWidget(self.input)

        self.input.returnPressed.connect(
            self._submit
        )

        self.input.escape_pressed.connect(
            self._request_escape
        )

        self.input.history_previous.connect(
            self._show_previous_history
        )

        self.input.history_next.connect(
            self._show_next_history
        )

        self.input.tab_pressed.connect(
            self.tab_requested.emit
    )

        # Styling is inherited from the governed AIAS semantic QSS.

    def set_prompt(self, text):
        prompt = str(text).strip()

        if not prompt:
            prompt = "Comando:"

        self.prompt_label.setText(prompt)

    def reset_prompt(self):
        self.set_prompt("Comando:")

    def _submit(self):
        text = self.input.text().strip()

        if not text:
            return

        self._add_to_history(text)
        self.input.clear()

        self.command_submitted.emit(text)

    def _request_escape(self):
        self.input.clear()
        self.escape_requested.emit()

    def clear_input(self):
        self.input.clear()

    def set_input_text(self, text):
        self.input.setText(str(text))
        self.input.setCursorPosition(
            len(self.input.text())
        )

    def focus_input(self):
        self.input.setFocus()
        self.input.selectAll()

    def _add_to_history(self, text):
        if self.history and self.history[-1] == text:
            self.history_index = len(self.history)
            return

        self.history.append(text)
        self.history_index = len(self.history)

    def _show_previous_history(self):
        if not self.history:
            return

        self.history_index = max(
            0,
            self.history_index - 1,
        )

        self.set_input_text(
            self.history[self.history_index]
        )

    def _show_next_history(self):
        if not self.history:
            return

        self.history_index = min(
            len(self.history),
            self.history_index + 1,
        )

        if self.history_index >= len(self.history):
            self.input.clear()
            return

        self.set_input_text(
            self.history[self.history_index]
        )
