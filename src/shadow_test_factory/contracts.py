from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class GoldenCase:
    case_id: str
    description: str
    execute: Callable[[], Any]
    expected: Any

    def validate(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True)
class GoldenCaseResult:
    case_id: str
    passed: bool
    actual: Any
    expected: Any
    error: str | None = None


@dataclass(frozen=True)
class TestPolicy:
    fail_fast: bool = False
    require_all_pass: bool = True
    allow_skips: bool = True


@dataclass(frozen=True)
class EvidenceRecord:
    suite_id: str
    results: tuple[GoldenCaseResult, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def passed_count(self) -> int:
        return sum(1 for item in self.results if item.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for item in self.results if not item.passed)

    @property
    def all_passed(self) -> bool:
        return self.failed_count == 0
