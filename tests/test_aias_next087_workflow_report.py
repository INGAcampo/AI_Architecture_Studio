from aias_next087_workflow_report import WorkflowReport

def test_report_accepts_complete_ordered_flow():
    result = WorkflowReport().generate(["INTAKE", "VALIDATION", "DECISION"])
    assert result["complete"] is True
    assert result["approved"] is False
