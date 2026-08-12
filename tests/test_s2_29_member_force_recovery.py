import pytest
from engines.structural.force_recovery import *

@pytest.mark.parametrize("index", range(120))
def test_force_recovery(index):
    recovery = MemberForceRecovery()
    k = index + 1
    start, end = recovery.recover_axial(k, 0.0, 1.0)
    item = MemberEndForces(f"M{index}", start, index, index*2, end, -index, -index*2)
    env = recovery.envelope((item,))
    assert start == -k and end == k
    assert env["axial_max"] == k
