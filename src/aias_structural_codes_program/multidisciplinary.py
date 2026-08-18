"""MDP-01 governed design contracts for timber, masonry and advanced foundations."""
from __future__ import annotations

from dataclasses import dataclass
import math
from .material_codes import MaterialCodePack

SUPPORTED_SYSTEMS={
    "TIMBER":{"BEAM","COLUMN","TRUSS","PANEL","CONNECTION"},
    "MASONRY":{"BEARING_WALL","SHEAR_WALL","INFILL","PIER","LINTEL"},
    "ADVANCED_FOUNDATION":{"PILE","PILE_CAP","RAFT","CAISSON","DIAPHRAGM_WALL","ANCHOR"},
}


@dataclass(frozen=True,slots=True)
class DomainAction:
    check_id:str
    demand:float
    units:str


@dataclass(frozen=True,slots=True)
class DomainResistance:
    check_id:str
    resistance:float
    units:str
    rule_id:str


@dataclass(frozen=True,slots=True)
class DomainDesignRequest:
    design_id:str
    object_id:str
    domain:str
    system_type:str
    geometry_reference:str
    material_reference:str
    analysis_reference:str
    actions:tuple[DomainAction,...]
    resistances:tuple[DomainResistance,...]
    soil_model_reference:str=""

    def validate(self)->list[str]:
        issues=[]
        if not all((self.design_id,self.object_id,self.geometry_reference,self.material_reference,self.analysis_reference)):
            issues.append("design_traceability_incomplete")
        if self.domain not in SUPPORTED_SYSTEMS:
            issues.append("unsupported_design_domain")
        elif self.system_type not in SUPPORTED_SYSTEMS[self.domain]:
            issues.append("unsupported_system_type")
        if self.domain=="ADVANCED_FOUNDATION" and not self.soil_model_reference:
            issues.append("soil_model_reference_required")
        action_ids=[x.check_id for x in self.actions];resistance_ids=[x.check_id for x in self.resistances]
        if not action_ids:issues.append("design_actions_required")
        if len(action_ids)!=len(set(action_ids)):issues.append("duplicate_design_action")
        if len(resistance_ids)!=len(set(resistance_ids)):issues.append("duplicate_design_resistance")
        if set(action_ids)-set(resistance_ids):issues.append(f"missing_resistances:{sorted(set(action_ids)-set(resistance_ids))}")
        for row in self.actions:
            if not row.units or not math.isfinite(row.demand) or row.demand<0:issues.append(f"{row.check_id}:invalid_demand")
        for row in self.resistances:
            if not row.units or not row.rule_id or not math.isfinite(row.resistance) or row.resistance<=0:issues.append(f"{row.check_id}:invalid_resistance")
        return issues


@dataclass(frozen=True,slots=True)
class DomainCheckResult:
    check_id:str;demand:float;resistance:float;utilization:float;units:str;rule_id:str;status:str


@dataclass(frozen=True,slots=True)
class DomainDesignResult:
    design_id:str;domain:str;checks:tuple[DomainCheckResult,...];governing_check_id:str;governing_utilization:float|None;status:str;issues:tuple[str,...];normative_compliance_claimed:bool;construction_approved:bool=False


class GovernedDomainDesigner:
    """Calculate transparent demand/capacity checks while preserving normative boundaries."""
    def design(self,request:DomainDesignRequest,pack:MaterialCodePack,jurisdiction,on_date)->DomainDesignResult:
        issues=request.validate()+pack.validate()
        if pack.domain!=request.domain:issues.append("material_pack_domain_mismatch")
        capacities={x.check_id:x for x in request.resistances};checks=[]
        for action in request.actions:
            resistance=capacities.get(action.check_id)
            if resistance is None:continue
            if action.units!=resistance.units:
                issues.append(f"{action.check_id}:unit_mismatch");continue
            ratio=action.demand/resistance.resistance
            checks.append(DomainCheckResult(action.check_id,action.demand,resistance.resistance,ratio,action.units,resistance.rule_id,"PASS" if ratio<=1 else "FAIL"))
            if ratio>1:issues.append(f"{action.check_id}:capacity_exceeded")
        governing=max(checks,key=lambda x:x.utilization) if checks else None
        normative=not issues and pack.normative_claim_allowed(jurisdiction,on_date)
        if not checks:status="REJECTED"
        elif issues:status="REJECTED"
        elif normative:status="PASS_NORMATIVE_REVIEW_REQUIRED"
        else:status="PASS_REFERENCE"
        return DomainDesignResult(request.design_id,request.domain,tuple(checks),governing.check_id if governing else "",governing.utilization if governing else None,status,tuple(issues),normative,False)
