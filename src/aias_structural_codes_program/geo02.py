"""GEO-02 governed reference design for piles, pile groups and diaphragm walls."""
from __future__ import annotations

from dataclasses import dataclass
import math
from .mdp02 import EngineeringStudyContext


@dataclass(frozen=True,slots=True)
class DeepPile:
    pile_id:str;diameter_m:float;length_m:float;unit_tip_resistance_kpa:float;unit_shaft_resistance_kpa:float;source_id:str


@dataclass(frozen=True,slots=True)
class PileGroupCase:
    case_id:str;piles:tuple[DeepPile,...];group_efficiency:float;axial_demand_kn:float;factor_of_safety:float


@dataclass(frozen=True,slots=True)
class DiaphragmWallCase:
    case_id:str;height_m:float;length_m:float;thickness_m:float;soil_unit_weight_kn_m3:float;active_pressure_coefficient:float;surcharge_kpa:float;source_id:str


@dataclass(frozen=True,slots=True)
class PileCapacityResult:
    pile_id:str;tip_capacity_kn:float;shaft_capacity_kn:float;ultimate_capacity_kn:float


@dataclass(frozen=True,slots=True)
class DeepFoundationResult:
    case_id:str;discipline:str;status:str;pile_capacities:tuple[PileCapacityResult,...];ultimate_group_capacity_kn:float;allowable_group_capacity_kn:float;demand_capacity_ratio:float|None;lateral_force_kn:float;overturning_moment_kn_m:float;issues:tuple[str,...];normative_compliance_claimed:bool;construction_approved:bool=False


class DeepFoundationEngine:
    """Execute transparent capacities while failing closed on missing evidence."""
    @staticmethod
    def _source_issues(context,source_id):
        return [] if source_id in {x.source_id for x in context.sources} else [f"{source_id}:unknown_source_id"]

    def pile_group(self,context:EngineeringStudyContext,case:PileGroupCase)->DeepFoundationResult:
        issues=context.validate()
        if not case.case_id:issues.append("case_id_required")
        if not case.piles:issues.append("piles_required")
        if not 0<case.group_efficiency<=1:issues.append("invalid_group_efficiency")
        if case.axial_demand_kn<0 or case.factor_of_safety<=1:issues.append("invalid_design_controls")
        ids=[x.pile_id for x in case.piles]
        if len(ids)!=len(set(ids)):issues.append("duplicate_pile_id")
        capacities=[]
        for pile in case.piles:
            issues.extend(self._source_issues(context,pile.source_id))
            if not pile.pile_id or min(pile.diameter_m,pile.length_m,pile.unit_tip_resistance_kpa,pile.unit_shaft_resistance_kpa)<=0:
                issues.append(f"{pile.pile_id}:invalid_pile_properties");continue
            tip=pile.unit_tip_resistance_kpa*math.pi*pile.diameter_m**2/4
            shaft=pile.unit_shaft_resistance_kpa*math.pi*pile.diameter_m*pile.length_m
            capacities.append(PileCapacityResult(pile.pile_id,tip,shaft,tip+shaft))
        ultimate=sum(x.ultimate_capacity_kn for x in capacities)*case.group_efficiency if capacities else 0.0
        allowable=ultimate/case.factor_of_safety if ultimate and case.factor_of_safety>0 else 0.0
        ratio=case.axial_demand_kn/allowable if allowable else None
        if ratio is not None and ratio>1:issues.append("pile_group_capacity_exceeded")
        normative=not issues and context.normative_claim_allowed()
        return DeepFoundationResult(case.case_id,"PILE_GROUP","PASS_NORMATIVE_REVIEW_REQUIRED" if normative else ("PASS_REFERENCE" if not issues else "REJECTED"),tuple(capacities),ultimate,allowable,ratio,0,0,tuple(issues),normative,False)

    def diaphragm_wall(self,context:EngineeringStudyContext,case:DiaphragmWallCase)->DeepFoundationResult:
        issues=context.validate()+self._source_issues(context,case.source_id)
        if not case.case_id:issues.append("case_id_required")
        if min(case.height_m,case.length_m,case.thickness_m,case.soil_unit_weight_kn_m3)<=0 or not 0<case.active_pressure_coefficient<=1 or case.surcharge_kpa<0:
            issues.append("invalid_diaphragm_wall_inputs")
        triangular=.5*case.active_pressure_coefficient*case.soil_unit_weight_kn_m3*case.height_m**2*case.length_m if not issues else 0.0
        uniform=case.active_pressure_coefficient*case.surcharge_kpa*case.height_m*case.length_m if not issues else 0.0
        moment=triangular*case.height_m/3+uniform*case.height_m/2 if not issues else 0.0
        normative=not issues and context.normative_claim_allowed()
        return DeepFoundationResult(case.case_id,"DIAPHRAGM_WALL","PASS_NORMATIVE_REVIEW_REQUIRED" if normative else ("PASS_REFERENCE" if not issues else "REJECTED"),(),0,0,None,triangular+uniform,moment,tuple(issues),normative,False)
