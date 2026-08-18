"""Quality evidence, traceability and checksum release for the calculation framework."""
from __future__ import annotations
from pathlib import Path
import json, hashlib, zipfile, time
from .reference_cases import run_reference_cases

class ECFOrchestrator:
    """Validate reference mathematics and package its professional-use limitations."""
    def validate_and_release(self, workspace: Path) -> dict:
        """Run mathematical reference cases and package traceable release evidence."""
        workspace.mkdir(parents=True, exist_ok=True)
        cases = run_reference_cases()
        passed = all(c["passed"] for c in cases)
        qa_dir = workspace / "qa"
        qa_dir.mkdir(parents=True, exist_ok=True)
        qa = qa_dir / "reference_cases.json"
        qa.write_text(json.dumps({"passed":passed,"cases":cases}, indent=2), encoding="utf-8")
        if not passed:
            raise RuntimeError("reference_cases_failed")

        trace = workspace / "traceability" / "AMP-010A.json"
        trace.parent.mkdir(parents=True, exist_ok=True)
        trace.write_text(json.dumps({
            "program":"AMP-010A",
            "sdd":"ASDD-000010",
            "aeks_integration":"CKU-000001",
            "reference_cases":[c["id"] for c in cases],
            "human_review_required_for_professional_use":True,
        }, indent=2), encoding="utf-8")

        technical = workspace / "technical_file" / "technical_file.json"
        technical.parent.mkdir(parents=True, exist_ok=True)
        technical.write_text(json.dumps({
            "title":"AIAS Enterprise Calculation Framework - Mathematical Kernel",
            "status":"READY_FOR_ENGINEERING_REVIEW",
            "scope":"Generic mathematical infrastructure; not a code-specific engineering design.",
            "limitations":["Professional validation required before use in regulated engineering deliverables."],
        }, indent=2), encoding="utf-8")

        release = workspace / "release"
        release.mkdir(parents=True, exist_ok=True)
        archive = release / "AMP-010A_ECF_1.0.0.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for path in workspace.rglob("*"):
                if path.is_file() and release not in path.parents:
                    z.write(path, path.relative_to(workspace))
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        return {
            "validated":True,
            "reference_cases":len(cases),
            "archive":str(archive),
            "sha256":digest,
            "workspace":str(workspace),
        }
