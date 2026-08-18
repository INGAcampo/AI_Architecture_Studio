from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .contracts import (
    AecApplication,
    JobEnvelope,
    JobResult,
    JobState,
    WorkerCapability,
)


Handler = Callable[[dict[str, Any]], dict[str, Any]]


class DeterministicWorker:
    """Vendor-neutral deterministic worker used to validate orchestration contracts.

    Vendor-specific runtimes are deliberately not invoked in AEC-ORCHESTRATOR-001.
    """

    def __init__(
        self,
        capability: WorkerCapability,
        handlers: dict[str, Handler] | None = None,
    ) -> None:
        self.capability = capability
        self._handlers = dict(handlers or {})
        self._completed_by_idempotency_key: dict[str, JobResult] = {}

    @property
    def application(self) -> AecApplication:
        return self.capability.application

    def register(self, operation: str, handler: Handler) -> None:
        if not operation.strip():
            raise ValueError("operation must not be empty")
        self._handlers[operation] = handler

    def execute(self, job: JobEnvelope) -> JobResult:
        job.validate()

        if job.application != self.application:
            return JobResult(
                job_id=job.job_id,
                application=job.application,
                operation=job.command.operation,
                state=JobState.FAILED,
                error="worker application mismatch",
            )

        cached = self._completed_by_idempotency_key.get(job.idempotency_key)
        if cached is not None:
            return cached

        operation = job.command.operation

        if not self.capability.supports(operation):
            return JobResult(
                job_id=job.job_id,
                application=job.application,
                operation=operation,
                state=JobState.FAILED,
                error="operation is not declared by worker capability",
            )

        handler = self._handlers.get(operation)
        if handler is None:
            return JobResult(
                job_id=job.job_id,
                application=job.application,
                operation=operation,
                state=JobState.FAILED,
                error="no deterministic handler is registered",
            )

        try:
            output = dict(handler(dict(job.command.payload)))
        except Exception as exc:
            return JobResult(
                job_id=job.job_id,
                application=job.application,
                operation=operation,
                state=JobState.FAILED,
                error=str(exc),
            )

        result = JobResult(
            job_id=job.job_id,
            application=job.application,
            operation=operation,
            state=JobState.SUCCEEDED,
            output=output,
            error=None,
        )
        self._completed_by_idempotency_key[job.idempotency_key] = result
        return result
