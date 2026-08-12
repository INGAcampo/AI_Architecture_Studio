from aias_next089_dashboard_feed import DashboardFeed

def test_feed_marks_operational_only():
    result = DashboardFeed().build({"total": 1})
    assert result["feed"] == "AIAS-NEXT-089"
    assert result["classification"] == "OPERATIONAL_ONLY"
    assert result["audited"] is False
