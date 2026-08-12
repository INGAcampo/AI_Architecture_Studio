import json
from pathlib import Path

from aias_next013_review import EvidenceReview


def test_review_does_not_claim_completion_without_records(tmp_path: Path):
    result = EvidenceReview(tmp_path / "missing.jsonl").run()
    assert result.complete is False
    assert result.valid_records == 0
