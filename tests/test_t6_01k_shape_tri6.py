import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.shape_tri6 import ShapeTri6
    assert round(sum(ShapeTri6().evaluate(.2,.3)),8)==1
