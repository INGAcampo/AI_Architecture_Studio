import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.transient_diagnostics import TransientDiagnosticsEngine
    assert not TransientDiagnosticsEngine().inspect(True,.01,True).warnings
