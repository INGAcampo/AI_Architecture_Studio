"""Immutable licensed project-reference case library."""
from __future__ import annotations
import hashlib,json
class ProjectReferenceLibrary:
    """Register attributable non-sensitive project cases for repeatable validation."""
    def __init__(self):self.cases={}
    def register(self,case:dict)->dict:
        """Register a complete anonymized reference case and reject identity drift."""
        required={"case_id","domain","version","license_id","provenance","inputs","expected","anonymized"}
        if required-set(case) or not case["anonymized"]:raise ValueError("invalid_reference_case")
        canonical=json.dumps(case,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode();row={**case,"case_sha256":hashlib.sha256(canonical).hexdigest()};old=self.cases.get(case["case_id"])
        if old and old!=row:raise ValueError("reference_case_conflict")
        self.cases[case["case_id"]]=row;return row
