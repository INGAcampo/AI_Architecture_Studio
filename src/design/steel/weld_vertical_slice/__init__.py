from dataclasses import dataclass
from design.steel.weld_domain import WeldDemand
from design.steel.weld_group import WeldGroupEngine
from design.steel.weld_design_engine import WeldDesignEngine
from design.steel.weld_optimizer import WeldOptimizer
from design.steel.weld_report_ai import WeldReportAI
@dataclass(frozen=True,slots=True)
class WeldConnectionWorkflowResult:
    group_properties:object; group_forces:tuple; design_results:tuple; optimizations:tuple; maximum_unity:float; passed:bool; advice:object; report:object
class WeldConnectionVerticalSlice:
    def run(self,segs,fx,fy,m,tension=0):
        props,forces=WeldGroupEngine().distribute(segs,fx,fy,m); by={s.segment_id:s for s in segs}; eng=WeldDesignEngine(); opt=WeldOptimizer(eng)
        rs=[]; os=[]
        for f in forces:
            d=WeldDemand(f.force_x,f.force_y,tension/len(segs),0); rs.append(eng.design(by[f.segment_id],d)); os.append(opt.optimize(by[f.segment_id],d))
        ai=WeldReportAI(); mx=max(r.unity_ratio for r in rs); ok=all(r.passed for r in rs)
        return WeldConnectionWorkflowResult(props,forces,tuple(rs),tuple(os),mx,ok,ai.advise(tuple(rs),tuple(os)),ai.build(tuple(rs),tuple(os)))
