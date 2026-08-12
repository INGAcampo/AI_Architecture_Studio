from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class RegenerationStatus(str, Enum):
    CLEAN = "clean"
    DIRTY = "dirty"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass(slots=True)
class RegenerationItem:
    object_id: str
    callback: Callable[[], Any]
    priority: int = 100
    dependencies: tuple[str, ...] = ()
    status: RegenerationStatus = RegenerationStatus.DIRTY
    revision: int = 0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.object_id.strip():
            raise ValueError("object_id no puede estar vacío")
        if self.priority < 0:
            raise ValueError("priority no puede ser negativa")
        if not callable(self.callback):
            raise TypeError("callback debe ser invocable")


@dataclass(frozen=True, slots=True)
class RegenerationResult:
    object_id: str
    success: bool
    value: Any = None
    error: str | None = None
    revision: int = 0


class TransactionState(str, Enum):
    ACTIVE = "active"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"
