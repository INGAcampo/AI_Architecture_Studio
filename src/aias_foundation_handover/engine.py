"""Application service for verified foundation lifecycle handover."""
from __future__ import annotations
from pathlib import Path
from .acceptance import evaluate
from .custody import custody_event, verify_transmittal
from .kpi import calculate
from .maturity import assess

class FoundationHandoverEngine:
    """Build an accepted, traceable lifecycle dossier from an ECP-E transmittal."""
    def build(self, transmittal: Path, actor: str = "AIAS", baseline_hours: float = 4.0, actual_hours: float = 1.8) -> dict:
        """Validate a transmittal and assemble custody, KPI and maturity evidence."""
        verification = verify_transmittal(transmittal)
        acceptance = evaluate(verification)
        if not acceptance["lifecycle_accepted"]: raise ValueError("handover_acceptance_failed")
        kpi = calculate(baseline_hours, actual_hours, min(actual_hours, 1.2), 4, 6)
        maturity = assess({"repeatable_delivery": True, "traceability": verification["valid"], "automated_quality_gates": True, "measured_acceleration": kpi.meets_45_percent_target, "continuous_improvement_loop": True})
        event = custody_event(verification["package_id"], actor)
        findings = [{"id":"FND-KPI-001","severity":"INFO","status":"OPEN","message":kpi.warning}] if kpi.classification != "AUDITED_PRODUCTION_MEASUREMENT" else []
        return {"handover_id": f"HANDOVER-{verification['package_id']}", "source_package": verification["package_id"], "verification": {k:v for k,v in verification.items() if k != "manifest"}, "acceptance": acceptance, "custody": [event.to_dict()], "kpi": kpi.to_dict(), "maturity": maturity, "findings": findings, "legal_status": verification["manifest"]["delivery_status"]}
