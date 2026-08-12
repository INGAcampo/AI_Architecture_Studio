"""Public module supporting the coordinated multi-studio desktop shell."""
from PySide6.QtWidgets import QPlainTextEdit

class OutputConsole(QPlainTextEdit):
    """Execute the public OutputConsole operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setReadOnly(True)

    def write_message(self, message: str) -> None:
        """Persist message for the coordinated multi-studio desktop shell in its stable external representation."""
        self.appendPlainText(message)
