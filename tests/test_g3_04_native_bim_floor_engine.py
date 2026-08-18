import pytest
from bim_authoring.floors import *

@pytest.mark.parametrize("i", range(120))
def test_floor(i):
    floor_type = FloorType("FT", "Slab", (
        FloorLayer("L1", "finish", 0.02),
        FloorLayer("L2", "concrete", 0.18),
    ))
    floor = FloorInstance(
        f"F{i}",
        floor_type,
        FloorProfile(
            ((0,0),(6,0),(6,4),(0,4)),
            (((2,1),(3,1),(3,2),(2,2)),),
        ),
        0,
    )
    engine = NativeBimFloorEngine()
    q = engine.quantities(floor)
    assert q.gross_area == pytest.approx(24)
    assert q.opening_area == pytest.approx(1)
    assert q.net_area == pytest.approx(23)
    assert q.volume == pytest.approx(4.6)
