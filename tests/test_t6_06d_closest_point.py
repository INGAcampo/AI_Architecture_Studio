import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.closest_point import ClosestPointEngine
    assert ClosestPointEngine().on_segment((2,0),(0,0),(1,0))==(1.0,0.0)
