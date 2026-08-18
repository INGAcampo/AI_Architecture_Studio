from aias_next039_archive import ContinuityArchive
def test_archive_records_missing_source_without_fabricating_hash(tmp_path):
    e=ContinuityArchive(tmp_path/'archive.jsonl').append(tmp_path/'missing'); assert e.sha256==''
