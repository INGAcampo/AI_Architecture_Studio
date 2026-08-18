from pathlib import Path

from aias_next017_review import ReviewPackageBuilder


def test_review_package_is_not_ready_without_intake(tmp_path: Path):
    package = ReviewPackageBuilder(tmp_path).build()
    assert package.review_ready is False
    assert package.decision == "CONTINUE_COLLECTION"
