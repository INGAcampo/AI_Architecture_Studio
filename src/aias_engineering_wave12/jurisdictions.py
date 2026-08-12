"""Licensed, versioned and effective-date-aware jurisdiction pack registry."""
from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import date

@dataclass(frozen=True,slots=True)
class JurisdictionPack:
    """Declare a bounded jurisdiction pack without embedding unlicensed standards."""
    pack_id:str;jurisdiction:str;version:str;legal_status:str;effective_from:str;effective_to:str|None;license_id:str;provenance:str;unit_system:str;rules:tuple[dict,...];professional_review_required:bool=True
    def validate(self)->None:
        """Reject unattributed, unlicensed or falsely authoritative packs."""
        if not self.pack_id.startswith("JUR-") or not all((self.jurisdiction,self.version,self.license_id,self.provenance,self.unit_system)):raise ValueError("invalid_jurisdiction_pack")
        if self.legal_status not in {"REFERENCE_ONLY","VERIFIED_OFFICIAL"}:raise ValueError("invalid_legal_status")
        if self.legal_status=="VERIFIED_OFFICIAL" and not self.professional_review_required:raise ValueError("professional_review_boundary_required")
    def to_dict(self):
        """Project the jurisdiction pack into its stable dictionary representation."""
        return asdict(self)
class JurisdictionRegistry:
    """Register immutable packs and resolve only effective explicitly permitted versions."""
    def __init__(self):self.packs={}
    def register(self,pack:JurisdictionPack)->None:
        """Register one pack identity/version and reject conflicting replacement."""
        pack.validate();key=(pack.pack_id,pack.version)
        if key in self.packs and self.packs[key]!=pack:raise ValueError("jurisdiction_pack_conflict")
        self.packs[key]=pack
    def resolve(self,pack_id:str,on_date:date,allow_reference:bool=False)->JurisdictionPack:
        """Resolve an effective pack while requiring explicit opt-in for reference material."""
        candidates=[p for (i,_),p in self.packs.items() if i==pack_id and date.fromisoformat(p.effective_from)<=on_date and (not p.effective_to or on_date<=date.fromisoformat(p.effective_to))]
        if len(candidates)!=1:raise ValueError("jurisdiction_pack_not_uniquely_effective")
        pack=candidates[0]
        if pack.legal_status=="REFERENCE_ONLY" and not allow_reference:raise ValueError("reference_pack_requires_explicit_opt_in")
        return pack
