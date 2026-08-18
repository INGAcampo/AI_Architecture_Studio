from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceEvidence:
    source_id: str
    publisher: str
    document_version: str
    sha256: str
    independently_verified: bool


@dataclass(frozen=True)
class SourceAdmissionDecision:
    accepted: bool
    reason: str


def evaluate_source_evidence(source: SourceEvidence) -> SourceAdmissionDecision:
    if not source.source_id.strip():
        return SourceAdmissionDecision(False,"missing_source_id")
    if not source.publisher.strip():
        return SourceAdmissionDecision(False,"missing_publisher")
    if not source.document_version.strip():
        return SourceAdmissionDecision(False,"missing_document_version")
    if len(source.sha256)!=64:
        return SourceAdmissionDecision(False,"invalid_sha256")
    if not source.independently_verified:
        return SourceAdmissionDecision(False,"source_not_independently_verified")
    return SourceAdmissionDecision(True,"accepted")
