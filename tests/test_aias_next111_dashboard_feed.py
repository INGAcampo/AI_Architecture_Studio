from aias_next111_dashboard_feed import BundleDashboardFeed

def test_feed_is_operational_only():
    result = BundleDashboardFeed().build({"valid": True})
    assert result["feed"] == "AIAS-NEXT-111"
    assert result["classification"] == "OPERATIONAL_ONLY"
    assert result["audited"] is False
