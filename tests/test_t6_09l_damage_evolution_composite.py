import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.damage_evolution_composite import CompositeDamageEvolution
    assert CompositeDamageEvolution().linear(.5,.2,.8)==pytest.approx(.5)
