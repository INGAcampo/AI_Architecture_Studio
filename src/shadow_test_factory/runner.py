from __future__ import annotations

from .contracts import EvidenceRecord, GoldenCase, GoldenCaseResult, TestPolicy


class GoldenCaseRunner:
    def __init__(self, policy: TestPolicy | None = None) -> None:
        self.policy = policy or TestPolicy()

    def run(self, suite_id: str, cases: list[GoldenCase]) -> EvidenceRecord:
        if not suite_id.strip():
            raise ValueError("suite_id must not be empty")

        results = []

        for case in cases:
            case.validate()

            try:
                actual = case.execute()
                passed = actual == case.expected
                error = None
            except Exception as exc:
                actual = None
                passed = False
                error = f"{type(exc).__name__}: {exc}"

            results.append(
                GoldenCaseResult(
                    case_id=case.case_id,
                    passed=passed,
                    actual=actual,
                    expected=case.expected,
                    error=error,
                )
            )

            if self.policy.fail_fast and not passed:
                break

        record = EvidenceRecord(
            suite_id=suite_id,
            results=tuple(results),
            metadata={
                "policy": {
                    "fail_fast": self.policy.fail_fast,
                    "require_all_pass": self.policy.require_all_pass,
                    "allow_skips": self.policy.allow_skips,
                }
            },
        )

        return record
