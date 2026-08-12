import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.normal_vector import NormalVectorEngine
    assert NormalVectorEngine().from_edge_2d((0,0),(1,0))==pytest.approx((0,1))
