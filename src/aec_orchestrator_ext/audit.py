from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditEvent:
    sequence: int
    job_id: str
    event_type: str
    detail: str


class AuditTrail:
    def __init__(self) -> None:
        self._events = []

    def append(self, job_id: str, event_type: str, detail: str = "") -> AuditEvent:
        if not job_id.strip():
            raise ValueError("job_id must not be empty")
        if not event_type.strip():
            raise ValueError("event_type must not be empty")

        event = AuditEvent(
            sequence=len(self._events) + 1,
            job_id=job_id,
            event_type=event_type,
            detail=detail,
        )
        self._events.append(event)
        return event

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)
