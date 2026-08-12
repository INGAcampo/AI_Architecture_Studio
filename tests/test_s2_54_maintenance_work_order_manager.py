import pytest
from engines.structural.maintenance import *

@pytest.mark.parametrize("index", range(120))
def test_maintenance(index):
    manager = MaintenanceManager()
    status = WorkOrderStatus.OPEN if index % 2 == 0 else WorkOrderStatus.COMPLETED
    order = WorkOrder(
        f"W{index}",
        f"A{index%7}",
        f"Work {index}",
        priority=index % 5 + 1,
        status=status,
    )
    manager.create(order)
    assert order in manager.for_asset(order.asset_id)
    expected = 1 if status is WorkOrderStatus.OPEN else 0
    assert len(manager.active_orders()) == expected
