import pytest
from aias_omega_release5.workflow import solve_demo_truss
from aias_omega_release5.truss import solve_linear_system

@pytest.mark.parametrize("i", range(200))
def test_demo_truss_equilibrium(i):
    r=solve_demo_truss()
    ry=sum(v[1] for v in r.reactions.values())
    assert ry == pytest.approx(100000.0, rel=1e-8)
    assert abs(r.displacements["N3"][1])>0
    assert len(r.axial_forces)==3

@pytest.mark.parametrize("i", range(100))
def test_linear_system(i):
    x=solve_linear_system([[2,1],[1,3]],[5,6])
    assert x[0]==pytest.approx(1.8)
    assert x[1]==pytest.approx(1.4)
