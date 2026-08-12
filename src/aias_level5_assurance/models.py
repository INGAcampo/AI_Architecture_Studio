"""Longitudinal evidence, organizational snapshot and independent audit contracts."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field
@dataclass(frozen=True,slots=True)
class AssuranceEvidence:
    """Represent classified dated evidence for one Level 5 criterion."""
    evidence_id:str;criterion_id:str;classification:str;observed_at:str;source:str;value:object;sha256:str;project_id:str|None=None
    def validate(self):
        """Validate validate for honest Level 5 evidence and maturity assurance and report explicit issues."""
        if not all((self.evidence_id,self.criterion_id,self.observed_at,self.source)) or len(self.sha256)!=64:raise ValueError("invalid_assurance_evidence")
        if self.classification not in {"REFERENCE_VALIDATION","PRODUCTION_OBSERVATION","INDEPENDENT_AUDIT"}:raise ValueError("invalid_evidence_classification")
@dataclass(frozen=True,slots=True)
class AuditAttestation:
    """Represent a non-self-issued independent organizational audit conclusion."""
    audit_id:str;auditor_organization:str;auditor_identity:str;accreditation_ref:str;issued_at:str;scope:str;conclusion:str;open_critical_findings:int;evidence_sha256:str;independent:bool
    def validate(self):
        """Validate validate for honest Level 5 evidence and maturity assurance and report explicit issues."""
        if not all((self.audit_id,self.auditor_organization,self.auditor_identity,self.accreditation_ref,self.issued_at,self.scope,self.conclusion)) or len(self.evidence_sha256)!=64:raise ValueError("invalid_audit_attestation")
        if not self.independent:raise ValueError("self_audit_not_sufficient")
@dataclass(frozen=True,slots=True)
class OrganizationalSnapshot:
    """Declare measured organizational outcomes over an explicit observation window."""
    organization_id:str;window_start:str;window_end:str;completed_projects:int;operational_systems:tuple[str,...];metrics:dict;critical_findings:int=0
