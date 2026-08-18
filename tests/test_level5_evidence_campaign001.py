import json
from datetime import datetime, timezone

import pytest

from aias_level5_assurance import EvidenceLedger

KEY = b"test-only-level5-evidence-signing-key-32bytes"
NOW = "2026-08-03T12:00:00+00:00"


def test_real_evidence_is_authenticated_and_hash_chained(tmp_path):
    ledger = EvidenceLedger(tmp_path / "evidence.jsonl", KEY)
    first = ledger.append("PROJECT_STARTED", {"project_id": "PRJ-001", "source": "signed project order"}, NOW, evidence_id="L5E-000001")
    second = ledger.append("PROJECT_COMPLETED", {"project_id": "PRJ-001", "source": "accepted technical file"}, NOW, evidence_id="L5E-000002")
    assert second["previous_hash"] == first["record_hash"]
    assert ledger.verify() == {"valid": True, "records": 2, "head_sha256": second["record_hash"], "errors": []}


def test_tampering_is_detected(tmp_path):
    path = tmp_path / "evidence.jsonl"
    ledger = EvidenceLedger(path, KEY)
    ledger.append("PROJECT_COMPLETED", {"project_id": "PRJ-001", "source": "acceptance"}, NOW, evidence_id="L5E-000001")
    row = json.loads(path.read_text(encoding="utf-8")); row["payload"]["project_id"] = "PRJ-TAMPERED"
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    assert not ledger.verify()["valid"] and "hash:1" in ledger.verify()["errors"]


def test_campaign_never_claims_level5_from_insufficient_history(tmp_path):
    ledger = EvidenceLedger(tmp_path / "evidence.jsonl", KEY)
    ledger.append("PROJECT_COMPLETED", {"project_id": "PRJ-001", "source": "acceptance"}, NOW, evidence_id="L5E-000001")
    status = ledger.campaign_status()
    assert status["completed_projects"] == 1
    assert not status["eligible_for_independent_audit"]
    assert not status["organizational_level_5_established"]


def test_invalid_or_future_observations_are_rejected(tmp_path):
    ledger = EvidenceLedger(tmp_path / "evidence.jsonl", KEY)
    with pytest.raises(ValueError, match="project_id_required"):
        ledger.append("PROJECT_COMPLETED", {"source": "none"}, NOW, evidence_id="L5E-000001")
    with pytest.raises(ValueError, match="invalid_observation_time"):
        ledger.append("INCIDENT", {"source": "future"}, "2999-01-01T00:00:00+00:00", evidence_id="L5E-000002")
    with pytest.raises(ValueError, match="invalid_independent_audit_attestation"):
        ledger.append("AUDIT_ATTESTATION", {"source": "internal memo", "independent": False, "conclusion": "LEVEL_5_CONFORMANT", "open_critical_findings": 0, "auditor_identity": "AIAS", "accreditation_ref": "SELF"}, NOW, evidence_id="L5E-000003")


def test_criterion_observation_projects_to_assessor_evidence(tmp_path):
    ledger = EvidenceLedger(tmp_path / "evidence.jsonl", KEY)
    ledger.append("CRITERION_OBSERVED", {"project_id": "PRJ-001", "criterion_id": "governance", "source": "approved gate record", "value": True}, NOW, evidence_id="L5E-000001")
    evidence = ledger.assurance_evidence()[0]
    assert evidence.classification == "PRODUCTION_OBSERVATION" and evidence.project_id == "PRJ-001"
