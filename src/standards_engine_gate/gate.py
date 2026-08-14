from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StandardsGateDecision:
    accepted:bool
    reason:str

def evaluate_standards_gate(*,provenance_valid:bool,applicable:bool,source_verified:bool)->StandardsGateDecision:
    if not provenance_valid:
        return StandardsGateDecision(False,"invalid_provenance")
    if not source_verified:
        return StandardsGateDecision(False,"source_not_verified")
    if not applicable:
        return StandardsGateDecision(False,"not_applicable")
    return StandardsGateDecision(True,"accepted")
