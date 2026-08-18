"""Immutable charters and work-item contracts for AIAS enterprise offices."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field

@dataclass(frozen=True,slots=True)
class OfficeCharter:
    """Define one office mandate, authority, controls and measurable outcomes."""
    office_id:str
    name:str
    mandate:tuple[str,...]
    accountable_for:tuple[str,...]
    decision_rights:tuple[str,...]
    required_evidence:tuple[str,...]
    kpis:tuple[str,...]
    escalation_to:str
    dependencies:tuple[str,...]=()
    def validate(self)->None:
        """Reject incomplete or unaccountable office charters."""
        if not self.office_id.startswith("OFFICE-") or not self.name or not self.escalation_to:raise ValueError("invalid_office_identity")
        if not all((self.mandate,self.accountable_for,self.decision_rights,self.required_evidence,self.kpis)):raise ValueError("incomplete_office_charter")
    def to_dict(self)->dict:
        """Serialize an office charter for the canonical registry."""
        return asdict(self)

@dataclass(frozen=True,slots=True)
class WorkItem:
    """Represent an attributable item requiring one accountable office owner."""
    item_id:str
    category:str
    title:str
    source:str
    evidence:dict=field(default_factory=dict)
