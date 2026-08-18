import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.compression_euler import EulerBucklingEngine
    assert EulerBucklingEngine().critical_load_n(200000,1e8,1,3000)>0
