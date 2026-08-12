import pytest
from engines.civil.road_alignment import *

@pytest.mark.parametrize("index", range(120))
def test_alignment(index):
    alignment = RoadAlignment(
        f"A{index}",
        (
            AlignmentPoint("P1", 0, 0, 100),
            AlignmentPoint("P2", 3, 4, 101),
            AlignmentPoint("P3", 6, 8, 102),
        ),
    )
    engine = RoadAlignmentEngine()
    assert engine.segment_lengths(alignment) == (5.0, 5.0)
    assert engine.total_length(alignment) == 10.0
    assert engine.station_of_point(alignment, 2) == 10.0
