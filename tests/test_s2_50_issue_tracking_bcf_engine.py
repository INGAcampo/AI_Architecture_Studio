import json
import pytest
from engines.structural.bcf import *

@pytest.mark.parametrize("index", range(120))
def test_bcf_engine(index):
    engine = BcfIssueEngine()
    status = IssueStatus.OPEN if index % 2 == 0 else IssueStatus.RESOLVED
    issue = BcfIssue(
        f"I{index}",
        f"Issue {index}",
        status,
        related_element_ids=(f"E{index}",),
        comments=("Created",),
    )
    engine.add(issue)
    data = json.loads(engine.export_json())
    assert data["issues"][0]["issue_id"] == issue.issue_id
    assert len(engine.open_issues()) == (1 if status is IssueStatus.OPEN else 0)
