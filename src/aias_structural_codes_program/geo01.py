"""GEO-01 governed soil-structure interaction reference contract."""
from __future__ import annotations

from dataclasses import asdict,dataclass
import hashlib,json,math
from .mdp02 import EngineeringStudyContext


@dataclass(frozen=True,slots=True)
class SoilSpring:
    spring_id:str;structural_node_id:str;direction:str;stiffness_kn_m:float;ultimate_reaction_kn:float;source_id:str


@dataclass(frozen=True,slots=True)
class InterfaceDisplacement:
    structural_node_id:str;direction:str;displacement_m:float;load_case_id:str


@dataclass(frozen=True,slots=True)
class SoilStructureRequest:
    analysis_id:str;structural_model_reference:str;geotechnical_model_reference:str;context:EngineeringStudyContext;springs:tuple[SoilSpring,...];displacements:tuple[InterfaceDisplacement,...];iteration_tolerance:float=.001;maximum_iterations:int=50
    def validate(self)->list[str]:
        issues=self.context.validate();known={x.source_id for x in self.context.sources}
        if not all((self.analysis_id,self.structural_model_reference,self.geotechnical_model_reference)):issues.append("ssi_traceability_incomplete")
        if not self.springs:issues.append("soil_springs_required")
        if not self.displacements:issues.append("interface_displacements_required")
        ids=[x.spring_id for x in self.springs]
        if len(ids)!=len(set(ids)):issues.append("duplicate_soil_spring")
        keys=[]
        for row in self.springs:
            keys.append((row.structural_node_id,row.direction))
            if row.direction not in {"X","Y","Z","RX","RY","RZ"}:issues.append(f"{row.spring_id}:invalid_direction")
            if row.stiffness_kn_m<=0 or row.ultimate_reaction_kn<=0:issues.append(f"{row.spring_id}:invalid_spring_properties")
            if row.source_id not in known:issues.append(f"{row.spring_id}:unknown_source_id")
        if len(keys)!=len(set(keys)):issues.append("duplicate_node_direction_spring")
        if self.iteration_tolerance<=0 or self.maximum_iterations<=0:issues.append("invalid_iteration_controls")
        for row in self.displacements:
            if not row.load_case_id or not math.isfinite(row.displacement_m):issues.append(f"{row.structural_node_id}:invalid_displacement")
        return issues


@dataclass(frozen=True,slots=True)
class InterfaceReaction:
    spring_id:str;structural_node_id:str;direction:str;load_case_id:str;displacement_m:float;reaction_kn:float;secant_stiffness_kn_m:float;yielded:bool


@dataclass(frozen=True,slots=True)
class SoilStructureResult:
    analysis_id:str;status:str;reactions:tuple[InterfaceReaction,...];unmatched_interfaces:tuple[str,...];maximum_utilization:float;issues:tuple[str,...];request_sha256:str;normative_compliance_claimed:bool;construction_approved:bool=False


class SoilStructureInteractionEngine:
    """Resolve bounded Winkler reactions with explicit geotechnical provenance."""
    def analyze(self,request:SoilStructureRequest)->SoilStructureResult:
        issues=request.validate();springs={(x.structural_node_id,x.direction):x for x in request.springs};reactions=[];unmatched=[];maximum=0.0
        for displacement in request.displacements:
            spring=springs.get((displacement.structural_node_id,displacement.direction))
            if spring is None:
                marker=f"{displacement.structural_node_id}:{displacement.direction}:{displacement.load_case_id}";unmatched.append(marker);issues.append(f"{marker}:spring_missing");continue
            elastic=spring.stiffness_kn_m*displacement.displacement_m
            reaction=math.copysign(min(abs(elastic),spring.ultimate_reaction_kn),elastic)
            utilization=abs(elastic)/spring.ultimate_reaction_kn;maximum=max(maximum,utilization)
            secant=abs(reaction/displacement.displacement_m) if displacement.displacement_m else spring.stiffness_kn_m
            reactions.append(InterfaceReaction(spring.spring_id,spring.structural_node_id,spring.direction,displacement.load_case_id,displacement.displacement_m,reaction,secant,abs(elastic)>spring.ultimate_reaction_kn))
        payload=json.dumps(asdict(request),sort_keys=True,separators=(",",":"),ensure_ascii=False)
        digest=hashlib.sha256(payload.encode("utf-8")).hexdigest();normative=not issues and request.context.normative_claim_allowed()
        return SoilStructureResult(request.analysis_id,"COMPLETED" if not issues else "REJECTED",tuple(reactions),tuple(unmatched),maximum,tuple(issues),digest,normative,False)
