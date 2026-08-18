import pytest
from engines.structural.analysis_cases import *

@pytest.mark.parametrize("index", range(120))
def test_analysis_cases(index):
    manager = AnalysisCaseManager()
    kind = list(AnalysisCaseKind)[index % len(AnalysisCaseKind)]
    case = AnalysisCase(f"C{index}", f"Case {index}", kind, active=index % 3 != 0)
    manager.add(case)
    assert manager.get(case.case_id) is case
    assert len(manager.active_cases()) in (0, 1)
