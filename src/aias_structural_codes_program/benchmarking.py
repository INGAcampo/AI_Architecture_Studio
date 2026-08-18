"""Independent, integrity-protected benchmark validation for structural results."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math


@dataclass(frozen=True, slots=True)
class BenchmarkValue:
    """One expected independent result and its admissible comparison tolerance."""

    metric_id: str
    expected: float
    absolute_tolerance: float
    relative_tolerance: float
    units: str

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.metric_id or not self.units:
            issues.append("benchmark_metric_identity_incomplete")
        if not all(math.isfinite(x) for x in (self.expected, self.absolute_tolerance, self.relative_tolerance)):
            issues.append(f"{self.metric_id}:non_finite_value")
        if self.absolute_tolerance < 0 or self.relative_tolerance < 0:
            issues.append(f"{self.metric_id}:negative_tolerance")
        return issues


@dataclass(frozen=True, slots=True)
class IndependentBenchmark:
    """Externally derived benchmark with provenance and review evidence."""

    benchmark_id: str
    version: str
    domain: str
    source_organization: str
    source_locator: str
    method: str
    reviewer: str
    review_status: str
    values: tuple[BenchmarkValue, ...]
    independent_from_aias: bool

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not all((self.benchmark_id, self.version, self.domain, self.source_organization, self.source_locator, self.method)):
            issues.append("benchmark_provenance_incomplete")
        if not self.independent_from_aias:
            issues.append("independence_not_established")
        if self.review_status not in {"ACCEPTED", "REJECTED", "PENDING"}:
            issues.append("invalid_review_status")
        if self.review_status == "ACCEPTED" and not self.reviewer:
            issues.append("accepted_review_requires_reviewer")
        ids = [value.metric_id for value in self.values]
        if not ids:
            issues.append("benchmark_values_required")
        if len(ids) != len(set(ids)):
            issues.append("duplicate_benchmark_metric")
        for value in self.values:
            issues.extend(value.validate())
        return issues

    def integrity_sha256(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class BenchmarkComparison:
    metric_id: str
    expected: float
    actual: float | None
    difference: float | None
    allowed_difference: float
    units: str
    status: str


@dataclass(frozen=True, slots=True)
class BenchmarkValidationResult:
    benchmark_id: str
    benchmark_sha256: str
    comparisons: tuple[BenchmarkComparison, ...]
    issues: tuple[str, ...]
    status: str
    professional_release_authorized: bool = False

    def evidence_sha256(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class IndependentBenchmarkValidator:
    """Compare AIAS outputs with independent expected values and fail closed."""

    def validate(self, benchmark: IndependentBenchmark, actual: dict[str, float]) -> BenchmarkValidationResult:
        issues = benchmark.validate()
        expected_ids = {value.metric_id for value in benchmark.values}
        unexpected = sorted(set(actual) - expected_ids)
        if unexpected:
            issues.append(f"unexpected_metrics:{unexpected}")
        comparisons: list[BenchmarkComparison] = []
        for expected in benchmark.values:
            measured = actual.get(expected.metric_id)
            allowed = max(expected.absolute_tolerance, abs(expected.expected) * expected.relative_tolerance)
            if measured is None:
                comparisons.append(BenchmarkComparison(expected.metric_id, expected.expected, None, None, allowed, expected.units, "MISSING"))
                issues.append(f"{expected.metric_id}:actual_value_missing")
                continue
            if not math.isfinite(measured):
                comparisons.append(BenchmarkComparison(expected.metric_id, expected.expected, measured, None, allowed, expected.units, "INVALID"))
                issues.append(f"{expected.metric_id}:actual_value_non_finite")
                continue
            difference = abs(measured - expected.expected)
            status = "PASS" if difference <= allowed else "FAIL"
            comparisons.append(BenchmarkComparison(expected.metric_id, expected.expected, measured, difference, allowed, expected.units, status))
            if status == "FAIL":
                issues.append(f"{expected.metric_id}:outside_tolerance")
        passed = not issues and benchmark.review_status == "ACCEPTED" and all(row.status == "PASS" for row in comparisons)
        return BenchmarkValidationResult(
            benchmark.benchmark_id,
            benchmark.integrity_sha256(),
            tuple(comparisons),
            tuple(issues),
            "VALIDATED_INDEPENDENT" if passed else "REJECTED",
            False,
        )
