"""
AI Architecture Studio
Ribbon

Foundation 4.2
"""

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Ribbon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)

        title = QLabel("Herramientas AIAS")
        title.setStyleSheet(
            "color: white; font-weight: bold;"
        )

        buttons = QHBoxLayout()

        self.new_project_btn = QPushButton("Nuevo Proyecto")
        self.open_project_btn = QPushButton("Abrir")
        self.save_project_btn = QPushButton("Guardar")

        self.line_btn = QPushButton("LINE")
        self.polyline_btn = QPushButton("PLINE")
        self.rectangle_btn = QPushButton("RECTANGLE")
        self.circle_btn = QPushButton("CIRCLE")
        self.move_btn = QPushButton("MOVE")
        self.copy_btn = QPushButton("COPY")
        self.rotate_btn = QPushButton("ROTATE")

        self.wall_btn = QPushButton("Muro")
        self.column_btn = QPushButton("Columna")
        self.beam_btn = QPushButton("Viga")

        for button in [
            self.new_project_btn,
            self.open_project_btn,
            self.save_project_btn,
            self.line_btn,
            self.polyline_btn,
            self.rectangle_btn,
            self.circle_btn,
            self.move_btn,
            self.copy_btn,
            self.rotate_btn,
            self.wall_btn,
            self.column_btn,
            self.beam_btn,
        ]:
            buttons.addWidget(button)

        layout.addWidget(title)
        layout.addLayout(buttons)

        self.setStyleSheet("""
            QWidget {
                background-color: #252525;
            }

            QPushButton {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                padding: 8px 14px;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #444444;
            }

            QPushButton:pressed {
                background-color: #555555;
            }
        """)