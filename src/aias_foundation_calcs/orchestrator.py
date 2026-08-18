"""Reference execution, technical-file production and checksum release orchestration."""
from pathlib import Path
import json,zipfile,hashlib
from .reference_cases import reference_input,run_reference_cases
from .engine import FoundationCalculationEngine
from .reporting import CalculationReportWriter

class FoundationCalculationOrchestrator:
    """Execute the validated reference footing and package its calculation evidence."""
    def execute(self, workspace: Path) -> dict:
        """Execute the reference footing and package calculation and QA evidence."""
        workspace.mkdir(parents=True,exist_ok=True)
        data=reference_input()
        package=FoundationCalculationEngine().calculate(data)
        CalculationReportWriter().write_json(data,package,workspace/"technical_file"/"foundation_calculation.json")
        cases=run_reference_cases()
        qa=workspace/"qa"/"reference_cases.json"; qa.parent.mkdir(parents=True,exist_ok=True)
        qa.write_text(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2),encoding="utf-8")
        if not all(c["passed"] for c in cases):
            raise RuntimeError("reference_cases_failed")
        rel=workspace/"release"; rel.mkdir(exist_ok=True)
        archive=rel/"ECP-000001B_FOUNDATION_CALCULATION_ENGINE_1.0.0.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
            for p in workspace.rglob("*"):
                if p.is_file() and rel not in p.parents:
                    z.write(p,p.relative_to(workspace))
        return {
            "validated":True,
            "reference_cases":len(cases),
            "combinations":len(package.results),
            "governing":package.governing,
            "archive":str(archive),
            "sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
        }
