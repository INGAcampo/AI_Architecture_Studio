from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import hashlib
from typing import Any
class EvidenceStatus(str, Enum):
    RECEIVED="received"; VERIFIED="verified"; REJECTED="rejected"; PENDING_AUTHORITY="pending_authority"
@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    gate_id: str
    authority: str
    scope: str
    content_sha256: str
    status: EvidenceStatus = EvidenceStatus.RECEIVED
    notes: str = ""
class EvidenceIntake:
    def __init__(self) -> None: self.records: dict[str, EvidenceRecord] = {}
    def receive(self, record: EvidenceRecord) -> EvidenceRecord:
        if not record.evidence_id.strip() or not record.gate_id.strip(): raise ValueError("evidence_and_gate_required")
        if record.evidence_id in self.records: raise ValueError("duplicate_evidence:" + record.evidence_id)
        if len(record.content_sha256) != 64: raise ValueError("invalid_sha256")
        self.records[record.evidence_id] = record
        return record
    def verify(self, evidence_id: str, content: bytes, *, authority_confirmed: bool = False) -> EvidenceRecord:
        current=self.records[evidence_id]; digest=hashlib.sha256(content).hexdigest()
        if digest != current.content_sha256: raise ValueError("evidence_hash_mismatch")
        status=EvidenceStatus.VERIFIED if authority_confirmed else EvidenceStatus.PENDING_AUTHORITY
        updated=EvidenceRecord(current.evidence_id,current.gate_id,current.authority,current.scope,current.content_sha256,status,current.notes)
        self.records[evidence_id]=updated; return updated
    def roadmap_eligible(self, evidence_id: str) -> bool: return self.records[evidence_id].status == EvidenceStatus.VERIFIED
