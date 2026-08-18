"""Factory for creating valid, independently identified engineering objects."""
from __future__ import annotations
from .models import EngineeringObject, EngineeringState, Material, Load
from .identity import EngineeringIdentityService

class EngineeringObjectFactory:
    """Assemble object aggregates while defensively copying mutable caller data."""
    def create(self, *, object_type: str, name: str, geometry: dict,
               properties: dict, materials: list[Material], loads: list[Load],
               traceability: dict, metadata: dict | None = None) -> EngineeringObject:
        """Create a new aggregate with unique identity and defensive mutable copies."""
        return EngineeringObject(
            object_id=EngineeringIdentityService().new_id(),
            object_type=object_type,
            name=name,
            geometry=geometry,
            properties=dict(properties),
            materials=list(materials),
            loads=list(loads),
            state=EngineeringState(),
            metadata=dict(metadata or {}),
            traceability=dict(traceability),
        )
