"""Geometry reference validation, traceability and checksum release orchestration."""
from __future__ import annotations
from pathlib import Path
import json,hashlib,zipfile
from .reference_cases import run_reference_cases

class GeometryKernelOrchestrator:
    """Execute kernel acceptance cases and package reusable geometry evidence."""
    def validate_and_release(self, workspace: Path):
        """Run reference cases and write traceable checksum-protected release evidence."""
        workspace.mkdir(parents=True,exist_ok=True)
        cases=run_reference_cases()
        passed=all(c["passed"] for c in cases)
        qa=workspace/"qa"/"geometry_reference_cases.json"
        qa.parent.mkdir(parents=True,exist_ok=True)
        qa.write_text(json.dumps({"passed":passed,"cases":cases},indent=2),encoding="utf-8")
        if not passed:
            raise RuntimeError("geometry_reference_cases_failed")
        tech=workspace/"technical_file"/"technical_file.json"
        tech.parent.mkdir(parents=True,exist_ok=True)
        tech.write_text(json.dumps({
            "program":"AMP-010B",
            "status":"READY_FOR_INTEGRATION",
            "scope":"Domain-independent 2D geometry kernel",
            "consumers":["ECF","CAD","BIM","ECP Foundations"],
            "human_review_required_for_regulated_deliverables":True
        },indent=2),encoding="utf-8")
        rel=workspace/"release"
        rel.mkdir(parents=True,exist_ok=True)
        archive=rel/"AMP-010B_GEOMETRY_KERNEL_1.0.0.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
            for p in workspace.rglob("*"):
                if p.is_file() and rel not in p.parents:
                    z.write(p,p.relative_to(workspace))
        return {
            "validated":True,
            "reference_cases":len(cases),
            "archive":str(archive),
            "sha256":hashlib.sha256(archive.read_bytes()).hexdigest()
        }
