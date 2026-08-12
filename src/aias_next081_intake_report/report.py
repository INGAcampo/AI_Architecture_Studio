"""Stable report envelope for evidence intake validation."""
from __future__ import annotations
from typing import Any, Mapping
from aias_next080_intake import EvidenceIntake

class IntakeReport:
    def generate(self, record: Mapping[str, Any]) -> dict[str, Any]:
        validation = EvidenceIntake().validate(record)
        return {"report": "AIAS-NEXT-081", "validation": validation, "approved": False}
