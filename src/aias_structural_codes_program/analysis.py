"""Whole-building analysis contract shared by internal and external CAE adapters."""
from __future__ import annotations
from dataclasses import asdict,dataclass
from .building import StructuralBuilding

@dataclass(frozen=True,slots=True)
class LoadCase:
    case_id:str;category:str;description:str;source:str

@dataclass(frozen=True,slots=True)
class AnalysisRequest:
    analysis_id:str;building:StructuralBuilding;load_cases:tuple[LoadCase,...];solver_id:str;solver_version:str;analysis_types:tuple[str,...]
    def validate(self)->list[str]:
        issues=self.building.validate();ids=[x.case_id for x in self.load_cases]
        if not self.analysis_id:issues.append("analysis_id_required")
        if not self.solver_id or not self.solver_version:issues.append("solver_identity_required")
        if len(ids)!=len(set(ids)):issues.append("duplicate_load_case")
        allowed={"STATIC_LINEAR","MODAL","RESPONSE_SPECTRUM","SECOND_ORDER","NONLINEAR"}
        if not self.analysis_types or set(self.analysis_types)-allowed:issues.append("unsupported_analysis_type")
        for case in self.load_cases:
            if case.category not in {"DEAD","LIVE","WIND","SEISMIC","SOIL","HYDRAULIC","OTHER"}:issues.append(f"{case.case_id}:unsupported_category")
            if not case.source:issues.append(f"{case.case_id}:source_required")
        return issues
    def exchange(self)->dict:
        return {"schema":"AIAS-WHOLE-BUILDING-ANALYSIS-1.0","analysis_id":self.analysis_id,"building":self.building.exchange(),"load_cases":[asdict(x) for x in self.load_cases],"solver":{"id":self.solver_id,"version":self.solver_version},"analysis_types":list(self.analysis_types),"normative_compliance_claimed":False}

@dataclass(frozen=True,slots=True)
class MemberDemand:
    member_id:str;load_case_id:str;axial_kn:float;shear_y_kn:float;shear_z_kn:float;torsion_kn_m:float;moment_y_kn_m:float;moment_z_kn_m:float

@dataclass(frozen=True,slots=True)
class AnalysisResult:
    analysis_id:str;solver_id:str;solver_version:str;status:str;demands:tuple[MemberDemand,...];warnings:tuple[str,...]=()
    def validate_against(self,request:AnalysisRequest)->list[str]:
        issues=[];members={x.member_id for x in request.building.members};cases={x.case_id for x in request.load_cases}
        if self.analysis_id!=request.analysis_id:issues.append("analysis_identity_mismatch")
        if (self.solver_id,self.solver_version)!=(request.solver_id,request.solver_version):issues.append("solver_identity_mismatch")
        if self.status not in {"COMPLETED","FAILED","PARTIAL"}:issues.append("invalid_result_status")
        for row in self.demands:
            if row.member_id not in members:issues.append(f"{row.member_id}:unknown_member")
            if row.load_case_id not in cases:issues.append(f"{row.load_case_id}:unknown_load_case")
        return issues
