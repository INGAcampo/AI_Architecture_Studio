from dataclasses import dataclass
from analysis.contact.contact_domain import ContactPoint,ContactResult
from analysis.contact.penalty_contact import PenaltyContactEngine
from analysis.contact.coulomb_friction import CoulombFrictionEngine
from analysis.contact.contact_diagnostics import ContactDiagnosticsEngine
from analysis.contact.contact_ai_advisor import ContactAIAdvisor
from analysis.contact.contact_report import ContactReportEngine
from analysis.contact.cpu_gpu_contact_scheduler import CPUGPUContactScheduler
@dataclass(frozen=True,slots=True)
class Workflow: result:object;diagnostics:object;advice:object;backend:str;report:object
class ContactVerticalSlice:
    def run(self,gap=-1e-6,penalty=1e7,mu=.3,count=1000):
        pressure=PenaltyContactEngine().pressure(gap,penalty);state=CoulombFrictionEngine().state(.1*pressure,pressure,mu)
        p=ContactPoint("S1","M1",gap,(0,1),pressure,state);r=ContactResult((p,),True,4,max(-gap,0))
        backend=CPUGPUContactScheduler().choose(count);d=ContactDiagnosticsEngine().inspect(True,r.maximum_penetration,.01)
        return Workflow(r,d,ContactAIAdvisor().advise(d),backend,ContactReportEngine().build(r,mu,backend))
