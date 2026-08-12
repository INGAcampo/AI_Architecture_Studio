"""Public module supporting the coordinated multi-studio desktop shell."""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame, QGridLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget
)

class StudioCard(QFrame):
    """Execute the public StudioCard operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    activated = Signal(str)

    def __init__(self, studio_id: str, name: str, description: str, parent=None) -> None:
        super().__init__(parent)
        self.studio_id = studio_id
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(230, 140)
        layout = QVBoxLayout(self)
        title = QLabel(name)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        text = QLabel(description)
        text.setWordWrap(True)
        text.setStyleSheet("color: #9da7b3;")
        button = QPushButton("Abrir Studio")
        button.clicked.connect(lambda: self.activated.emit(self.studio_id))
        layout.addWidget(title)
        layout.addWidget(text, 1)
        layout.addWidget(button)

class HomeStudio(QWidget):
    """Execute the public HomeStudio operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    studioRequested = Signal(str)

    def __init__(self, descriptors, parent=None) -> None:
        super().__init__(parent)
        outer = QVBoxLayout(self)
        heading = QLabel("AI Architecture Studio — Plataforma Multi‑Studio")
        heading.setStyleSheet("font-size: 26px; font-weight: 600;")
        outer.addWidget(heading)
        sub = QLabel("Un proyecto, múltiples disciplinas, un modelo coordinado.")
        sub.setStyleSheet("font-size: 14px; color: #9da7b3;")
        outer.addWidget(sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        for i, descriptor in enumerate(descriptors):
            card = StudioCard(
                descriptor.studio_id,
                descriptor.name,
                descriptor.description,
            )
            card.activated.connect(self.studioRequested)
            grid.addWidget(card, i // 3, i % 3)
        scroll.setWidget(container)
        outer.addWidget(scroll, 1)
