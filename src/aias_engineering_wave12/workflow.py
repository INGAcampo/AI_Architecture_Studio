"""Professional foundation workflow joining calculations, checks and evidence."""
from __future__ import annotations
from pathlib import Path
from aias_foundation_calcs.orchestrator import FoundationCalculationOrchestrator
from aias_foundation_code_checks.orchestrator import FoundationCodeCheckOrchestrator
from .evidence import EngineeringEvidenceLedger

class FoundationProfessionalWorkflow:
    """Execute validated reference calculation and code-check engines as one file."""
    def execute(self,workspace:Path)->dict:
        """Produce both engine releases and chain their evidence for professional review."""
        calculation=FoundationCalculationOrchestrator().execute(workspace/"calculation");checks=FoundationCodeCheckOrchestrator().execute(workspace/"code_checks");ledger=EngineeringEvidenceLedger(workspace/"engineering_evidence.json");ledger.append("EVD-FOUND-CALC","CALCULATION","ECP-000001B",calculation);ledger.append("EVD-FOUND-CHECK","CODE_CHECK","ECP-000001C",checks)
        return {"validated":calculation["validated"] and checks["validated"] and ledger.verify()["valid"],"calculation":calculation,"code_checks":checks,"ledger":ledger.verify(),"professional_review_required":True}
