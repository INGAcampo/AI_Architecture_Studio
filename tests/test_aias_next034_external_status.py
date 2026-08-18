from pathlib import Path

from aias_next034_external_status import ExternalStatusBuilder


def test_status_report_blocks_without_registry(tmp_path: Path):
    report = ExternalStatusBuilder(tmp_path / "registry.json").build()
    assert report.all_approved is False
    assert report.release_blocked is True
