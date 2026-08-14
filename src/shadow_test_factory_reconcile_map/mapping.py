from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ReconciliationMapEntry:
    shadow_path:str
    canonical_path:str
    canonical_exists:bool
    classification:str

def classify_canonical_overlap(shadow_path:str,canonical_path:str,canonical_exists:bool)->ReconciliationMapEntry:
    if not shadow_path.strip() or not canonical_path.strip():
        raise ValueError("paths must not be empty")
    classification="ADDITIVE_CANDIDATE"
    if canonical_exists:
        classification="REQUIRES_CONTENT_RECONCILIATION"
    return ReconciliationMapEntry(shadow_path,canonical_path,bool(canonical_exists),classification)
