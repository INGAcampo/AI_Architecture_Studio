import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.dynamic_diagnostics import DynamicDiagnosticsEngine
    assert not DynamicDiagnosticsEngine().inspect((1,2),1,.01).warnings
