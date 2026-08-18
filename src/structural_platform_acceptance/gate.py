from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StructuralAcceptanceDecision:
    accepted:bool
    mismatch_count:int
    missing_count:int
    reason:str

def evaluate_structural_acceptance(matrix,max_mismatches:int=0)->StructuralAcceptanceDecision:
    if max_mismatches<0:
        raise ValueError("max_mismatches must be nonnegative")

    mismatch=sum(1 for row in matrix.rows if row.status=="MISMATCH")
    missing=sum(
        1 for row in matrix.rows
        if row.status in {"MISSING_BASELINE","MISSING_CANDIDATE"}
    )

    if missing:
        return StructuralAcceptanceDecision(False,mismatch,missing,"missing_results")

    if mismatch>max_mismatches:
        return StructuralAcceptanceDecision(False,mismatch,missing,"mismatch_limit_exceeded")

    return StructuralAcceptanceDecision(True,mismatch,missing,"accepted")
