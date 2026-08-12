from aias_next084_decision import DecisionRecord

def test_default_decision_is_pending():
    result = DecisionRecord().create("E-1")
    assert result["decision"] == "PENDING_REVIEW"
    assert result["approved"] is False
