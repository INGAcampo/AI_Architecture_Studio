import pytest
pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication
from cad_professional_kernel.service import CadKernelService
from cad_viewport_pro_v2.viewport_widget import ProfessionalViewport

@pytest.mark.parametrize("i",range(40))
def test_viewport_v2_constructs(i):
    app=QApplication.instance() or QApplication([])
    viewport=ProfessionalViewport(CadKernelService())
    assert viewport.settings.minor_grid_alpha < viewport.settings.major_grid_alpha
