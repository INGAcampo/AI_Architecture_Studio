from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
class WorkerState(str, Enum):
    DECLARED="declared"; OPEN="open"; READY="ready"; CLOSED="closed"; UNAVAILABLE="unavailable"
@dataclass(frozen=True, slots=True)
class WorkerContract:
    worker_id: str
    product: str
    capabilities: tuple[str, ...]
    runtime_required: bool = True
    license_verified: bool = False
    state: WorkerState = WorkerState.DECLARED
@dataclass(slots=True)
class WorkerRegistry:
    workers: dict[str, WorkerContract] = field(default_factory=dict)
    def register(self, worker: WorkerContract) -> None:
        if not worker.worker_id.strip(): raise ValueError("worker_id cannot be empty")
        if worker.worker_id in self.workers: raise ValueError("duplicate_worker:" + worker.worker_id)
        self.workers[worker.worker_id] = worker
    def open(self, worker_id: str) -> WorkerContract:
        worker=self._get(worker_id)
        if worker.runtime_required and not worker.license_verified:
            return WorkerContract(worker.worker_id,worker.product,worker.capabilities,worker.runtime_required,worker.license_verified,WorkerState.UNAVAILABLE)
        return WorkerContract(worker.worker_id,worker.product,worker.capabilities,worker.runtime_required,worker.license_verified,WorkerState.OPEN)
    def _get(self, worker_id: str) -> WorkerContract:
        try: return self.workers[worker_id]
        except KeyError as exc: raise KeyError("unknown_worker:" + worker_id) from exc
