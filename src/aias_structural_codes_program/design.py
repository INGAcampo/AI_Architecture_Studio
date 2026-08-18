"""Batch beam and column design over whole-building analysis demands."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from .analysis import AnalysisRequest,AnalysisResult

@dataclass(frozen=True,slots=True)
class SectionCapacity:
    section_id:str;member_kind:str;axial_kn:float;shear_kn:float;moment_kn_m:float;weight_kg_m:float

@dataclass(frozen=True,slots=True)
class DesignRulePack:
    pack_id:str;version:str;legal_status:str;jurisdiction:str;capacities:tuple[SectionCapacity,...];source:str
    def validate(self)->list[str]:
        issues=[];keys=[]
        if not all((self.pack_id,self.version,self.legal_status,self.jurisdiction,self.source)):issues.append("rule_pack_identity_incomplete")
        for c in self.capacities:
            keys.append((c.member_kind,c.section_id))
            if c.member_kind not in {"BEAM","COLUMN"}:issues.append(f"{c.section_id}:unsupported_member_kind")
            if not all(isfinite(x) and x>0 for x in (c.axial_kn,c.shear_kn,c.moment_kn_m,c.weight_kg_m)):issues.append(f"{c.section_id}:invalid_capacity")
        if len(keys)!=len(set(keys)):issues.append("duplicate_capacity")
        return issues

@dataclass(frozen=True,slots=True)
class MemberDesign:
    member_id:str;member_kind:str;selected_section_id:str|None;axial_ratio:float;shear_ratio:float;moment_ratio:float;governing_ratio:float;status:str;rule_pack_id:str

@dataclass(frozen=True,slots=True)
class BatchDesignResult:
    analysis_id:str;rule_pack_id:str;rule_pack_version:str;legal_status:str;designs:tuple[MemberDesign,...];issues:tuple[str,...];professional_review_required:bool=True;construction_approved:bool=False

class BatchMemberDesigner:
    """Select the lightest adequate reference capacity for every beam and column."""
    def design(self,request:AnalysisRequest,result:AnalysisResult,pack:DesignRulePack)->BatchDesignResult:
        issues=request.validate()+result.validate_against(request)+pack.validate()
        if result.status!="COMPLETED":issues.append("analysis_not_completed")
        if issues:return BatchDesignResult(request.analysis_id,pack.pack_id,pack.version,pack.legal_status,(),tuple(sorted(set(issues))))
        output=[]
        for member in request.building.members:
            if member.kind not in {"BEAM","COLUMN"}:continue
            rows=[x for x in result.demands if x.member_id==member.member_id]
            if not rows:
                output.append(MemberDesign(member.member_id,member.kind,None,0,0,0,float("inf"),"NO_DEMAND",pack.pack_id));continue
            axial=max(abs(x.axial_kn) for x in rows);shear=max(max(abs(x.shear_y_kn),abs(x.shear_z_kn)) for x in rows);moment=max(max(abs(x.moment_y_kn_m),abs(x.moment_z_kn_m)) for x in rows)
            candidates=[]
            for cap in pack.capacities:
                if cap.member_kind!=member.kind:continue
                ratios=(axial/cap.axial_kn,shear/cap.shear_kn,moment/cap.moment_kn_m);candidates.append((max(ratios),cap.weight_kg_m,cap,ratios))
            adequate=sorted((x for x in candidates if x[0]<=1),key=lambda x:(x[1],x[0],x[2].section_id))
            chosen=adequate[0] if adequate else (max(candidates,key=lambda x:x[0]) if candidates else None)
            if chosen is None:output.append(MemberDesign(member.member_id,member.kind,None,0,0,0,float("inf"),"NO_CAPACITY",pack.pack_id));continue
            ratio,_,cap,ratios=chosen;output.append(MemberDesign(member.member_id,member.kind,cap.section_id,*ratios,ratio,"PASS_REFERENCE" if ratio<=1 else "FAIL_REFERENCE",pack.pack_id))
        return BatchDesignResult(request.analysis_id,pack.pack_id,pack.version,pack.legal_status,tuple(output),(),professional_review_required=True,construction_approved=False)
