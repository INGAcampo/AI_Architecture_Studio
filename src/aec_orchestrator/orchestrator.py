from __future__ import annotations

from dataclasses import dataclass

from .contracts import AecApplication, JobEnvelope, JobResult, JobState
from .worker import DeterministicWorker


@dataclass(frozen=True)
class DispatchRecord:
    job_id: str
    application: AecApplication
    state: JobState


class AecOrchestrator:
    def __init__(self) -> None:
        self._workers: dict[AecApplication, DeterministicWorker] = {}
        self._records: list[DispatchRecord] = []

    def register_worker(self, worker: DeterministicWorker) -> None:
        if worker.application in self._workers:
            raise ValueError(
                f"worker already registered for {worker.application.value}"
            )
        self._workers[worker.application] = worker

    def dispatch(self, job: JobEnvelope) -> JobResult:
        job.validate()
        worker = self._workers.get(job.application)

        if worker is None:
            result = JobResult(
                job_id=job.job_id,
                application=job.application,
                operation=job.command.operation,
                state=JobState.FAILED,
                error="no worker registered for requested application",
            )
        else:
            result = worker.execute(job)

        self._records.append(
            DispatchRecord(
                job_id=job.job_id,
                application=job.application,
                state=result.state,
            )
        )
        return result

    @property
    def records(self) -> tuple[DispatchRecord, ...]:
        return tuple(self._records)
