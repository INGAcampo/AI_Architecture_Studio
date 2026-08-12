"""Explicit policy, recovery objectives and retention planning."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone

@dataclass(frozen=True,slots=True)
class SecurityRecoveryPolicy:
    """Define backup exclusions, cryptographic controls and recovery objectives."""
    rpo_minutes:int=60
    rto_minutes:int=120
    retention_count:int=10
    forbidden_names:tuple[str,...] = (".env","secrets.json","credentials.json","id_rsa","id_ed25519")
    forbidden_suffixes:tuple[str,...] = (".pem",".key",".pfx",".p12")
    def validate(self)->None:
        """Reject non-positive objectives or retention that cannot preserve history."""
        if self.rpo_minutes<=0 or self.rto_minutes<=0 or self.retention_count<2:raise ValueError("invalid_recovery_policy")
    def retention_candidates(self,snapshots:list[dict])->list[str]:
        """Plan oldest verified snapshot removals without deleting any data."""
        ordered=sorted((x for x in snapshots if x.get("verified")),key=lambda x:x.get("created_at",""),reverse=True)
        return [x["snapshot_id"] for x in ordered[self.retention_count:]]
    def objective_status(self,last_verified_at:str|None,recovery_seconds:float|None,now:datetime|None=None)->dict:
        """Evaluate measured RPO age and recovery duration against declared targets."""
        now=now or datetime.now(timezone.utc);age=None if not last_verified_at else (now-datetime.fromisoformat(last_verified_at)).total_seconds()/60
        return {"rpo_minutes":self.rpo_minutes,"rto_minutes":self.rto_minutes,"measured_rpo_minutes":age,"measured_rto_minutes":None if recovery_seconds is None else recovery_seconds/60,"rpo_met":age is not None and age<=self.rpo_minutes,"rto_met":recovery_seconds is not None and recovery_seconds/60<=self.rto_minutes}
