from aias_next092_dashboard_report import DashboardReport

def test_report_preserves_validation_boundary():
    result = DashboardReport().generate({"dashboard_component": "EVIDENCE_REVIEW_METRICS", "audited": False})
    assert result["report"] == "AIAS-NEXT-092"
    assert result["validation"]["valid"] is True
    assert result["certification"] is False
