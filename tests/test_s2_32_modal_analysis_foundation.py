import pytest
from engines.structural.modal import *

@pytest.mark.parametrize("index", range(120))
def test_modal_modes(index):
    mode = ModalMode(index + 1, float((index + 1) ** 2), participation_factor=0.001 * index)
    assert mode.frequency_hz > 0
    engine = ModalAnalysisFoundation()
    assert engine.sort_modes((mode,))[0] is mode
