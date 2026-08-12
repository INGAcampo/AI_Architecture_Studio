import pytest
pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication
from aias_program_s1_cad.workspace import CadProgramS1Window

@pytest.mark.parametrize("i",range(50))
def test_program_s1_window_constructs(i):
    app=QApplication.instance() or QApplication([])
    window=CadProgramS1Window()
    assert window.service is not None
    assert len(window.service.entities)>=2
