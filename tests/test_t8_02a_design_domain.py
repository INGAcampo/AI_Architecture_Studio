import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.design_domain import DesignFactors
    assert DesignFactors().phi_flexure==0.90
