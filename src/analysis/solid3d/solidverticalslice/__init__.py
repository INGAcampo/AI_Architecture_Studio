from dataclasses import dataclass
from analysis.solid3d.volumetricmesh import VolumetricMeshEngine
from analysis.solid3d.tetra4 import Tetra4Engine
from analysis.solid3d.vonmises3d import VonMises3DEngine
from analysis.solid3d.soliddiagnostics import SolidDiagnosticsEngine
from analysis.solid3d.solidadvisor import SolidAIAdvisor
from analysis.solid3d.solidreport import SolidReportEngine
@dataclass(frozen=True,slots=True)
class Workflow: nodes:tuple;elements:tuple;volume:float;maximum_von_mises:float;diagnostics:object;advice:object;report:object
class SolidVerticalSlice:
    def run(self):
        n,e=VolumetricMeshEngine().unit_tetra();v=Tetra4Engine().volume(tuple(x.coordinates for x in n))
        vm=VonMises3DEngine().calculate(100,40,20,5,3,2);d=SolidDiagnosticsEngine().inspect(.85,.04)
        return Workflow(n,e,v,vm,d,SolidAIAdvisor().advise(d),SolidReportEngine().build(len(n),len(e),vm))
