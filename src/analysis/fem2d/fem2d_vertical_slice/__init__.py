from dataclasses import dataclass
from analysis.fem2d.structured_quad_mesh import StructuredQuadMeshGenerator
from analysis.fem2d.adaptive_pipeline import AdaptivePipeline
from analysis.fem2d.fem2d_diagnostics import Fem2DDiagnosticsEngine
from analysis.fem2d.fem2d_report import Fem2DReportEngine
@dataclass(frozen=True,slots=True)
class Fem2DWorkflowResult: nodes:tuple; elements:tuple; adaptive:object; diagnostics:object; report:object
class Fem2DVerticalSlice:
    def run(self,w,h,nx,ny,errors,stress,q=.8):
        nodes,els=StructuredQuadMeshGenerator().generate(w,h,nx,ny); a=AdaptivePipeline().run(errors,tuple(w/max(nx,1) for _ in errors),.05); d=Fem2DDiagnosticsEngine().inspect(q,max(errors,default=0)); r=Fem2DReportEngine().build(len(nodes),len(els),stress,max(errors,default=0),not d.warnings); return Fem2DWorkflowResult(nodes,els,a,d,r)