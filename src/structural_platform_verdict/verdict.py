from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StructuralVerdict:
    accepted:bool
    reason:str
    evidence_sha256:str

def make_structural_verdict(bundle,evidence_sha256:str)->StructuralVerdict:
    if len(evidence_sha256)!=64:
        raise ValueError("evidence_sha256 must be SHA256")
    if bundle.missing_count:
        return StructuralVerdict(False,"missing_results",evidence_sha256)
    if bundle.mismatch_count:
        return StructuralVerdict(False,"comparison_mismatch",evidence_sha256)
    if not bundle.comparison_passed:
        return StructuralVerdict(False,"comparison_not_passed",evidence_sha256)
    return StructuralVerdict(True,"accepted",evidence_sha256)
