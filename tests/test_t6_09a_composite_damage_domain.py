import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.composite_damage_domain import CompositeDamageState
    assert CompositeDamageState(0,0,0,0,False).failed is False
