import pytest
pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication
from aias_multistudio_shell.home_studio import HomeStudio
from aias_multistudio_shell.services import ShellServices
from aias_multistudio_shell.studios import StudioDescriptor

@pytest.mark.parametrize("i", range(50))
def test_home_studio_constructs(i):
    app = QApplication.instance() or QApplication([])
    descriptor = StudioDescriptor("cad", "CAD", "Design", lambda: object(), "CAD")
    home = HomeStudio((descriptor,))
    assert home is not None
