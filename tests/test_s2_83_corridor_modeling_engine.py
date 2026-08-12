import pytest
from engines.civil.corridor import *

@pytest.mark.parametrize("index", range(120))
def test_corridor(index):
    model = CorridorModel(
        f"C{index}",
        (
            CorridorSection(0, 3.5, 3.5, 100),
            CorridorSection(100, 4.0, 4.0, 102),
        ),
    )
    assert model.width_at(10) == 7.0
    assert model.elevation_range() == (100, 102)
