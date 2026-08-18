from pathlib import Path

from aias_next032_decision import DecisionRecordBuilder


def test_decision_record_starts_pending(tmp_path: Path):
    record = DecisionRecordBuilder(tmp_path).build()
    assert record.decision == "PENDING"
    assert record.authority_id == "UNVERIFIED"
