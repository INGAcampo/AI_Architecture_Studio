from dataclasses import replace

from standards_engine_ext.provenance import RulePack,RulePackProvenance,compute_rule_pack_sha256
from standards_engine_report.applicability import ApplicabilityContext,evaluate_applicability
from standards_engine_report.report import build_evaluation_report


class Outcome:
    def __init__(self,passed,severity,source_reference):
        self.passed=passed
        self.severity=severity
        self.source_reference=source_reference


def make_pack():
    provisional=RulePack(
        "DEMO",
        "1.0",
        RulePackProvenance(
            "DEMO-NOT-A-CODE",
            "1",
            "TEST",
            "2026-01-01",
            None,
        ),
        ("R1",),
        "0"*64,
    )
    return replace(
        provisional,
        content_sha256=compute_rule_pack_sha256(provisional),
    )


def test_applicability_accepts_matching_jurisdiction():
    d=evaluate_applicability(
        make_pack(),
        ApplicabilityContext("TEST","BUILDING","2026-08-01"),
    )
    assert d.applicable is True


def test_applicability_rejects_wrong_jurisdiction():
    d=evaluate_applicability(
        make_pack(),
        ApplicabilityContext("OTHER","BUILDING","2026-08-01"),
    )
    assert d.applicable is False
    assert d.reason=="jurisdiction_mismatch"


def test_report_counts_and_sources_are_deterministic():
    report=build_evaluation_report(
        "RS1",
        (
            Outcome(True,"ERROR","SRC-B"),
            Outcome(False,"WARNING","SRC-A"),
            Outcome(False,"ERROR","SRC-A"),
        ),
    )
    assert report.passed_count==1
    assert report.failed_count==2
    assert report.warnings_count==1
    assert report.source_references==("SRC-A","SRC-B")
