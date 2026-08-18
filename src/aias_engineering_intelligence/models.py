"""Immutable intelligence request, evidence and recommendation contracts."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field
@dataclass(frozen=True,slots=True)
class Evidence:
    """Represent one attributable integrity-verifiable fact supporting a decision."""
    evidence_id:str;evidence_type:str;source:str;claim:str;value:object;trust:float;sha256:str;legal_status:str="REFERENCE_ONLY";metadata:dict=field(default_factory=dict)
    def validate(self):
        """Reject incomplete, weakly identified or invalidly scored evidence."""
        if not all((self.evidence_id,self.evidence_type,self.source,self.claim)) or len(self.sha256)!=64:raise ValueError("invalid_evidence_identity")
        if not 0<=self.trust<=1:raise ValueError("invalid_evidence_trust")
@dataclass(frozen=True,slots=True)
class IntelligenceRequest:
    """Declare a bounded question, expected claims, risk and regulatory context."""
    request_id:str;question:str;required_claims:tuple[str,...];risk_level:str;regulated:bool;context_ref:str
    def validate(self):
        """Reject open-ended or improperly classified intelligence requests."""
        if not all((self.request_id,self.question,self.required_claims,self.context_ref)):raise ValueError("invalid_intelligence_request")
        if self.risk_level not in {"LOW","MEDIUM","HIGH","CRITICAL"}:raise ValueError("invalid_risk_level")
@dataclass(frozen=True,slots=True)
class Recommendation:
    """Return a recommendation or abstention with complete evidence lineage."""
    request_id:str;status:str;recommendation:str;confidence:float;evidence_ids:tuple[str,...];reasons:tuple[str,...];professional_review_required:bool;final_authority:str="HUMAN_OR_GOVERNED_WORKFLOW"
    def to_dict(self):
        """Project the recommendation into its stable dictionary representation."""
        return asdict(self)
