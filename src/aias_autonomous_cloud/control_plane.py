"""Persistent fair scheduler, authorization, leases, recovery and audit records."""
from __future__ import annotations
import hashlib,json,os,tempfile
from datetime import datetime,timedelta,timezone
from pathlib import Path
from .models import CloudJob,TenantQuota,Worker
class AutonomousCloudControlPlane:
    """Coordinate tenant-isolated engineering jobs without binding a cloud provider."""
    def __init__(self,path:Path):self.path=path;self.data=self._load();self.quotas={}
    def _load(self):return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {"schema_version":"1.0.0","jobs":{},"audit":[],"principals":{}}
    def register_tenant(self,quota:TenantQuota,principals:dict[str,tuple[str,...]]):
        """Register quota and tenant-scoped principal roles."""
        quota.validate();self.quotas[quota.tenant_id]=quota
        for principal,roles in principals.items():self.data["principals"][principal]={"tenant_id":quota.tenant_id,"roles":list(roles)}
        self._audit("tenant.registered",quota.tenant_id,{"principals":sorted(principals)});self._save()
    def submit(self,job:CloudJob,principal:str)->dict:
        """Submit an immutable job after tenant authorization and queue-quota checks."""
        job.validate();self._authorize(principal,job.tenant_id,"submit");quota=self._quota(job.tenant_id);queued=sum(x["tenant_id"]==job.tenant_id and x["status"]=="QUEUED" for x in self.data["jobs"].values())
        if queued>=quota.max_queued:raise ValueError("queued_job_quota_exceeded")
        old=self.data["jobs"].get(job.job_id);row={**job.to_dict(),"status":"QUEUED","submitted_at":self._now(),"attempt":0,"lease":None,"artifacts":[]}
        if old and old!=row:raise ValueError("job_id_conflict")
        self.data["jobs"][job.job_id]=old or row;self._audit("job.submitted",job.tenant_id,{"job_id":job.job_id,"principal":principal});self._save();return self.data["jobs"][job.job_id]
    def lease(self,worker:Worker,lease_seconds:int=60,now:datetime|None=None)->dict|None:
        """Lease the fairest compatible queued job while enforcing tenant concurrency."""
        worker.validate();now=now or datetime.now(timezone.utc);self.recover_expired(now);candidates=[]
        for job in self.data["jobs"].values():
            if job["status"]!="QUEUED" or not set(job["required_capabilities"])<=set(worker.capabilities):continue
            running=sum(x["tenant_id"]==job["tenant_id"] and x["status"]=="RUNNING" for x in self.data["jobs"].values())
            if running<self._quota(job["tenant_id"]).max_running:candidates.append((running,-job["priority"],job["submitted_at"],job["job_id"],job))
        if not candidates:return None
        job=min(candidates)[-1];job["status"]="RUNNING";job["attempt"]+=1;job["lease"]={"worker_id":worker.worker_id,"expires_at":(now+timedelta(seconds=lease_seconds)).isoformat()};self._audit("job.leased",job["tenant_id"],{"job_id":job["job_id"],"worker_id":worker.worker_id});self._save();return json.loads(json.dumps(job))
    def heartbeat(self,job_id:str,worker_id:str,lease_seconds:int=60,now:datetime|None=None):
        """Extend only the current worker lease for a running job."""
        job=self._running(job_id,worker_id);now=now or datetime.now(timezone.utc);job["lease"]["expires_at"]=(now+timedelta(seconds=lease_seconds)).isoformat();self._save()
    def complete(self,job_id:str,worker_id:str,artifacts:list[dict],evidence:dict)->dict:
        """Complete a leased job only with validation and artifact integrity evidence."""
        job=self._running(job_id,worker_id)
        if not evidence.get("validation") or not all(len(x.get("sha256",""))==64 for x in artifacts):raise ValueError("incomplete_completion_evidence")
        job.update({"status":"COMPLETED","lease":None,"artifacts":artifacts,"completion_evidence":evidence,"completed_at":self._now()});self._audit("job.completed",job["tenant_id"],{"job_id":job_id,"worker_id":worker_id});self._save();return job
    def recover_expired(self,now:datetime|None=None)->list[str]:
        """Requeue expired jobs without losing attempt or audit history."""
        now=now or datetime.now(timezone.utc);recovered=[]
        for job in self.data["jobs"].values():
            if job["status"]=="RUNNING" and datetime.fromisoformat(job["lease"]["expires_at"])<=now:job["status"]="QUEUED";job["lease"]=None;recovered.append(job["job_id"]);self._audit("job.recovered",job["tenant_id"],{"job_id":job["job_id"]})
        if recovered:self._save()
        return recovered
    def _authorize(self,principal,tenant,action):
        row=self.data["principals"].get(principal)
        if not row or row["tenant_id"]!=tenant or action not in row["roles"]:raise ValueError("tenant_authorization_denied")
    def _quota(self,tenant):
        if tenant not in self.quotas:raise ValueError("unknown_tenant")
        return self.quotas[tenant]
    def _running(self,job_id,worker):
        job=self.data["jobs"].get(job_id)
        if not job or job["status"]!="RUNNING" or job["lease"]["worker_id"]!=worker:raise ValueError("invalid_job_lease")
        return job
    def _audit(self,event,tenant,payload):
        previous=self.data["audit"][-1]["record_sha256"] if self.data["audit"] else "GENESIS";row={"sequence":len(self.data["audit"])+1,"event":event,"tenant_id":tenant,"payload":payload,"occurred_at":self._now(),"previous_sha256":previous};row["record_sha256"]=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest();self.data["audit"].append(row)
    @staticmethod
    def _now():return datetime.now(timezone.utc).isoformat()
    def _save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.data,stream,ensure_ascii=False,indent=2,sort_keys=True);stream.write("\n")
            os.replace(name,self.path)
        finally:
            if os.path.exists(name):os.unlink(name)
