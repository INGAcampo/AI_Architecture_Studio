from aias_next070_monitor import ArchiveMonitor
def test_missing(tmp_path):assert ArchiveMonitor(tmp_path/'x').check()['status']=='NO_ARCHIVE'
