import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.shape_quad8 import ShapeQuad8
    assert round(sum(ShapeQuad8().evaluate(.2,.3)),8)==1
