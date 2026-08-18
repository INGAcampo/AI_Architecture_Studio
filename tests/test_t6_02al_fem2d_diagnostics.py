import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem2d.fem2d_diagnostics import Fem2DDiagnosticsEngine
    assert not Fem2DDiagnosticsEngine().inspect(.8,.05).warnings
