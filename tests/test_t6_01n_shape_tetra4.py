import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.shape_tetra4 import ShapeTetra4
    assert sum(ShapeTetra4().evaluate(.1,.2,.3))==1
