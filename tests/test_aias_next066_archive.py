from aias_next066_archive import RoadmapArchive
def test_archive_missing_hash_empty(tmp_path):assert RoadmapArchive(tmp_path/'a').add(tmp_path/'x')['sha256']==''
