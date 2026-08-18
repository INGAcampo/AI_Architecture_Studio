"""Governed orchestration, normalized evidence and event publication."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from typing import Callable
from .adapters import default_runners,normalize
from .contracts import DevelopmentJob,DevelopmentResult
from .policy import DevelopmentPolicy


class DevelopmentPlatform:
    """Execute specification-driven production through a controlled AEPS adapter."""
    def __init__(self, allowed_root: Path, runners: dict[str,Callable]|None=None, event_sink: Callable[[dict],None]|None=None):
        self.allowed_root=allowed_root;self.runners=runners or default_runners();self.event_sink=event_sink or (lambda event:None);self.policy=DevelopmentPolicy()
    def execute(self, job: DevelopmentJob) -> DevelopmentResult:
        """Validate, select, execute and record a tamper-evident normalized build."""
        payload=self.policy.validate(job,self.allowed_root);engine=self.policy.select(payload,job.mode)
        self.event_sink({"type":"development.started","job_id":job.job_id,"engine":engine,"correlation_id":job.correlation_id})
        raw=self.runners[engine](job.specification.resolve(),job.workspace.resolve());certified,artifacts,evidence=normalize(job.job_id,engine,raw)
        canonical=json.dumps({"job_id":job.job_id,"engine":engine,"certified":certified,"artifacts":artifacts,"evidence":evidence},ensure_ascii=False,sort_keys=True,default=str).encode()
        record={"schema_version":"1.0.0","job_id":job.job_id,"engine":engine,"certified":certified,"specification_id":payload["id"],"specification_version":payload["version"],"correlation_id":job.correlation_id,"completed_at":datetime.now(timezone.utc).isoformat(),"evidence_sha256":hashlib.sha256(canonical).hexdigest()}
        evidence={**evidence,"development_platform":record};result=DevelopmentResult(job.job_id,engine,certified,artifacts,evidence)
        self.event_sink({"type":"development.completed","job_id":job.job_id,"engine":engine,"certified":certified,"correlation_id":job.correlation_id,"evidence_sha256":record["evidence_sha256"]})
        return result
