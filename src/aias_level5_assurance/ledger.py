"""Tamper-evident longitudinal production-evidence ledger."""
from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from pathlib import Path

from .models import AssuranceEvidence
from .policy import Level5Policy

GENESIS = "0" * 64
ALLOWED_EVENTS = {
    "PROJECT_STARTED",
    "PROJECT_COMPLETED",
    "CRITERION_OBSERVED",
    "METRIC_OBSERVED",
    "PROFESSIONAL_REVIEW",
    "RECOVERY_DRILL",
    "IMPROVEMENT_ACTION",
    "INCIDENT",
    "AUDIT_ATTESTATION",
}


def _canonical(value: dict) -> bytes:
    """Serialize one evidence value deterministically for hashing and signing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class EvidenceLedger:
    """Append and verify authenticated, hash-chained Level 5 evidence records."""

    def __init__(self, path: Path, signing_key: bytes):
        if len(signing_key) < 32:
            raise ValueError("signing_key_too_short")
        self.path = Path(path)
        self.signing_key = signing_key

    def records(self) -> list[dict]:
        """Return all ledger records after strict JSON decoding."""
        if not self.path.is_file():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def append(self, event_type: str, payload: dict, observed_at: str, *, evidence_id: str) -> dict:
        """Append one real observation after validating identity, time and evidence semantics."""
        if event_type not in ALLOWED_EVENTS:
            raise ValueError("unsupported_evidence_event")
        if not evidence_id.startswith("L5E-"):
            raise ValueError("invalid_evidence_id")
        observed = datetime.fromisoformat(observed_at)
        if observed.tzinfo is None or observed > datetime.now(timezone.utc):
            raise ValueError("invalid_observation_time")
        if not payload.get("source"):
            raise ValueError("evidence_source_required")
        if event_type in {"PROJECT_STARTED", "PROJECT_COMPLETED", "PROFESSIONAL_REVIEW"} and not payload.get("project_id"):
            raise ValueError("project_id_required")
        if event_type == "CRITERION_OBSERVED":
            if payload.get("criterion_id") not in Level5Policy.REQUIRED_CRITERIA or not payload.get("project_id"):
                raise ValueError("invalid_production_criterion")
        if event_type == "METRIC_OBSERVED":
            if payload.get("metric") not in Level5Policy.METRIC_THRESHOLDS or not isinstance(payload.get("value"), (int, float)):
                raise ValueError("invalid_metric_observation")
        if event_type == "AUDIT_ATTESTATION":
            if not payload.get("independent") or payload.get("conclusion") != "LEVEL_5_CONFORMANT" or payload.get("open_critical_findings") != 0 or not payload.get("auditor_identity") or not payload.get("accreditation_ref"):
                raise ValueError("invalid_independent_audit_attestation")
        current = self.records()
        if any(row["evidence_id"] == evidence_id for row in current):
            raise ValueError("duplicate_evidence_id")
        previous_hash = current[-1]["record_hash"] if current else GENESIS
        unsigned = {"sequence": len(current) + 1, "evidence_id": evidence_id, "event_type": event_type, "observed_at": observed_at, "payload": payload, "previous_hash": previous_hash}
        record_hash = hashlib.sha256(_canonical(unsigned)).hexdigest()
        signature = hmac.new(self.signing_key, record_hash.encode("ascii"), hashlib.sha256).hexdigest()
        record = {**unsigned, "record_hash": record_hash, "signature": signature}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
        return record

    def verify(self) -> dict:
        """Verify sequence, hash chain and HMAC authenticity for the complete ledger."""
        errors: list[str] = []
        previous_hash = GENESIS
        rows = self.records()
        for expected_sequence, row in enumerate(rows, 1):
            unsigned = {key: row[key] for key in ("sequence", "evidence_id", "event_type", "observed_at", "payload", "previous_hash")}
            expected_hash = hashlib.sha256(_canonical(unsigned)).hexdigest()
            expected_signature = hmac.new(self.signing_key, expected_hash.encode("ascii"), hashlib.sha256).hexdigest()
            if row.get("sequence") != expected_sequence:
                errors.append(f"sequence:{expected_sequence}")
            if row.get("previous_hash") != previous_hash:
                errors.append(f"chain:{expected_sequence}")
            if row.get("record_hash") != expected_hash:
                errors.append(f"hash:{expected_sequence}")
            if not hmac.compare_digest(str(row.get("signature", "")), expected_signature):
                errors.append(f"signature:{expected_sequence}")
            previous_hash = str(row.get("record_hash", ""))
        return {"valid": not errors, "records": len(rows), "head_sha256": previous_hash, "errors": errors}

    def campaign_status(self) -> dict:
        """Derive honest longitudinal progress solely from verified ledger evidence."""
        verification = self.verify()
        if not verification["valid"]:
            return {**verification, "eligible_for_independent_audit": False}
        rows = self.records()
        completed_projects = sorted({row["payload"]["project_id"] for row in rows if row["event_type"] == "PROJECT_COMPLETED"})
        criteria = sorted({row["payload"]["criterion_id"] for row in rows if row["event_type"] == "CRITERION_OBSERVED"})
        dates = [datetime.fromisoformat(row["observed_at"]) for row in rows]
        window_days = (max(dates) - min(dates)).days if dates else 0
        metrics: dict[str, float] = {}
        for row in rows:
            if row["event_type"] == "METRIC_OBSERVED":
                metrics[row["payload"]["metric"]] = float(row["payload"]["value"])
        metric_failures = {name: {"actual": metrics.get(name), "required": minimum} for name, minimum in Level5Policy.METRIC_THRESHOLDS.items() if metrics.get(name) is None or metrics[name] < minimum}
        audit_present = any(row["event_type"] == "AUDIT_ATTESTATION" for row in rows)
        eligible = window_days >= Level5Policy.MINIMUM_WINDOW_DAYS and len(completed_projects) >= Level5Policy.MINIMUM_PROJECTS and set(criteria) == set(Level5Policy.REQUIRED_CRITERIA) and not metric_failures
        return {**verification, "window_days": window_days, "completed_projects": len(completed_projects), "criteria_observed": criteria, "metric_failures": metric_failures, "independent_conformant_audit_recorded": audit_present, "eligible_for_independent_audit": eligible, "ready_for_formal_level5_assessment": eligible and audit_present, "organizational_level_5_established": False}

    def assurance_evidence(self) -> list[AssuranceEvidence]:
        """Project verified criterion observations into assessor-compatible evidence."""
        if not self.verify()["valid"]:
            raise ValueError("ledger_integrity_failed")
        return [AssuranceEvidence(row["evidence_id"], row["payload"]["criterion_id"], "PRODUCTION_OBSERVATION", row["observed_at"], row["payload"]["source"], row["payload"].get("value"), row["record_hash"], row["payload"]["project_id"]) for row in self.records() if row["event_type"] == "CRITERION_OBSERVED"]
