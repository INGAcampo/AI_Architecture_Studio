"""Tenant quota, cloud job and worker contracts."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field
@dataclass(frozen=True,slots=True)
class TenantQuota:
    """Bound queued, running and artifact consumption for one tenant."""
    tenant_id:str;max_queued:int;max_running:int;max_artifact_bytes:int
    def validate(self):
        """Validate validate for the cloud-neutral autonomous engineering control plane and report explicit issues."""
        if not self.tenant_id.startswith("TEN-") or min(self.max_queued,self.max_running,self.max_artifact_bytes)<=0:raise ValueError("invalid_tenant_quota")
@dataclass(frozen=True,slots=True)
class CloudJob:
    """Declare one immutable tenant-owned and capability-constrained cloud job."""
    job_id:str;tenant_id:str;project_id:str;required_capabilities:tuple[str,...];payload:dict;max_runtime_seconds:int=3600;priority:int=50
    def validate(self):
        """Validate validate for the cloud-neutral autonomous engineering control plane and report explicit issues."""
        if not self.job_id.startswith("JOB-") or not self.tenant_id.startswith("TEN-") or not self.project_id or not self.required_capabilities:raise ValueError("invalid_cloud_job")
        if self.max_runtime_seconds<=0 or not 0<=self.priority<=100:raise ValueError("invalid_cloud_job_limits")
    def to_dict(self):
        """Project the cloud job into its stable dictionary representation."""
        return asdict(self)
@dataclass(frozen=True,slots=True)
class Worker:
    """Declare an ephemeral worker and its explicit execution capabilities."""
    worker_id:str;capabilities:tuple[str,...];trusted:bool=True
    def validate(self):
        """Validate validate for the cloud-neutral autonomous engineering control plane and report explicit issues."""
        if not self.worker_id.startswith("WRK-") or not self.capabilities or not self.trusted:raise ValueError("invalid_or_untrusted_worker")
