import json
import pytest
from engines.structural.reports import *

@pytest.mark.parametrize("index", range(120))
def test_reports(index):
    generator = StructuralReportGenerator()
    section = ReportSection(f"Section {index}", f"Value {index}")
    markdown = generator.markdown("AIAS Report", (section,))
    assert f"Section {index}" in markdown
    data = json.loads(generator.json_report("AIAS Report", (section,)))
    assert data["sections"][0]["content"] == f"Value {index}"
