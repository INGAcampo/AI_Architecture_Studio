import pytest
from engines.analysis.project import AnalysisProject
from engines.analysis.manager import AnalysisManager
from engines.analysis.platform import *

@pytest.mark.parametrize("i",range(120))
def test_platform(i):
    p=AnalysisProject(f"P{i}","Demo")
    platform=ProfessionalStructuralAnalysisPlatform(AnalysisManager())
    r=platform.analyze(f"R{i}",p,(("validate",lambda c:True),("solve",lambda c:{"u":0.1})))
    assert r.completed
    assert r.results_db.metadata["solve"]["u"]==pytest.approx(0.1)
