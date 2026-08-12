from dataclasses import dataclass
from design.steel.bolt_domain import Bolt,BoltMaterial,BoltGrade,BoltGroupDemand
from design.steel.bolt_design_engine import BoltDesignEngine
from design.steel.bolt_group import BoltGroupEngine

@dataclass(frozen=True, slots=True)
class BoltConnectionWorkflowResult:
    bolt_forces:tuple
    bolt_results:tuple
    maximum_unity:float
    passed:bool
    report_markdown:str

class BoltConnectionVerticalSlice:
    def __init__(self):
        self.group=BoltGroupEngine()
        self.design=BoltDesignEngine()

    def run(self,points,total_shear_x,total_shear_y,moment,tension_per_bolt,diameter=0.022,
            plate_thickness=0.012,plate_fu=450e6,edge_distance=0.04,spacing=0.07):
        forces=self.group.distribute(points,total_shear_x,total_shear_y,moment)
        material=BoltMaterial(BoltGrade.A325,620e6,372e6)
        results=[]
        for force in forces:
            bolt=Bolt(force.bolt_id,diameter,material)
            demand=BoltGroupDemand(force.shear_x,force.shear_y,tension_per_bolt,0.0)
            results.append(self.design.design(bolt,demand,plate_thickness,plate_fu,edge_distance,spacing))
        max_unity=max((r.unity_ratio for r in results),default=0.0)
        passed=all(r.passed for r in results)
        lines=["# Bolt Connection Design Report","",f"- Bolts: {len(results)}",f"- Maximum unity: {max_unity:.4f}",f"- Status: {'PASS' if passed else 'FAIL'}",""]
        for r in results:
            lines.append(f"- {r.bolt_id}: unity={r.unity_ratio:.4f}, governing={r.governing_check}, status={'PASS' if r.passed else 'FAIL'}")
        return BoltConnectionWorkflowResult(forces,tuple(results),max_unity,passed,"\n".join(lines)+"\n")
