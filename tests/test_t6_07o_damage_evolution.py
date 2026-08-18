import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.damage_evolution import DamageEvolutionLaw
    assert DamageEvolutionLaw().exponential(.01,.001,10)>0
