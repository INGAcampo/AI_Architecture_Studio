from aias_next069_publication import ArchivePublication
def test_missing_archive():assert ArchivePublication('missing').publish()['approval'] is False
