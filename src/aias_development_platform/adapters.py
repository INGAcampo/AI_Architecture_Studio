"""Adapters that preserve existing AEPS engines behind one platform boundary."""
from __future__ import annotations
from pathlib import Path
from typing import Callable


def default_runners() -> dict[str, Callable[[Path,Path],object]]:
    """Build lazily imported runners for the installed V3, V4 and V5 engines."""
    def v3(spec,workspace):
        from aias_aeps_automation_v3.orchestrator import AutomationOrchestrator
        return AutomationOrchestrator().build(spec,workspace)
    def v4(spec,workspace):
        from aias_aeps_advanced_v4.orchestrator import AdvancedProductionOrchestrator
        return AdvancedProductionOrchestrator().build(spec,workspace)
    def v5(spec,workspace):
        from aias_aeps_autonomous_v5.orchestrator import AutonomousEngineeringOrchestrator
        return AutonomousEngineeringOrchestrator().build(spec,workspace)
    return {"v3":v3,"v4":v4,"v5":v5}


def normalize(job_id: str, engine: str, raw: object) -> tuple[bool,tuple[str,...],dict]:
    """Normalize dictionaries, V3 contexts and V5 results without data loss."""
    if isinstance(raw,dict):
        certified=bool(raw.get("certified"));artifacts=tuple(str(x) for x in raw.get("artifacts",[]) if x);evidence=dict(raw)
    elif hasattr(raw,"reports"):
        reports=dict(raw.reports);certified=bool(getattr(raw,"certified",reports.get("certified",False)));artifacts=tuple(str(getattr(x,"path",x)) for x in getattr(raw,"artifacts",[]));evidence=reports
    else: raise TypeError("unsupported_engine_result")
    return certified,artifacts,evidence
