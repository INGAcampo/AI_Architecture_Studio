import pytest
from bim_authoring.ceilings import *

@pytest.mark.parametrize("i", range(120))
def test_ceiling(i):
    ceiling = CeilingInstance(
        f"C{i}",
        CeilingType("CT","Gypsum",0.015,"gypsum"),
        ((0,0),(5,0),(5,4),(0,4)),
        2.7,
        room_id="R1",
    )
    engine = NativeBimCeilingEngine()
    assert engine.area(ceiling) == pytest.approx(20)
    assert engine.volume(ceiling) == pytest.approx(0.3)
    assert engine.validate(ceiling) == ()
