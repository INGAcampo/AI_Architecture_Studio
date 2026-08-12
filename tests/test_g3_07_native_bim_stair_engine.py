import pytest
from bim_authoring.stairs import *

@pytest.mark.parametrize("i", range(120))
def test_stair(i):
    stair = StairInstance(
        f"S{i}",
        StairType("ST","Concrete stair",0.175,0.28,1.2),
        0,
        3.0,
    )
    engine = NativeBimStairEngine()
    g = engine.generate(stair)
    assert g.riser_count == 18
    assert g.actual_riser == pytest.approx(3/18)
    assert engine.validate(stair) == ()
