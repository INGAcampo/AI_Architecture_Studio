import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.shape_hexa8 import ShapeHexa8
    assert round(sum(ShapeHexa8().evaluate(.1,.2,.3)),8)==1
