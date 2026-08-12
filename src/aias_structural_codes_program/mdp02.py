"""MDP-02 traceable reference calculations for ground and water engineering."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math


@dataclass(frozen=True,slots=True)
class StudySource:
    source_id:str;source_type:str;organization:str;locator:str;status:str
    def validate(self)->list[str]:
        issues=[]
        if not all((self.source_id,self.source_type,self.organization,self.locator)):issues.append(f"{self.source_id}:source_incomplete")
        if self.status not in {"REFERENCE","AUTHORIZED","DRAFT"}:issues.append(f"{self.source_id}:invalid_source_status")
        return issues


@dataclass(frozen=True,slots=True)
class EngineeringStudyContext:
    study_id:str;revision:str;jurisdiction:str;units:str;sources:tuple[StudySource,...];normative_pack_id:str="";independent_review_status:str="PENDING"
    def validate(self)->list[str]:
        issues=[]
        if not all((self.study_id,self.revision,self.jurisdiction)):issues.append("study_identity_incomplete")
        if self.units!="SI":issues.append("unsupported_unit_system")
        ids=[x.source_id for x in self.sources]
        if not ids:issues.append("study_sources_required")
        if len(ids)!=len(set(ids)):issues.append("duplicate_study_source")
        for source in self.sources:issues.extend(source.validate())
        return issues
    def normative_claim_allowed(self)->bool:
        return not self.validate() and bool(self.normative_pack_id) and self.independent_review_status=="ACCEPTED" and all(x.status=="AUTHORIZED" for x in self.sources)


@dataclass(frozen=True,slots=True)
class GroundLayer:
    layer_id:str;thickness_m:float;unit_weight_kn_m3:float;source_id:str


@dataclass(frozen=True,slots=True)
class RockShearCase:
    case_id:str;cohesion_kpa:float;friction_angle_deg:float;normal_stress_kpa:float;applied_shear_kpa:float;source_id:str


@dataclass(frozen=True,slots=True)
class CatchmentCase:
    case_id:str;area_hectares:float;runoff_coefficient:float;rainfall_intensity_mm_h:float;source_id:str


@dataclass(frozen=True,slots=True)
class PressurePipeCase:
    case_id:str;length_m:float;diameter_m:float;flow_m3_s:float;hazen_williams_c:float;source_id:str


@dataclass(frozen=True,slots=True)
class GravityPipeCase:
    case_id:str;diameter_m:float;slope:float;manning_n:float;fill_ratio:float;source_id:str


@dataclass(frozen=True,slots=True)
class StudyResult:
    study_id:str;case_id:str;discipline:str;method:str;values:tuple[tuple[str,float,str],...];issues:tuple[str,...];normative_compliance_claimed:bool;construction_approved:bool=False
    def sha256(self)->str:
        data=json.dumps(asdict(self),sort_keys=True,separators=(",",":"),ensure_ascii=False)
        return hashlib.sha256(data.encode("utf-8")).hexdigest()


class GroundWaterEngineering:
    """Execute auditable equations; source acceptance remains an external gate."""
    @staticmethod
    def _base(context,case_id,source_id):
        issues=context.validate();known={x.source_id for x in context.sources}
        if not case_id:issues.append("case_id_required")
        if source_id not in known:issues.append("unknown_source_id")
        return issues

    def vertical_stress(self,context:EngineeringStudyContext,case_id:str,layers:tuple[GroundLayer,...])->StudyResult:
        issues=context.validate();known={x.source_id for x in context.sources}
        if not case_id:issues.append("case_id_required")
        if not layers:issues.append("ground_layers_required")
        for layer in layers:
            if not layer.layer_id or layer.thickness_m<=0 or layer.unit_weight_kn_m3<=0:issues.append(f"{layer.layer_id}:invalid_ground_layer")
            if layer.source_id not in known:issues.append(f"{layer.layer_id}:unknown_source_id")
        stress=sum(x.thickness_m*x.unit_weight_kn_m3 for x in layers) if not issues else 0.0
        return StudyResult(context.study_id,case_id,"GEOTECHNICS","TOTAL_VERTICAL_STRESS",(("vertical_stress",stress,"kPa"),),tuple(issues),context.normative_claim_allowed() and not issues)

    def rock_shear(self,context:EngineeringStudyContext,case:RockShearCase)->StudyResult:
        issues=self._base(context,case.case_id,case.source_id)
        if case.cohesion_kpa<0 or not 0<=case.friction_angle_deg<90 or case.normal_stress_kpa<0 or case.applied_shear_kpa<=0:issues.append("invalid_rock_shear_inputs")
        capacity=case.cohesion_kpa+case.normal_stress_kpa*math.tan(math.radians(case.friction_angle_deg)) if not issues else 0.0
        factor=capacity/case.applied_shear_kpa if not issues else 0.0
        return StudyResult(context.study_id,case.case_id,"ROCK_MECHANICS","MOHR_COULOMB_REFERENCE",(("shear_capacity",capacity,"kPa"),("factor_of_safety",factor,"ratio")),tuple(issues),context.normative_claim_allowed() and not issues)

    def rational_peak_flow(self,context:EngineeringStudyContext,case:CatchmentCase)->StudyResult:
        issues=self._base(context,case.case_id,case.source_id)
        if case.area_hectares<=0 or not 0<=case.runoff_coefficient<=1 or case.rainfall_intensity_mm_h<0:issues.append("invalid_catchment_inputs")
        flow=.00278*case.runoff_coefficient*case.rainfall_intensity_mm_h*case.area_hectares if not issues else 0.0
        return StudyResult(context.study_id,case.case_id,"HYDROLOGY","RATIONAL_METHOD_REFERENCE",(("peak_flow",flow,"m3/s"),),tuple(issues),context.normative_claim_allowed() and not issues)

    def pressure_pipe(self,context:EngineeringStudyContext,case:PressurePipeCase)->StudyResult:
        issues=self._base(context,case.case_id,case.source_id)
        if min(case.length_m,case.diameter_m,case.flow_m3_s,case.hazen_williams_c)<=0:issues.append("invalid_pressure_pipe_inputs")
        area=math.pi*case.diameter_m**2/4 if not issues else 0.0;velocity=case.flow_m3_s/area if not issues else 0.0
        loss=10.67*case.length_m*case.flow_m3_s**1.852/(case.hazen_williams_c**1.852*case.diameter_m**4.87) if not issues else 0.0
        return StudyResult(context.study_id,case.case_id,"WATER_NETWORK","HAZEN_WILLIAMS_SI_REFERENCE",(("velocity",velocity,"m/s"),("head_loss",loss,"m")),tuple(issues),context.normative_claim_allowed() and not issues)

    def gravity_pipe(self,context:EngineeringStudyContext,case:GravityPipeCase)->StudyResult:
        issues=self._base(context,case.case_id,case.source_id)
        if min(case.diameter_m,case.slope,case.manning_n)<=0 or not 0<case.fill_ratio<=1:issues.append("invalid_gravity_pipe_inputs")
        area=math.pi*case.diameter_m**2/4*case.fill_ratio if not issues else 0.0;radius=case.diameter_m/4 if not issues else 0.0
        capacity=(1/case.manning_n)*area*radius**(2/3)*case.slope**.5 if not issues else 0.0
        return StudyResult(context.study_id,case.case_id,"SANITARY_STORMWATER","MANNING_REFERENCE",(("capacity",capacity,"m3/s"),),tuple(issues),context.normative_claim_allowed() and not issues)
