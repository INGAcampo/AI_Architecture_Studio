"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from pathlib import Path
import json, hashlib
from .models import CertificationBundle
from .constitution import FullConstitutionValidator

class AdvancedCertificationEngine:
    """Execute the public AdvancedCertificationEngine operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    def certify(self, context: dict, output_dir: Path) -> CertificationBundle:
        """Execute the public AdvancedCertificationEngine.certify operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        checks = FullConstitutionValidator().validate(context)
        issues = [c.check_id for c in checks if not c.passed]
        output_dir.mkdir(parents=True, exist_ok=True)
        report = {
            "certified": not issues,
            "checks": [
                {"id": c.check_id, "passed": c.passed, "message": c.message}
                for c in checks
            ],
            "issues": issues,
        }
        report_path = output_dir / "constitutional_certification.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
        return CertificationBundle(
            certified=not issues,
            issues=issues,
            reports={"constitutional": report, "sha256": digest},
            output_dir=output_dir,
        )
