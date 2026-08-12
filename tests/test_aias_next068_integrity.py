from aias_next068_integrity import IntegrityReport
def test_integrity_missing(tmp_path):assert IntegrityReport(tmp_path/'x').build()['status']=='NO_ARCHIVE'
