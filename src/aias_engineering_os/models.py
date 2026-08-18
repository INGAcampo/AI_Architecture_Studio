"""Service and idempotent operating-command contracts for AEOS."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field
@dataclass(frozen=True,slots=True)
class ServiceDescriptor:
    """Declare one versioned AEOS service and its operational dependencies."""
    service_id:str;name:str;version:str;capabilities:tuple[str,...];dependencies:tuple[str,...]=();health:str="READY"
    def validate(self):
        """Reject incomplete, capability-free or invalid-health services."""
        if not all((self.service_id,self.name,self.version)) or not self.capabilities:raise ValueError("invalid_service_descriptor")
        if self.health not in {"READY","DEGRADED","UNAVAILABLE"}:raise ValueError("invalid_service_health")
    def to_dict(self):
        """Project the service descriptor into its stable dictionary representation."""
        return asdict(self)
@dataclass(frozen=True,slots=True)
class OperatingCommand:
    """Request one project-state transition with evidence and correlation identity."""
    command_id:str;project_id:str;target_state:str;actor:str;correlation_id:str;evidence:dict=field(default_factory=dict)
    def validate(self):
        """Reject unattributed or uncorrelated operating commands."""
        if not all((self.command_id,self.project_id,self.target_state,self.actor,self.correlation_id)):raise ValueError("invalid_operating_command")
