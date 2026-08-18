import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.compression_torsional_buckling import TorsionalBucklingEngine
    assert TorsionalBucklingEngine().critical_stress_mpa(200000,77000,1e11,1e5,1e8,1e7,3000)>0
