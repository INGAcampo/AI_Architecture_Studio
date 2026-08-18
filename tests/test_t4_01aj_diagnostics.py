import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.diagnostics import StructuralDiagnostics
    assert StructuralDiagnostics().inspect(((1,0),(0,0))).warnings
