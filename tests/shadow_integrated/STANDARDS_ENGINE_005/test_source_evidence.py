from standards_engine_evidence.source import SourceEvidence,evaluate_source_evidence


def valid_source():
    return SourceEvidence(
        "SRC-1",
        "DEMO-PUBLISHER",
        "2026.1",
        "a"*64,
        True,
    )


def test_verified_source_is_accepted():
    assert evaluate_source_evidence(valid_source()).accepted is True


def test_unverified_source_is_rejected():
    source=SourceEvidence("SRC-1","PUB","1","a"*64,False)
    d=evaluate_source_evidence(source)
    assert d.accepted is False
    assert d.reason=="source_not_independently_verified"


def test_bad_hash_is_rejected():
    source=SourceEvidence("SRC-1","PUB","1","bad",True)
    assert evaluate_source_evidence(source).accepted is False
