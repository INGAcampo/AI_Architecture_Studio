from aias_next086_workflow import ReviewWorkflow

def test_workflow_advances_in_order():
    result = ReviewWorkflow().advance("INTAKE")
    assert result["next"] == "VALIDATION"
    assert result["approved"] is False
