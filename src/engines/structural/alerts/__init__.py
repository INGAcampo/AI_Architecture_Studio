from dataclasses import dataclass
from enum import Enum

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class Comparison(str, Enum):
    GREATER_THAN = "gt"
    GREATER_EQUAL = "ge"
    LESS_THAN = "lt"
    LESS_EQUAL = "le"

@dataclass(frozen=True, slots=True)
class OperationalRule:
    rule_id: str
    metric: str
    comparison: Comparison
    threshold: float
    severity: AlertSeverity

    def __post_init__(self):
        if not self.rule_id.strip() or not self.metric.strip():
            raise ValueError("Datos obligatorios")

@dataclass(frozen=True, slots=True)
class Alert:
    alert_id: str
    rule_id: str
    asset_id: str
    severity: AlertSeverity
    value: float
    threshold: float

class AlertEngine:
    def evaluate(self, rule, asset_id, value):
        checks = {
            Comparison.GREATER_THAN: value > rule.threshold,
            Comparison.GREATER_EQUAL: value >= rule.threshold,
            Comparison.LESS_THAN: value < rule.threshold,
            Comparison.LESS_EQUAL: value <= rule.threshold,
        }
        if not checks[rule.comparison]:
            return None
        return Alert(
            f"{rule.rule_id}:{asset_id}",
            rule.rule_id,
            asset_id,
            rule.severity,
            value,
            rule.threshold,
        )
