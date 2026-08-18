from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationReport:
    ruleset_id: str
    passed_count: int
    failed_count: int
    warnings_count: int
    source_references: tuple[str,...]


def build_evaluation_report(ruleset_id: str, outcomes) -> EvaluationReport:
    if not ruleset_id.strip():
        raise ValueError("ruleset_id must not be empty")

    values=tuple(outcomes)
    passed=sum(1 for item in values if item.passed)
    failed=sum(1 for item in values if not item.passed)
    warnings=sum(
        1 for item in values
        if not item.passed and item.severity=="WARNING"
    )
    refs=tuple(sorted({
        item.source_reference
        for item in values
        if item.source_reference
    }))

    return EvaluationReport(
        ruleset_id=ruleset_id,
        passed_count=passed,
        failed_count=failed,
        warnings_count=warnings,
        source_references=refs,
    )
