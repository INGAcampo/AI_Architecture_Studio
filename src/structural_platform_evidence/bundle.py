from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class StructuralEvidenceBundle:
    model_id:str
    baseline_engine:str
    candidate_engine:str
    comparison_passed:bool
    mismatch_count:int
    missing_count:int

    def validate(self):
        if not self.model_id.strip():
            raise ValueError("model_id must not be empty")
        if not self.baseline_engine.strip() or not self.candidate_engine.strip():
            raise ValueError("engine names must not be empty")
        if self.mismatch_count<0 or self.missing_count<0:
            raise ValueError("counts must be nonnegative")

def evidence_bundle_sha256(bundle:StructuralEvidenceBundle)->str:
    bundle.validate()
    payload={
        "baseline_engine":bundle.baseline_engine,
        "candidate_engine":bundle.candidate_engine,
        "comparison_passed":bool(bundle.comparison_passed),
        "mismatch_count":int(bundle.mismatch_count),
        "missing_count":int(bundle.missing_count),
        "model_id":bundle.model_id,
    }
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
    return hashlib.sha256(raw).hexdigest()
