from aias_next052_summary import StrategicSummary
def test_summary_pending(tmp_path):assert StrategicSummary(tmp_path/'x').build()['approval']=='PENDING'
