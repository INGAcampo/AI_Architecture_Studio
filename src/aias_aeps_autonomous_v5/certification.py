"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from pathlib import Path
import hashlib, json

class AutonomousCertificationEngine:
    """Execute the public AutonomousCertificationEngine operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def certify(self, specification: dict, test_report: dict, security_issues: list[str], workspace: Path) -> dict:
        """Execute the public AutonomousCertificationEngine.certify operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        issues = []
        if not specification.get("requirements"):
            issues.append("missing_requirements")
        if not specification.get("architecture_refs"):
            issues.append("missing_architecture_refs")
        if not specification.get("adr_refs"):
            issues.append("missing_adr_refs")
        if not test_report.get("passed"):
            issues.append("tests_failed")
        issues.extend(security_issues)

        certified = not issues
        out = workspace / "certification"
        out.mkdir(parents=True, exist_ok=True)
        path = out / "autonomous_certificate.json"
        path.write_text(json.dumps({
            "certified": certified,
            "issues": issues,
            "specification_id": specification.get("id"),
        }, indent=2), encoding="utf-8")
        return {
            "certified": certified,
            "issues": issues,
            "certificate": str(path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
