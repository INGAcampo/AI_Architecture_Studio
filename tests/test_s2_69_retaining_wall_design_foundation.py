import pytest
from engines.structural.retaining_walls import *

@pytest.mark.parametrize("index", range(120))
def test_retaining_wall(index):
    case = RetainingWallCase(f"C{index}", 200 + index, 100, 150 + index, 75)
    engine = RetainingWallDesignEngine()
    assert engine.overturning_fs(case) > 1
    assert engine.sliding_fs(case) > 1
