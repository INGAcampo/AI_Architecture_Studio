"""Virtual engineer and work-order contracts with explicit legal limitations."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field
@dataclass(frozen=True,slots=True)
class VirtualEngineer:
    """Represent a non-human AIAS worker with bounded verified competencies."""
    engineer_id:str;name:str;role:str;office_id:str;competencies:tuple[str,...];authorized_actions:tuple[str,...];credential_refs:tuple[str,...];status:str="AVAILABLE";licensed_professional:bool=False
    def validate(self):
        """Reject incomplete identity, uncredentialed competencies or license claims."""
        if not self.engineer_id.startswith("VE-") or not all((self.name,self.role,self.office_id)):raise ValueError("invalid_virtual_engineer")
        if not self.competencies or not self.authorized_actions or not self.credential_refs:raise ValueError("incomplete_virtual_engineer_authority")
        if self.licensed_professional:raise ValueError("virtual_engineer_cannot_be_licensed_professional")
    def to_dict(self):
        """Project the virtual engineer into its stable dictionary representation."""
        return asdict(self)
@dataclass(frozen=True,slots=True)
class WorkOrder:
    """Declare one attributable, evidence-producing and risk-classified task."""
    work_id:str;title:str;required_competencies:tuple[str,...];action:str;source_ref:str;risk_level:str;regulated:bool=False;metadata:dict=field(default_factory=dict)
    def validate(self):
        """Reject incomplete work, unsupported risk levels or missing competence needs."""
        if not all((self.work_id,self.title,self.action,self.source_ref)) or not self.required_competencies:raise ValueError("invalid_work_order")
        if self.risk_level not in {"LOW","MEDIUM","HIGH","CRITICAL"}:raise ValueError("invalid_risk_level")
