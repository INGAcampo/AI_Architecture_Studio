import pytest
from design.steel.beam_splice import *
@pytest.mark.parametrize("i",range(120))
def test_beam_splice(i):
    assert BeamSpliceEngine().design(80e3,.6,200e3,40e3,100e3).passed
