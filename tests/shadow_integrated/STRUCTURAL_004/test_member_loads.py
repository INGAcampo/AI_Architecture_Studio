import math

from structural_platform_frame_ext.member_loads import (
    UniformMemberLoad,
    fixed_end_forces_local,
    recover_local_end_forces,
)


def test_fixed_end_forces_match_closed_form():
    w=10000.0
    l=6.0
    f=fixed_end_forces_local(UniformMemberLoad(w),l)

    assert math.isclose(f[1],-w*l/2.0,rel_tol=1e-12)
    assert math.isclose(f[2],-w*l*l/12.0,rel_tol=1e-12)
    assert math.isclose(f[4],-w*l/2.0,rel_tol=1e-12)
    assert math.isclose(f[5],w*l*l/12.0,rel_tol=1e-12)


def test_fixed_fixed_zero_displacement_recovers_fixed_end_forces():
    k=[[0.0]*6 for _ in range(6)]
    f=fixed_end_forces_local(UniformMemberLoad(5000.0),4.0)
    out=recover_local_end_forces(k,(0.0,)*6,f)
    assert out==f


def test_invalid_member_length_fails_closed():
    failed=False
    try:
        fixed_end_forces_local(UniformMemberLoad(1000.0),0.0)
    except ValueError:
        failed=True
    assert failed is True
