"""Identity, completeness, provenance and lifecycle validation for knowledge units."""
from __future__ import annotations
import re
from .models import KnowledgeUnit

EKU_ID = re.compile(r"^EKU-\d{6}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
VALID_STATUS = {"DRAFT", "REVIEW", "APPROVED", "RETIRED"}

class KnowledgeValidator:
    """Collect structural and governance violations before knowledge admission."""
    def validate(self, unit: KnowledgeUnit) -> list[str]:
        """Collect identity, version, source, applicability and relationship issues."""
        issues: list[str] = []
        if not EKU_ID.fullmatch(unit.eku_id):
            issues.append("invalid_eku_id")
        if not SEMVER.fullmatch(unit.version):
            issues.append("invalid_semver")
        if unit.status not in VALID_STATUS:
            issues.append("invalid_status")
        if not unit.title.strip():
            issues.append("missing_title")
        if not unit.discipline.strip():
            issues.append("missing_discipline")
        if not unit.category.strip():
            issues.append("missing_category")
        if not unit.source.strip():
            issues.append("missing_source")
        if not unit.traceability:
            issues.append("missing_traceability")
        if not unit.deliverables:
            issues.append("missing_deliverables")
        return issues
