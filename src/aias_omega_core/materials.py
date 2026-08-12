"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(slots=True)
class Material:
    """Execute the public Material operation for the Omega application core and shared runtime services using explicit caller inputs."""
    material_id: str
    name: str
    category: str
    properties: dict[str, float] = field(default_factory=dict)

class MaterialLibrary:
    """Execute the public MaterialLibrary operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._materials: dict[str, Material] = {}

    def add(self, material: Material) -> None:
        """Add add to the Omega application core and shared runtime services while enforcing identity constraints."""
        if material.material_id in self._materials:
            raise ValueError(material.material_id)
        self._materials[material.material_id] = material

    def get(self, material_id: str) -> Material:
        """Return get from the Omega application core and shared runtime services using deterministic lookup rules."""
        return self._materials[material_id]

    def all(self) -> tuple[Material, ...]:
        """Execute the public MaterialLibrary.all operation for the Omega application core and shared runtime services using explicit caller inputs."""
        return tuple(self._materials.values())
