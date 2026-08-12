from aias_next088_metrics import ReviewMetrics

def test_metrics_count_decisions():
    result = ReviewMetrics().calculate([{"decision": "ACCEPTED"}, {"decision": "PENDING_REVIEW"}])
    assert result["accepted"] == 1
    assert result["pending"] == 1
    assert result["organizational_maturity_audited"] is False
