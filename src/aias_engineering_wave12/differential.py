"""Unit-aware differential validation against governed reference results."""
from __future__ import annotations
class DifferentialValidator:
    """Compare exact result keys with absolute and relative engineering tolerances."""
    def compare(self,baseline:dict,candidate:dict,absolute_tolerance:float,relative_tolerance:float)->dict:
        """Return field-level differences and reject missing provenance or unit mismatch."""
        if not baseline.get("provenance") or not candidate.get("provenance"):raise ValueError("missing_result_provenance")
        if baseline.get("units")!=candidate.get("units"):raise ValueError("unit_mismatch")
        if set(baseline.get("values",{}))!=set(candidate.get("values",{})):raise ValueError("result_contract_mismatch")
        rows=[]
        for key,expected in baseline["values"].items():
            actual=candidate["values"][key];delta=abs(actual-expected);limit=max(absolute_tolerance,relative_tolerance*abs(expected));rows.append({"field":key,"expected":expected,"actual":actual,"delta":delta,"limit":limit,"passed":delta<=limit})
        return {"passed":all(r["passed"] for r in rows),"differences":rows,"baseline_provenance":baseline["provenance"],"candidate_provenance":candidate["provenance"]}
