import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.plastic_hinge import PlasticHinge
    assert PlasticHinge().rotation_state(.02,.01,.04)=='plastic'
