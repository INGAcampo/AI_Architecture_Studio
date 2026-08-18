import pytest
pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication
from cad_professional_kernel.service import CadKernelService
from cad_drawing_engine_v3.controller import DrawingController
from cad_drawing_engine_v3.viewport_v3 import DrawingViewport

@pytest.mark.parametrize("i",range(50))
def test_v3_viewport_constructs(i):
    app=QApplication.instance() or QApplication([])
    k=CadKernelService(); v=DrawingViewport(k,DrawingController(k))
    assert v.controller is not None
