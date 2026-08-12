import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.rc_diagnostics import RCDiagnosticsEngine
    assert not RCDiagnosticsEngine().inspect(.8,True,True).warnings
