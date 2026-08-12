from pathlib import Path

from aias_next036_review import FinalReviewBuilder


def test_final_review_package_is_not_release_approved(tmp_path: Path):
    package = FinalReviewBuilder(tmp_path).build()
    assert package.status == "PENDING_REVIEW"
    assert package.release_approved is False
