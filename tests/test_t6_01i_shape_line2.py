import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.shape_line2 import ShapeLine2
    assert sum(ShapeLine2().evaluate(.2))==1
