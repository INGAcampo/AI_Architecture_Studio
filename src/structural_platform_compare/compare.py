from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ComparisonResult:
    baseline:float
    candidate:float
    absolute_delta:float
    relative_delta:float
    within_tolerance:bool

def compare_scalar_results(baseline:float,candidate:float,abs_tol:float=1e-9,rel_tol:float=1e-6)->ComparisonResult:
    if abs_tol<0 or rel_tol<0:
        raise ValueError("tolerances must be nonnegative")
    delta=abs(candidate-baseline)
    denom=max(abs(baseline),abs(candidate),1e-30)
    rel=delta/denom
    return ComparisonResult(float(baseline),float(candidate),delta,rel,delta<=abs_tol or rel<=rel_tol)
