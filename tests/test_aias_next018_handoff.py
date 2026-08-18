from pathlib import Path

from aias_next018_handoff import HandoffBuilder


def test_handoff_requires_human_review(tmp_path: Path):
    manifest = HandoffBuilder(tmp_path).build()
    assert manifest.approval_status == "PENDING_HUMAN_REVIEW"
    assert manifest.required_reviewer_role == "independent human reviewer"
