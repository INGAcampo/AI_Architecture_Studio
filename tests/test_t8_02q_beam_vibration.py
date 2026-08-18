import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.beam_vibration import BeamVibrationEngine
    assert BeamVibrationEngine().first_frequency_hz(100000,100)>0
