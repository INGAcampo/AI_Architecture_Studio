import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.solid3d.soliddiagnostics import SolidDiagnosticsEngine
    assert not SolidDiagnosticsEngine().inspect(.8,.05).warnings
