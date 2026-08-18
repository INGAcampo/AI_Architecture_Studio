import pytest
from engines.analysis.project import AnalysisProject
from engines.analysis.manager import *

@pytest.mark.parametrize("i",range(120))
def test_manager(i):
    p=AnalysisProject(f"P{i}","Demo")
    m=AnalysisManager()
    run=m.execute(f"R{i}",p,(("validate",lambda c:True),))
    assert run.pipeline_result.completed
    assert m.get_run(f"R{i}") is run
