"""Tenant-isolated content-addressed artifact storage."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
class TenantArtifactStore:
    """Store immutable artifacts by digest within explicit tenant namespaces."""
    def __init__(self,root:Path,quota_lookup):self.root=root.resolve();self.quota_lookup=quota_lookup
    def put(self,tenant_id:str,job_id:str,name:str,data:bytes)->dict:
        """Store a safe artifact only if the tenant byte quota permits it."""
        if not name or Path(name).name!=name or any(x in name for x in ("..","/","\\")):raise ValueError("unsafe_artifact_name")
        quota=self.quota_lookup(tenant_id);tenant=(self.root/tenant_id).resolve()
        if self.root not in tenant.parents:raise ValueError("unsafe_tenant_path")
        used=sum(p.stat().st_size for p in tenant.rglob("*.blob")) if tenant.exists() else 0
        if used+len(data)>quota.max_artifact_bytes:raise ValueError("artifact_quota_exceeded")
        digest=hashlib.sha256(data).hexdigest();path=tenant/digest[:2]/f"{digest}.blob";path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists() and path.read_bytes()!=data:raise ValueError("artifact_digest_conflict")
        path.write_bytes(data);meta={"tenant_id":tenant_id,"job_id":job_id,"name":name,"sha256":digest,"bytes":len(data),"path":str(path)};(path.with_suffix(".json")).write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8");return meta
    def get(self,tenant_id:str,sha256:str)->bytes:
        """Read an artifact only from its owning tenant namespace and verify integrity."""
        path=self.root.resolve()/tenant_id/sha256[:2]/f"{sha256}.blob"
        if not path.is_file():raise ValueError("artifact_not_found")
        data=path.read_bytes()
        if hashlib.sha256(data).hexdigest()!=sha256:raise ValueError("artifact_integrity_failure")
        return data
