"""Permanent reference cases for the ECP-000001F capability."""
from pathlib import Path
from .orchestrator import FoundationHandoverOrchestrator

def run_reference_cases(workspace: Path) -> list[dict]:
    """Execute reference handover cases and return machine-readable results."""
    result=FoundationHandoverOrchestrator().execute(workspace)
    return [
        {"id":"FDH-000001","passed":result["validated"]},
        {"id":"FDH-000002","passed":result["maturity_level"]==5},
        {"id":"FDH-000003","passed":result["level_5_evidence_complete"]},
        {"id":"FDH-000004","passed":result["kpi_time_reduction"]>=.45},
        {"id":"FDH-000005","passed":result["kpi_classification"]=="REFERENCE_ENGINEERING_ESTIMATE"},
        {"id":"FDH-000006","passed":len(result["sha256"])==64},
    ]
