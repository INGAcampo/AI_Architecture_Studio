import pytest
from engines.civil.terrain import *

@pytest.mark.parametrize("index", range(120))
def test_terrain(index):
    points = (
        TerrainPoint("A", 0, 0, 100 + index),
        TerrainPoint("B", 10, 0, 101 + index),
        TerrainPoint("C", 0, 10, 99 + index),
    )
    model = DigitalTerrainModel(points)
    low, high = model.elevation_range()
    assert low == 99 + index
    assert high == 101 + index
    assert model.average_elevation() == pytest.approx(100 + index)
    assert model.nearest_point(0.1, 0.2).point_id == "A"
