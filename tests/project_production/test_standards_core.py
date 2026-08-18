from aias_standards_core import ApplicabilityEngine, StandardsPack


def test_fail_closed_and_evidence_bound():
    engine = ApplicabilityEngine(StandardsPack())
    context = {"project": "PILOT-BUILDING-001", "jurisdiction": "VE"}
    assert engine.evaluate("VE-SEISMIC-001", context).status == "INSUFFICIENT_EVIDENCE"
    verdict = engine.evaluate("VE-SEISMIC-001", context, {"source": "certified-study", "value": "zone-5", "pass": True})
    assert verdict.status == "PASS"
    assert len(verdict.evidence_sha256) == 64


def test_non_matching_jurisdiction_is_not_applicable():
    assert ApplicabilityEngine(StandardsPack()).evaluate("VE-WIND-001", {"project": "PILOT-BUILDING-001", "jurisdiction": "XX"}).status == "NOT_APPLICABLE"
