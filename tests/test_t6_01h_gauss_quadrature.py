import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.gauss_quadrature import GaussQuadrature
    assert sum(w for _,w in GaussQuadrature().line2())==2
