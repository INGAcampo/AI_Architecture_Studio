from aias_next079_authority_report import AuthorityReport

def test_report_preserves_pending_authority():
    result = AuthorityReport().generate([{"id": "E-1"}], [])
    assert result["report"] == "AIAS-NEXT-079"
    assert result["alignment"]["unmatched_evidence"] == ["E-1"]
    assert result["certification"] is False
