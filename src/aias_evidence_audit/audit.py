from __future__ import annotations
from dataclasses import dataclass
import hashlib, json
from typing import Any
@dataclass(frozen=True, slots=True)
class AuditEvent:
    sequence: int
    event_type: str
    subject_id: str
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str
class AuditTrail:
    def __init__(self) -> None: self.events: list[AuditEvent] = []
    def append(self, event_type: str, subject_id: str, payload: dict[str, Any]) -> AuditEvent:
        previous=self.events[-1].event_hash if self.events else "0"*64
        sequence=len(self.events)+1; canonical=json.dumps({"sequence":sequence,"event_type":event_type,"subject_id":subject_id,"payload":payload,"previous_hash":previous},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
        event=AuditEvent(sequence,event_type,subject_id,dict(payload),previous,hashlib.sha256(canonical).hexdigest()); self.events.append(event); return event
    def verify(self) -> bool:
        previous="0"*64
        for index,event in enumerate(self.events,1):
            if event.sequence != index or event.previous_hash != previous: return False
            canonical=json.dumps({"sequence":event.sequence,"event_type":event.event_type,"subject_id":event.subject_id,"payload":event.payload,"previous_hash":event.previous_hash},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
            if hashlib.sha256(canonical).hexdigest() != event.event_hash: return False
            previous=event.event_hash
        return True
