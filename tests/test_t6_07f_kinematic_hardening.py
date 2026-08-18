import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.kinematic_hardening import KinematicHardeningLaw
    assert KinematicHardeningLaw().update_backstress((0,0),(1,2),3)==(3,6)
