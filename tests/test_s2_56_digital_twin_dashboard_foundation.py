import pytest
from engines.structural.dashboard import *

@pytest.mark.parametrize("index", range(120))
def test_dashboard(index):
    dashboard = DigitalTwinDashboard()
    metric = DashboardMetric(
        f"M{index}",
        f"Metric {index}",
        float(index),
        "unit",
        status="alert" if index % 2 else "normal",
    )
    card = DashboardCard(f"C{index}", f"Card {index}", (metric,))
    dashboard.add_card(card)
    summary = dashboard.summary()
    assert summary["card_count"] == 1
    assert summary["metric_count"] == 1
    assert summary["alert_count"] == (1 if index % 2 else 0)
