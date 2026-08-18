from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class StructuralRecommendation: code:str; priority:int; object_id:str; message:str
class StructuralAIBase:
 def review_member(self,m,length,p,mat):
  r=[]; sl=length/min(p.rx,p.ry)
  if sl>200:r.append(StructuralRecommendation('high_slenderness',100,m.member_id,f'Esbeltez elevada: {sl:.1f}'))
  if mat.yield_strength<=0 and mat.compressive_strength<=0:r.append(StructuralRecommendation('missing_strength',90,m.member_id,'Material sin resistencia'))
  return tuple(sorted(r,key=lambda x:(-x.priority,x.code)))
 def rank_sections(self,candidates,demand): return tuple(i for _,i in sorted((cap-demand,i) for i,cap in candidates if cap>=demand))
