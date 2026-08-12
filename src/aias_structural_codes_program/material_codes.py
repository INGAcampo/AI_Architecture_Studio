"""Coverage and evidence contracts for licensed material code packs."""
from __future__ import annotations
from dataclasses import dataclass
from .normative import StructuralCodePack
REQUIRED_COVERAGE={
 "CONCRETE":{"FLEXURE","SHEAR","AXIAL","INTERACTION","SERVICEABILITY","DETAILING","DURABILITY","SEISMIC_DETAILING"},
 "STEEL":{"TENSION","COMPRESSION","FLEXURE","SHEAR","INTERACTION","STABILITY","SERVICEABILITY","CONNECTIONS","SEISMIC_DETAILING"},
 "FOUNDATION":{"BEARING","SLIDING","OVERTURNING","ONE_WAY_SHEAR","PUNCHING","FLEXURE","SETTLEMENT","DETAILING"},
 "TIMBER":{"TENSION","COMPRESSION","FLEXURE","SHEAR","INTERACTION","STABILITY","SERVICEABILITY","CONNECTIONS","DURABILITY","FIRE"},
 "MASONRY":{"AXIAL","IN_PLANE_SHEAR","OUT_OF_PLANE_FLEXURE","INTERACTION","SLENDERNESS","SERVICEABILITY","CONNECTIONS","DETAILING","SEISMIC_DETAILING"},
 "ADVANCED_FOUNDATION":{"AXIAL_GEOTECHNICAL","LATERAL_GEOTECHNICAL","STRUCTURAL_CAPACITY","GROUP_EFFECTS","SETTLEMENT","UPLIFT","PILE_CAP","RAFT","DIAPHRAGM_WALL","SOIL_STRUCTURE_INTERACTION","DURABILITY","CONSTRUCTABILITY"},
}
@dataclass(frozen=True,slots=True)
class CodeCheckRule:
    rule_id:str;category:str;source_id:str;source_locator:str;implementation_id:str;test_evidence:str;units:str
    def validate(self)->list[str]:return [] if all((self.rule_id,self.category,self.source_id,self.source_locator,self.implementation_id,self.test_evidence,self.units)) else [f"{self.rule_id}:incomplete_rule_traceability"]
@dataclass(frozen=True,slots=True)
class MaterialCodePack:
    pack_id:str;version:str;domain:str;parent:StructuralCodePack;rules:tuple[CodeCheckRule,...];benchmark_evidence:tuple[str,...];independent_review_status:str
    def validate(self)->list[str]:
        issues=self.parent.validate()
        if self.domain not in REQUIRED_COVERAGE:return issues+["unsupported_material_domain"]
        if not self.pack_id or not self.version:issues.append("material_pack_identity_incomplete")
        ids=[x.rule_id for x in self.rules]
        if len(ids)!=len(set(ids)):issues.append("duplicate_rule_id")
        for rule in self.rules:issues.extend(rule.validate())
        missing=REQUIRED_COVERAGE[self.domain]-{x.category for x in self.rules}
        if missing:issues.append(f"missing_coverage:{sorted(missing)}")
        if not self.benchmark_evidence:issues.append("benchmark_evidence_required")
        return issues
    def normative_claim_allowed(self,jurisdiction,on_date)->bool:return not self.validate() and self.parent.normative_claim_allowed(jurisdiction,on_date) and self.independent_review_status=="ACCEPTED"
    def coverage(self)->dict:
        required=REQUIRED_COVERAGE.get(self.domain,set());present={x.category for x in self.rules};return {"domain":self.domain,"required":sorted(required),"present":sorted(present),"missing":sorted(required-present),"complete":required<=present}
