import pytest
from documentation_kernel.documentation_qa import *

@pytest.mark.parametrize("i", range(120))
def test_qa(i):
    sheets = (
        {"sheet_id": "S1", "number": "A-101", "view_ids": ("V1",)},
        {"sheet_id": "S2", "number": "A-101", "view_ids": ()},
    )
    views = ({"view_id": "V1"},)
    engine = DocumentationQAAutomation()
    issues = engine.review(sheets, views)
    summary = engine.summary(issues)
    assert summary["total"] == 2
    assert summary["errors"] == 1
    assert summary["warnings"] == 1
