"""
AI Architecture Studio
Command Line

Foundation 2.2
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit


class CommandLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)

        label = QLabel("Comando:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("Escribe LINE, WALL, COLUMN o una instrucción IA...")

        layout.addWidget(label)
        layout.addWidget(self.input)

        self.setStyleSheet("""
            QWidget {
                background-color: #202020;
            }

            QLabel {
                color: white;
            }

            QLineEdit {
                background-color: #111111;
                color: white;
                border: 1px solid #555555;
                padding: 6px;
            }
        """)