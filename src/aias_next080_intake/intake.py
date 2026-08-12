"""Validation-only intake contract for externally supplied evidence."""
from __future__ import annotations
from typing import Any, Mapping

class EvidenceIntake:
    REQUIRED = ("id", "source", "sha256")
    def validate(self, record: Mapping[str, Any]) -> dict[str, Any]:
        missing = [field for field in self.REQUIRED if not record.get(field)]
        return {"status": "ACCEPTED_FOR_REVIEW" if not missing else "INVALID_INTAKE", "missing": missing, "approved": False}
