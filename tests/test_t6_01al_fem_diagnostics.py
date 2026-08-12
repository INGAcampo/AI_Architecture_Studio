import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_diagnostics import FemDiagnostics
    assert not FemDiagnostics().inspect(((1,0),(0,1)),.8).warnings
