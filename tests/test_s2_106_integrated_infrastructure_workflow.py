import pytest
from engines.civil.integrated_workflow import *

@pytest.mark.parametrize("i", range(120))
def test_workflow(i):
    steps = (
        WorkflowStep("A","complete"),
        WorkflowStep("B","complete"),
    )
    e = IntegratedInfrastructureWorkflow()
    assert e.is_complete(steps)
    assert e.progress(steps) == 1
