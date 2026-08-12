"""Evidence-based readiness assessment for external certification objectives."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .registry import official_frameworks


class CertificationReadinessAssessor:
    """Assess internal readiness while reserving all certification decisions to external authorities."""

    REQUIRED_EVIDENCE = {
        "CMMI-DEV-V3-ML5": ("engineering/aias/level5/LEVEL5_ASSURANCE_POLICY.json", "engineering/aias/roadmap/LEVEL5_EVIDENCE_CAMPAIGN.json"),
        "CMMI-AIM": ("src/aias_engineering_intelligence", "src/aias_enterprise_offices/ai_office.py"),
        "ISO-9001": ("engineering/aeps/05_SDD/ASDD-000002-formal-sdd.yaml", "src/aias_governance_assurance"),
        "ISO-IEC-27001": ("src/aias_security_recovery", "engineering/security_recovery001/compliance/QUALITY_GATES.json"),
        "ISO-IEC-42001": ("src/aias_engineering_intelligence", "src/aias_virtual_organization"),
        "ISO-22301": ("src/aias_security_recovery", "src/aias_engineering_os"),
    }

    def assess(self, root: Path) -> dict:
        """Report evidence availability without claiming conformity or certification."""
        rows = []
        for framework in official_frameworks():
            required = self.REQUIRED_EVIDENCE[framework["id"]]
            evidence = [{"path": path, "exists": (root / path).exists()} for path in required]
            rows.append({
                "framework_id": framework["id"],
                "role": framework["role"],
                "internal_evidence_available": all(item["exists"] for item in evidence),
                "evidence": evidence,
                "externally_certified_or_rated": False,
                "external_assessment_required": True,
            })
        payload = {"assessment_id": "CERT-READINESS-AIAS", "classification": "INTERNAL_READINESS_NOT_CERTIFICATION", "frameworks": rows, "certification_claim_permitted": False}
        payload["evidence_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return payload
