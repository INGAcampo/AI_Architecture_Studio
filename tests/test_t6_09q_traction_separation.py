import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.traction_separation import BilinearTractionSeparation
    assert BilinearTractionSeparation().traction(.015,.01,.02,10)==pytest.approx(5)
