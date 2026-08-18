"""Public module supporting foundation drawings, schedules and technical documentation."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class BarMark:
    """Execute the public BarMark operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    mark: str
    direction: str
    diameter_mm: int
    spacing_mm: int
    quantity: int
    length_mm: int
    layer: str = "BOTTOM"

    @property
    def unit_weight_kg_m(self) -> float:
        """Execute the public BarMark.unit_weight_kg_m operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
        return self.diameter_mm**2 / 162.0

    @property
    def total_weight_kg(self) -> float:
        """Execute the public BarMark.total_weight_kg operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
        return self.quantity * self.length_mm / 1000.0 * self.unit_weight_kg_m


@dataclass(frozen=True, slots=True)
class QuantitySummary:
    """Execute the public QuantitySummary operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    concrete_m3: float
    formwork_m2: float
    excavation_m3: float
    reinforcement_kg: float


@dataclass(frozen=True, slots=True)
class DocumentationPackage:
    """Execute the public DocumentationPackage operation for foundation drawings, schedules and technical documentation using explicit caller inputs."""
    package_id: str
    foundation: dict[str, Any]
    calculation: dict[str, Any]
    code_checks: dict[str, Any]
    bar_schedule: list[BarMark]
    quantities: QuantitySummary
    drawing_manifest: list[dict[str, str]]
    notes: list[str]
    traceability: dict[str, Any]
    qa: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Project the current value into the stable dict representation."""
        return asdict(self)
