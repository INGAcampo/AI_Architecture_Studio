from dataclasses import dataclass
from design.steel.domain import SteelBeam,SteelMemberDemand
from design.steel.plugin import SteelPlatformPlugin
@dataclass(frozen=True,slots=True)
class SteelBeamWorkflowResult: member:object;design_result:object;optimization_result:object;report:object;advice:object
class SteelBeamVerticalSlice:
 def __init__(self,c): self.c=c;SteelPlatformPlugin().activate(c)
 def run(self,member_id,profile_id,material_id,length,unbraced_length,axial=0.,shear=0.,moment=0.,target=.95):
  s=self.c.services;pr=s.resolve('steel.profiles');mr=s.resolve('steel.materials');p=pr.get(profile_id);m=mr.get(material_id);b=SteelBeam(member_id,profile_id,material_id,length,unbraced_length,SteelMemberDemand(axial,shear,moment));r=s.resolve('steel.design').design(b,p,m);o=s.resolve('steel.optimizer').optimize(b,p,m,pr.all(),target);rep=s.resolve('steel.reports').build(b,p,m,r,o);adv=s.resolve('steel.ai').explain_design(r);return SteelBeamWorkflowResult(b,r,o,rep,adv)
