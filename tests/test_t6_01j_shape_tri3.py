import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.shape_tri3 import ShapeTri3
    assert sum(ShapeTri3().evaluate(.2,.3))==1
