"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .ids import ObjectId

@dataclass(slots=True)
class EngineeringObject:
    """Execute the public EngineeringObject operation for the Omega application core and shared runtime services using explicit caller inputs."""
    object_id: ObjectId = field(default_factory=ObjectId.new)
    object_type: str = "generic"
    name: str = ""
    geometry: dict[str, Any] = field(default_factory=dict)
    properties: dict[str, Any] = field(default_factory=dict)
    material_id: str | None = None
    layer: str = "0"
    classification: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    revision: int = 0

    def set_property(self, key: str, value: Any) -> None:
        """Execute set property for the Omega application core and shared runtime services with validated state transitions."""
        if self.properties.get(key) != value:
            self.properties[key] = value
            self.revision += 1
