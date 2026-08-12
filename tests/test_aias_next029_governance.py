from pathlib import Path

from aias_next029_governance import GovernanceBuilder


def test_governance_record_does_not_grant_approval(tmp_path: Path):
    record = GovernanceBuilder(tmp_path).build()
    assert record.production_approval == "NOT_GRANTED"
    assert record.external_gates == "PENDING"
