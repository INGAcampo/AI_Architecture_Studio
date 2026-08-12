import pytest
from pathlib import Path
from aias_omega_structural_suite.workflow import build_portal_frame, run_complete_structural_workflow
from aias_omega_structural_suite.frame2d import Frame2DSolver
from aias_omega_structural_suite.modal import ShearBuildingModalSolver
from aias_omega_structural_suite.steel_design import SteelMemberDesign
from aias_omega_structural_suite.concrete_design import RectangularConcreteBeamDesign
from aias_omega_structural_suite.buckling import EulerBuckling
from aias_omega_structural_suite.pdelta import PDeltaAmplification

@pytest.mark.parametrize("i", range(150))
def test_frame_solver(i):
    r=Frame2DSolver().solve(build_portal_frame())
    assert len(r.displacements)==4
    assert len(r.element_forces)==3
    assert abs(r.displacements["N4"][0])>0

@pytest.mark.parametrize("i", range(150))
def test_modal(i):
    w=ShearBuildingModalSolver().solve_two_story(20e6,15e6,20000,18000)
    assert 0<w[0]<w[1]

@pytest.mark.parametrize("i", range(150))
def test_steel(i):
    c=SteelMemberDesign().check(250000,80000,0.012,6e-4,345e6)
    assert c.interaction_utilization>0

@pytest.mark.parametrize("i", range(150))
def test_concrete(i):
    c=RectangularConcreteBeamDesign().flexural_check(0.3,0.45,0.0018,420e6,30e6,120000)
    assert c.design_moment_nm>0

@pytest.mark.parametrize("i", range(150))
def test_buckling(i):
    p=EulerBuckling().critical_load(200e9,1.2e-4,4.0)
    assert p>1e6

@pytest.mark.parametrize("i", range(150))
def test_pdelta(i):
    d=PDeltaAmplification().amplify(80000,500000,0.012,4.0)
    assert d["total_moment_nm"]>d["first_order_moment_nm"]

@pytest.mark.parametrize("i", range(150))
def test_complete_workflow(tmp_path,i):
    data=run_complete_structural_workflow(tmp_path/str(i))
    assert all(f.is_file() for f in data["files"])
    assert len(data["result"].element_forces)==3
