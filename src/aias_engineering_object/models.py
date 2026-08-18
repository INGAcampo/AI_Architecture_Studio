"""Canonical data contracts composing the universal AIAS engineering object."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class Material:
    """Versioned engineering material with numeric properties, units and provenance."""
    material_id: str
    name: str
    category: str
    properties: dict[str, float]
    units: dict[str, str]
    source: str = "AIAS"
    version: str = "1.0.0"

@dataclass(slots=True)
class Load:
    """Applied load carrying magnitude, unit, direction and extensible metadata."""
    load_id: str
    load_type: str
    magnitude: float
    unit: str
    direction: tuple[float, float, float] = (0.0, 0.0, -1.0)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class EngineeringState:
    """Lifecycle, calculation, quality, documentation and revision state vector."""
    lifecycle: str = "DRAFT"
    calculation_status: str = "NOT_STARTED"
    qa_status: str = "NOT_STARTED"
    documentation_status: str = "NOT_STARTED"
    revision: int = 0

@dataclass(slots=True)
class EngineeringObject:
    """Traceable aggregate joining geometry, properties, materials, loads and state."""
    object_id: str
    object_type: str
    name: str
    geometry: dict[str, Any]
    properties: dict[str, Any]
    materials: list[Material]
    loads: list[Load]
    state: EngineeringState
    metadata: dict[str, Any]
    traceability: dict[str, Any]
    version: str = "1.0.0"

    def to_dict(self) -> dict[str, Any]:
        """Recursively serialize the complete engineering-object aggregate."""
        return asdict(self)
