from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    retryable_errors: tuple[str, ...] = (
        "timeout",
        "runtime_unavailable",
        "transient_external_error",
    )

    def validate(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least one")


@dataclass(frozen=True)
class RetryDecision:
    should_retry: bool
    next_attempt: int | None
    reason: str


def evaluate_retry(
    *,
    current_attempt: int,
    error_code: str,
    policy: RetryPolicy,
) -> RetryDecision:
    policy.validate()

    if current_attempt < 1:
        raise ValueError("current_attempt must be at least one")

    if current_attempt >= policy.max_attempts:
        return RetryDecision(False, None, "attempt_limit_reached")

    if error_code not in policy.retryable_errors:
        return RetryDecision(False, None, "error_is_not_retryable")

    return RetryDecision(True, current_attempt + 1, "retryable_error")
