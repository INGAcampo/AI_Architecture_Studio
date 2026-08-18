from aias_next112_dashboard_validation import FeedValidation

def test_validation_accepts_operational_feed():
    result = FeedValidation().validate({"classification": "OPERATIONAL_ONLY", "audited": False})
    assert result["valid"] is True
    assert result["audited"] is False
