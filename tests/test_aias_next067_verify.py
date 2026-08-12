from aias_next067_verify import ArchiveVerifier
def test_missing_archive(tmp_path):assert ArchiveVerifier(tmp_path/'x').run()['status']=='NO_ARCHIVE'
