"""Executable complete-vertical delivery gate for every new AIAS capability."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VerticalGateResult:
    """Report complete evidence coverage without inflating capability claims."""

    passed: bool
    required: tuple[str, ...]
    present: tuple[str, ...]
    missing: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"passed": self.passed, "required": list(self.required), "present": list(self.present), "missing": list(self.missing), "warnings": list(self.warnings)}


class CompleteVerticalGate:
    """Enforce specification-to-consumer delivery before validation and release."""

    BASE_REQUIRED = (
        "specification",
        "architecture",
        "implementation",
        "consumer",
        "tests",
        "documentation",
        "installer",
        "traceability",
        "reference_case",
    )

    def evaluate(self, evidence: dict, *, user_facing: bool, regulated: bool) -> VerticalGateResult:
        """Return a deterministic gap report for the declared capability context."""
        if not isinstance(evidence, dict):
            evidence = {}
        required = list(self.BASE_REQUIRED)
        if user_facing:
            required.extend(("interface", "rendered_review"))
        if regulated:
            required.extend(("normative_boundary", "professional_review_boundary"))
        present = tuple(key for key in required if self._substantive(evidence.get(key)))
        missing = tuple(key for key in required if key not in present)
        warnings = []
        consumer = str(evidence.get("consumer", "")).strip().upper()
        if consumer in {"NONE", "N/A", "FUTURE", "PLANNED"}:
            warnings.append("consumer_is_not_materialized")
        reference = str(evidence.get("reference_case", "")).strip().upper()
        if reference in {"NONE", "N/A", "FUTURE", "PLANNED"}:
            warnings.append("reference_case_is_not_materialized")
        passed = not missing and not warnings
        return VerticalGateResult(passed, tuple(required), present, missing, tuple(warnings))

    def require(self, evidence: dict, *, user_facing: bool, regulated: bool) -> VerticalGateResult:
        """Raise a machine-readable error when any vertical evidence is absent."""
        result = self.evaluate(evidence, user_facing=user_facing, regulated=regulated)
        if not result.passed:
            gaps = (*result.missing, *result.warnings)
            raise ValueError("incomplete_vertical_delivery:" + ",".join(gaps))
        return result

    @staticmethod
    def _substantive(value) -> bool:
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (tuple, list, dict, set)):
            return bool(value)
        return value is True
