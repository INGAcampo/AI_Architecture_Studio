"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from .reference_cases import reference_package, run_reference_cases
from .reporting import DocumentationWriter


class FoundationDocumentationOrchestrator:
    """Execute the public FoundationDocumentationOrchestrator operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    VERSION = "1.0.0"

    def execute(self, workspace: Path) -> dict:
        """Execute execute for foundation drawings, schedules and technical documentation with validated state transitions."""
        workspace.mkdir(parents=True, exist_ok=True)
        package = reference_package(workspace)
        files = DocumentationWriter().write(package, workspace)
        cases = run_reference_cases(workspace / "reference_validation")
        qa = workspace / "qa" / "reference_cases.json"
        qa.parent.mkdir(parents=True, exist_ok=True)
        qa.write_text(json.dumps({"passed": all(case["passed"] for case in cases), "cases": cases}, indent=2) + "\n", encoding="utf-8")
        if not all(case["passed"] for case in cases):
            raise RuntimeError("reference_cases_failed")
        release = workspace / "release"
        release.mkdir(exist_ok=True)
        archive = release / f"ECP-000001D_FOUNDATION_DETAILING_DOCUMENTATION_{self.VERSION}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for path in workspace.rglob("*"):
                if path.is_file() and release not in path.parents:
                    bundle.write(path, path.relative_to(workspace))
        return {"validated": True, "reference_cases": len(cases), "drawings": len(package.drawing_manifest), "bar_marks": len(package.bar_schedule), "legal_status": package.qa["legal_status"], "files": files, "archive": str(archive), "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
