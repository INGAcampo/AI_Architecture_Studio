import pytest
from engines.structural.postprocessing import *

@pytest.mark.parametrize("index", range(120))
def test_postprocessor(index):
    node = DeformedNode(f"N{index}", 0, 0, 0, index*0.001, index*0.002, index*0.003)
    pos = node.deformed_position(scale=10)
    assert pos[0] == pytest.approx(index*0.01)
    processor = ReactionPostprocessor()
    assert processor.resultant(((1,2,3),(4,5,6))) == (5,7,9)
