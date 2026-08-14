from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AecApplication(str, Enum):
    AUTOCAD = "AUTOCAD"
    REVIT = "REVIT"
    ETABS = "ETABS"
    SAP2000 = "SAP2000"
    SAFE = "SAFE"
    GEO5 = "GEO5"


class JobState(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    DISPATCHED = "DISPATCHED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class WorkerCapability:
    application: AecApplication
    operations: tuple[str, ...]
    protocol_version: str = "1.0"

    def supports(self, operation: str) -> bool:
        return operation in self.operations


@dataclass(frozen=True)
class JobCommand:
    operation: str
    payload: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.operation.strip():
            raise ValueError("operation must not be empty")


@dataclass(frozen=True)
class JobEnvelope:
    job_id: str
    application: AecApplication
    command: JobCommand
    idempotency_key: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.job_id.strip():
            raise ValueError("job_id must not be empty")
        if not self.idempotency_key.strip():
            raise ValueError("idempotency_key must not be empty")
        self.command.validate()


@dataclass(frozen=True)
class JobResult:
    job_id: str
    application: AecApplication
    operation: str
    state: JobState
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
