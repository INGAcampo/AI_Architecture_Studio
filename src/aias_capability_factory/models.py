"""Blueprint and lifecycle records for repeatable AIAS capability production."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field

@dataclass(frozen=True,slots=True)
class CapabilityBlueprint:
    """Specify one reusable capability and its governed production contract."""
    capability_id:str
    name:str
    domain:str
    version:str
    requirements:tuple[dict,...]
    architecture_refs:tuple[str,...]
    adr_refs:tuple[str,...]
    owner:str
    approval_id:str
    engine_mode:str="auto"
    metadata:dict=field(default_factory=dict)
    def validate(self)->None:
        """Reject incomplete, unapproved or untraceable capability blueprints."""
        if not self.capability_id.startswith("CAP-") or not all((self.name,self.domain,self.version,self.owner,self.approval_id)):raise ValueError("invalid_blueprint_identity")
        if not self.requirements or not self.architecture_refs or not self.adr_refs:raise ValueError("incomplete_blueprint_traceability")
        if any(not r.get("id") or not r.get("statement") for r in self.requirements):raise ValueError("invalid_requirement")
    def to_dict(self)->dict:
        """Serialize the immutable blueprint for registry persistence."""
        return asdict(self)

@dataclass(frozen=True,slots=True)
class CapabilityRecord:
    """Record the current governed state and accumulated evidence of a capability."""
    capability_id:str
    state:str
    version:str
    blueprint:dict
    evidence:dict=field(default_factory=dict)
    history:tuple[dict,...]=()
    def to_dict(self)->dict:
        """Serialize the capability lifecycle record."""
        return asdict(self)
