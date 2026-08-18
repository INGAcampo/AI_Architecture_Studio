from dataclasses import dataclass
from enum import Enum

class WorkOrderStatus(str, Enum):
    OPEN = "open"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass(frozen=True, slots=True)
class WorkOrder:
    work_order_id: str
    asset_id: str
    title: str
    priority: int
    status: WorkOrderStatus = WorkOrderStatus.OPEN
    scheduled_for: str | None = None

    def __post_init__(self):
        if not self.work_order_id.strip() or not self.asset_id.strip() or not self.title.strip():
            raise ValueError("Datos obligatorios")
        if not 1 <= self.priority <= 5:
            raise ValueError("priority debe estar entre 1 y 5")

class MaintenanceManager:
    def __init__(self):
        self._orders = {}

    def create(self, order):
        if order.work_order_id in self._orders:
            raise KeyError(order.work_order_id)
        self._orders[order.work_order_id] = order
        return order

    def for_asset(self, asset_id):
        return tuple(
            order for order in self._orders.values()
            if order.asset_id == asset_id
        )

    def active_orders(self):
        return tuple(
            order for order in self._orders.values()
            if order.status not in (WorkOrderStatus.COMPLETED, WorkOrderStatus.CANCELLED)
        )

    def highest_priority(self):
        active = self.active_orders()
        return min(active, key=lambda order: order.priority) if active else None
