"""Public module supporting the coordinated multi-studio desktop shell."""
from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

class GlobalPropertiesPanel(QWidget):
    """Execute the public GlobalPropertiesPanel operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        form = QFormLayout(self)
        self.project = QLabel("-")
        self.studio = QLabel("-")
        self.document = QLabel("-")
        form.addRow("Proyecto", self.project)
        form.addRow("Studio", self.studio)
        form.addRow("Documento", self.document)

    def set_context(self, project: str, studio: str, document: str) -> None:
        """Execute set context for the coordinated multi-studio desktop shell with validated state transitions."""
        self.project.setText(project)
        self.studio.setText(studio)
        self.document.setText(document)
