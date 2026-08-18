import pytest
pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication
from cad_professional_kernel.service import CadKernelService
from cad_viewport_pro.viewport import CadViewport

@pytest.mark.parametrize("i",range(50))
def test_viewport_constructs(i):
    app=QApplication.instance() or QApplication([])
    viewport=CadViewport(CadKernelService())
    assert viewport.camera.zoom>0
