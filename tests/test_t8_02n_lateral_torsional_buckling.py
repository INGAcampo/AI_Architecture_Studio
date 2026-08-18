import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.lateral_torsional_buckling import LateralTorsionalBucklingEngine
    assert LateralTorsionalBucklingEngine().nominal_moment_nmm(100,2,1,3,60)==80
