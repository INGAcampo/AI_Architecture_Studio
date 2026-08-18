import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.shape_quad4 import ShapeQuad4
    assert round(sum(ShapeQuad4().evaluate(.2,.3)),8)==1
