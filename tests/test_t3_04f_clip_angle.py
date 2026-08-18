import pytest
from design.steel.clip_angle import *
@pytest.mark.parametrize("i",range(120))
def test_clip(i):
    assert ClipAngleEngine().design(10,20,30,60,40,80).unity_ratio==pytest.approx(.5)
