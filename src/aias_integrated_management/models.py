"""Typed contracts for AIAS integrated management evidence."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class ManagementRisk:
    """Represent one owned risk across quality, security, AI or continuity."""
    risk_id: str
    domain: str
    statement: str
    likelihood: int
    impact: int
    owner: str
    treatment: str
    status: str = "OPEN"

    def validate(self) -> None:
        """Validate identity, scoring, ownership and treatment fields."""
        if not self.risk_id.startswith("IMSR-") or self.domain not in {"QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY"}:
            raise ValueError("invalid_management_risk")
        if not 1 <= self.likelihood <= 5 or not 1 <= self.impact <= 5 or not all((self.statement, self.owner, self.treatment)):
            raise ValueError("invalid_management_risk")

    def to_dict(self) -> dict:
        """Project the risk into its stable dictionary representation."""
        return {**asdict(self), "score": self.likelihood * self.impact}


@dataclass(frozen=True, slots=True)
class ManagementObjective:
    """Represent one measurable management-system objective."""
    objective_id: str
    domain: str
    statement: str
    metric: str
    baseline: float
    target: float
    due_date: str
    owner: str

    def validate(self) -> None:
        """Validate an objective without inventing performance observations."""
        if not self.objective_id.startswith("IMSO-") or not all((self.domain, self.statement, self.metric, self.due_date, self.owner)):
            raise ValueError("invalid_management_objective")
        date.fromisoformat(self.due_date)

    def to_dict(self) -> dict:
        """Project the objective into its stable dictionary representation."""
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CorrectiveAction:
    """Represent a bounded corrective action linked to objective evidence."""
    action_id: str
    source: str
    finding: str
    root_cause: str
    action: str
    owner: str
    due_date: str
    status: str = "OPEN"

    def validate(self) -> None:
        """Validate corrective-action traceability and lifecycle state."""
        if not self.action_id.startswith("IMSCA-") or not all((self.source, self.finding, self.root_cause, self.action, self.owner)) or self.status not in {"OPEN", "IMPLEMENTED", "EFFECTIVE", "CLOSED"}:
            raise ValueError("invalid_corrective_action")
        date.fromisoformat(self.due_date)

    def to_dict(self) -> dict:
        """Project the corrective action into its stable dictionary representation."""
        return asdict(self)
