import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_diagnostics import GPUDiagnosticsEngine
    assert not GPUDiagnosticsEngine().inspect(True,.5,True).warnings
