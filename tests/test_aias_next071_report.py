from aias_next071_report import ArchiveMonitorReport
def test_report_missing(tmp_path):assert ArchiveMonitorReport(tmp_path/'x').build()['status']=='NO_ARCHIVE'
