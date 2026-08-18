from pathlib import Path

from aias_next015_intake import EvidenceIntakeReport


def test_intake_report_is_explicitly_incomplete_without_sessions(tmp_path: Path):
    report = EvidenceIntakeReport(tmp_path).generate()
    assert report.complete is False
    assert report.sessions == 0
    assert (tmp_path / "engineering/aias/next015_intake/INTAKE_REPORT.json").exists()
