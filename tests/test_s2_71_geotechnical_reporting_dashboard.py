import json
import pytest
from engines.structural.geotechnical_dashboard import *

@pytest.mark.parametrize("index", range(120))
def test_geotechnical_dashboard(index):
    dashboard = GeotechnicalDashboard()
    kpi = GeotechnicalKpi(f"K{index}", f"KPI {index}", float(index+1), "unit")
    data = json.loads(dashboard.json_report("Geotechnical", (kpi,)))
    assert data["summary"]["kpi_count"] == 1
    assert data["kpis"][0]["kpi_id"] == kpi.kpi_id
