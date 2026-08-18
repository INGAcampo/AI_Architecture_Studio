from aias_next073_monitor import PublicationMonitor

def test_monitor_reports_missing_publication(tmp_path):
    result = PublicationMonitor(tmp_path / "publication.pdf").check()
    assert result == {"status": "NO_PUBLICATION", "observed": False, "changed": False}
