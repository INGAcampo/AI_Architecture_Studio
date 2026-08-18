import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.mode_shape import ModeShapeEngine
    assert ModeShapeEngine().normalize((2,1))==(1,.5)
