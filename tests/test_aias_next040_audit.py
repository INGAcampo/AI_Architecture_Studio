from aias_next040_audit import ContinuityAuditor
def test_empty_archive_is_no_evidence(tmp_path): assert ContinuityAuditor(tmp_path/'x').run().status=='NO_EVIDENCE'
