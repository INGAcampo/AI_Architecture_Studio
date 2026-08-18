"""Portal-frame fixture and end-to-end structural analysis/design workflow."""
from pathlib import Path
from .model import *
from .frame2d import Frame2DSolver
from .reports import StructuralReport
from .steel_design import SteelMemberDesign
from .concrete_design import RectangularConcreteBeamDesign
from .modal import ShearBuildingModalSolver
from .pdelta import PDeltaAmplification
from .buckling import EulerBuckling

def build_portal_frame():
    """Construct the canonical restrained single-bay portal-frame model."""
    m = StructuralModel2D()
    m.nodes = {
        "N1": Node2D("N1",0,0,True,True,True),
        "N2": Node2D("N2",6,0,True,True,True),
        "N3": Node2D("N3",0,4),
        "N4": Node2D("N4",6,4),
    }
    m.materials["STEEL"] = Material("STEEL",200e9,345e6,7850)
    m.sections["W"] = Section("W",0.012,1.2e-4,0.4)
    m.elements = {
        "C1": FrameElement2D("C1","N1","N3","STEEL","W"),
        "B1": FrameElement2D("B1","N3","N4","STEEL","W"),
        "C2": FrameElement2D("C2","N2","N4","STEEL","W"),
    }
    m.loads = [NodalLoad2D("N3",0,-50000,0), NodalLoad2D("N4",30000,-50000,0)]
    return m

def run_complete_structural_workflow(output_dir: Path):
    """Analyze, check, report and package the reference structural project."""
    output_dir.mkdir(parents=True, exist_ok=True)
    model = build_portal_frame()
    result = Frame2DSolver().solve(model)
    steel = SteelMemberDesign().check(250000,80000,0.012,6e-4,345e6)
    concrete = RectangularConcreteBeamDesign().flexural_check(0.3,0.45,0.0018,420e6,30e6,120000)
    modal = ShearBuildingModalSolver().solve_two_story(20e6,15e6,20000,18000)
    pdelta = PDeltaAmplification().amplify(80000,500000,0.012,4.0)
    buckling = EulerBuckling().critical_load(200e9,1.2e-4,4.0,1.0)
    report = StructuralReport()
    report.export_json(result, output_dir/"structural_result.json")
    report.export_markdown(result, output_dir/"structural_report.md")
    return {
        "result": result,
        "steel": steel,
        "concrete": concrete,
        "modal_rad_s": modal,
        "pdelta": pdelta,
        "buckling_n": buckling,
        "files": [output_dir/"structural_result.json", output_dir/"structural_report.md"],
    }
