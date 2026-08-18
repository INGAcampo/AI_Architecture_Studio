from aias_next061_status import RoadmapStatus
def test_status_missing(tmp_path):assert RoadmapStatus(tmp_path/'x').read()['status']=='HOLD'
