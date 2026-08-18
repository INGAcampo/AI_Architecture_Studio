from aias_next090_dashboard_integration import DashboardIntegration

def test_integration_accepts_operational_feed():
    result = DashboardIntegration().integrate({"classification": "OPERATIONAL_ONLY", "metrics": {}})
    assert result["dashboard_component"] == "EVIDENCE_REVIEW_METRICS"
    assert result["audited"] is False
