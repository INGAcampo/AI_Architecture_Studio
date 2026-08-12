import json
import pytest
from engines.civil.civil_reporting import *

@pytest.mark.parametrize("index", range(120))
def test_civil_reporting(index):
    quantities = (
        CivilQuantity(f"Q{index}A", "Cut", 100 + index, "m3"),
        CivilQuantity(f"Q{index}B", "Fill", 80 + index, "m3"),
    )
    engine = CivilReportingEngine()
    totals = engine.total_by_unit(quantities)
    assert totals["m3"] == 180 + 2*index
    data = json.loads(engine.json_report("Civil Report", quantities))
    assert data["totals"]["m3"] == 180 + 2*index
