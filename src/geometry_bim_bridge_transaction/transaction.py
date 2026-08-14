from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class GeometryTransactionDecision:
    accepted:bool
    reason:str

def evaluate_geometry_transaction(*,patch_guard_passed:bool,rollback_fully_reversible:bool,target_snapshot_available:bool)->GeometryTransactionDecision:
    if not patch_guard_passed:
        return GeometryTransactionDecision(False,"patch_guard_failed")
    if not target_snapshot_available:
        return GeometryTransactionDecision(False,"target_snapshot_missing")
    if not rollback_fully_reversible:
        return GeometryTransactionDecision(False,"rollback_not_fully_reversible")
    return GeometryTransactionDecision(True,"accepted")
