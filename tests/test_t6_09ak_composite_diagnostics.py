import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.composite_diagnostics import CompositeDiagnosticsEngine
    assert not CompositeDiagnosticsEngine().inspect(True,.2,.5).warnings
