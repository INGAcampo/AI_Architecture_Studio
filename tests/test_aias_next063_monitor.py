from aias_next063_monitor import RoadmapMonitor
def test_monitor_holds_missing(tmp_path):assert RoadmapMonitor(tmp_path/'x').check()['status']=='HOLD'
