import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.material_diagnostics import MaterialDiagnosticsEngine
    assert not MaterialDiagnosticsEngine().inspect(True,.1,.01).warnings
