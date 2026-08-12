from aias_next064_report import MonitorReport
def test_report_missing(tmp_path):assert MonitorReport(tmp_path/'x').build()['status']=='HOLD'
