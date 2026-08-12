from aias_next065_publication import MonitorPublication
def test_publication_missing(tmp_path):assert MonitorPublication(tmp_path/'x').publish()['status']=='HOLD'
