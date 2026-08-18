import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.hpc_diagnostics import HPCDiagnosticsEngine
    assert not HPCDiagnosticsEngine().inspect(True,.8,.4).warnings
