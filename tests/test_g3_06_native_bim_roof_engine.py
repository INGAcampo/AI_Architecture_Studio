import pytest
from bim_authoring.roofs import *

@pytest.mark.parametrize("i", range(120))
def test_roof(i):
    roof = RoofInstance(
        f"R{i}",
        RoofType("RT","Metal roof",0.12,"metal"),
        60,
        30,
        3.0,
    )
    q = NativeBimRoofEngine().quantities(roof)
    assert q.footprint_area == 60
    assert q.surface_area > 60
    assert q.volume > 0
