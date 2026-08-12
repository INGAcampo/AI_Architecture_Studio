"""Licensed, jurisdiction-aware structural rule-pack contracts."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from math import isfinite

@dataclass(frozen=True,slots=True)
class NormativeSource:
    source_id:str;title:str;edition:str;publisher:str;license_id:str;provenance_uri:str
@dataclass(frozen=True,slots=True)
class LoadCombination:
    combination_id:str;factors:tuple[tuple[str,float],...];limit_state:str
    def evaluate(self,case_values:dict[str,float])->float:
        missing={case for case,_ in self.factors}-set(case_values)
        if missing:raise ValueError(f"missing_load_cases:{sorted(missing)}")
        return sum(case_values[case]*factor for case,factor in self.factors)
@dataclass(frozen=True,slots=True)
class SeismicParameters:
    hazard_source:str;site_class:str;importance_factor:float;response_modification_factor:float;damping_ratio:float
@dataclass(frozen=True,slots=True)
class StructuralCodePack:
    pack_id:str;version:str;jurisdiction:str;effective_from:date;effective_to:date|None;legal_status:str;sources:tuple[NormativeSource,...];combinations:tuple[LoadCombination,...];seismic:SeismicParameters|None;professional_review_required:bool=True
    def validate(self)->list[str]:
        issues=[]
        if not all((self.pack_id,self.version,self.jurisdiction,self.legal_status)):issues.append("pack_identity_incomplete")
        if not self.sources:issues.append("normative_sources_required")
        for source in self.sources:
            if not all((source.source_id,source.title,source.edition,source.publisher,source.license_id,source.provenance_uri)):issues.append(f"{source.source_id}:source_incomplete")
        ids=[x.combination_id for x in self.combinations]
        if len(ids)!=len(set(ids)):issues.append("duplicate_combination")
        for combination in self.combinations:
            if combination.limit_state not in {"ULTIMATE","SERVICEABILITY","SEISMIC"}:issues.append(f"{combination.combination_id}:invalid_limit_state")
            if not combination.factors or not all(isfinite(f) for _,f in combination.factors):issues.append(f"{combination.combination_id}:invalid_factors")
        if self.seismic and (not self.seismic.hazard_source or self.seismic.importance_factor<=0 or self.seismic.response_modification_factor<=0 or not 0<self.seismic.damping_ratio<1):issues.append("invalid_seismic_parameters")
        if not self.professional_review_required:issues.append("professional_review_boundary_missing")
        return issues
    def applicable(self,jurisdiction:str,on_date:date)->bool:
        return self.jurisdiction==jurisdiction and self.effective_from<=on_date and (self.effective_to is None or on_date<=self.effective_to)
    def normative_claim_allowed(self,jurisdiction:str,on_date:date)->bool:
        return not self.validate() and self.applicable(jurisdiction,on_date) and self.legal_status=="OFFICIAL_VERIFIED" and all(x.license_id not in {"","UNLICENSED","DEMO"} for x in self.sources)
