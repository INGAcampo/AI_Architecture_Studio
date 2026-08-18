from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CheckpointReadiness:
    ready:bool
    reasons:tuple[str,...]

def check_checkpoint_readiness(*,queue_audit_passed:bool,dependency_closure_passed:bool,manifest_integrity_passed:bool,canonical_tracked_clean:bool)->CheckpointReadiness:
    reasons=[]
    if not queue_audit_passed:
        reasons.append("queue_audit_failed")
    if not dependency_closure_passed:
        reasons.append("dependency_closure_failed")
    if not manifest_integrity_passed:
        reasons.append("manifest_integrity_failed")
    if not canonical_tracked_clean:
        reasons.append("canonical_not_tracked_clean")
    return CheckpointReadiness(not reasons,tuple(reasons))
