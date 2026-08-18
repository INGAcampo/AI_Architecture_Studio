from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class DashboardMetric:
    metric_id: str
    label: str
    value: float
    unit: str = ""
    status: str = "normal"

    def __post_init__(self):
        if not self.metric_id.strip() or not self.label.strip():
            raise ValueError("Datos obligatorios")

@dataclass(frozen=True, slots=True)
class DashboardCard:
    card_id: str
    title: str
    metrics: tuple[DashboardMetric, ...] = ()
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.card_id.strip() or not self.title.strip():
            raise ValueError("Datos obligatorios")

class DigitalTwinDashboard:
    def __init__(self):
        self._cards = {}

    def add_card(self, card):
        if card.card_id in self._cards:
            raise KeyError(card.card_id)
        self._cards[card.card_id] = card
        return card

    def cards(self):
        return tuple(self._cards[key] for key in sorted(self._cards))

    def metrics(self):
        return tuple(
            metric
            for card in self.cards()
            for metric in card.metrics
        )

    def summary(self):
        metrics = self.metrics()
        return {
            "card_count": len(self._cards),
            "metric_count": len(metrics),
            "alert_count": sum(metric.status != "normal" for metric in metrics),
        }
