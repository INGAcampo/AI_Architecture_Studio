import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.design_combination import DesignCombinationEngine
    assert DesignCombinationEngine().service(10,20,5)==35
