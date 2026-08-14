from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeltaComparison:
    baseline_failures: tuple[str, ...]
    current_failures: tuple[str, ...]
    introduced: tuple[str, ...]
    resolved: tuple[str, ...]
    unchanged: tuple[str, ...]

    @property
    def introduced_count(self) -> int:
        return len(self.introduced)


def compare_failure_sets(
    baseline_failures,
    current_failures,
) -> DeltaComparison:
    baseline = set(str(item) for item in baseline_failures)
    current = set(str(item) for item in current_failures)

    return DeltaComparison(
        baseline_failures=tuple(sorted(baseline)),
        current_failures=tuple(sorted(current)),
        introduced=tuple(sorted(current - baseline)),
        resolved=tuple(sorted(baseline - current)),
        unchanged=tuple(sorted(baseline & current)),
    )
