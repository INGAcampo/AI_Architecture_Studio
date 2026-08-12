"""Public module supporting the coordinated multi-studio desktop shell."""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from cad_professional_kernel.service import CadKernelService
from cad_drawing_engine_v3.controller import DrawingController
from cad_drawing_engine_v3.viewport_v3 import DrawingViewport

class CadStudio(QWidget):
    """Execute the public CadStudio operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.kernel = CadKernelService()
        self.controller = DrawingController(self.kernel)
        self.viewport = DrawingViewport(self.kernel, self.controller)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.viewport)
