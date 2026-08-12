from pathlib import Path

from aias_next026_release import BundleBuilder


def test_bundle_marks_external_gates_pending(tmp_path: Path):
    bundle = BundleBuilder(tmp_path).build()
    assert bundle.status == "RELEASE_CANDIDATE_EVIDENCE_ONLY"
    assert bundle.external_gates_pending is True
