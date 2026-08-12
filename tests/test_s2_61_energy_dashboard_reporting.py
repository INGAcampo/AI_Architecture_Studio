import json
import pytest
from engines.structural.energy_dashboard import *

@pytest.mark.parametrize("index", range(120))
def test_energy_dashboard(index):
    reporter = EnergyDashboardReporter()
    kpi = EnergyKpi(
        f"K{index}",
        f"KPI {index}",
        float(index),
        "kWh/m2",
        target=100.0,
    )
    summary = reporter.summary((kpi,))
    assert summary["kpi_count"] == 1
    data = json.loads(reporter.json_report("Energy Report", (kpi,)))
    assert data["kpis"][0]["kpi_id"] == kpi.kpi_id
