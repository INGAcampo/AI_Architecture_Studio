from aias_next091_dashboard_validation import DashboardValidation

def test_validation_accepts_integrated_component():
    result = DashboardValidation().validate({"dashboard_component": "EVIDENCE_REVIEW_METRICS", "audited": False})
    assert result["valid"] is True
    assert result["audited"] is False
