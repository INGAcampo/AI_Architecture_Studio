from __future__ import annotations
from dataclasses import dataclass, field
import importlib.util
from typing import Any
@dataclass(frozen=True, slots=True)
class IfcAvailability:
    native_aias: bool
    ifcopenshell: bool
    production_ready: bool
    reason: str
@dataclass(frozen=True, slots=True)
class BimEntity:
    entity_id: str
    ifc_class: str
    properties: dict[str, Any] = field(default_factory=dict)
    relationships: tuple[str, ...] = ()
class BimNativeAdapter:
    """AIAS semantic BIM boundary; external IFC runtime is optional and explicit."""
    def availability(self) -> IfcAvailability:
        available = importlib.util.find_spec("ifcopenshell") is not None
        return IfcAvailability(True, available, False, "IfcOpenShell runtime unavailable" if not available else "schema and license gates pending")
    def validate_entity(self, entity: BimEntity) -> dict[str, Any]:
        if not entity.entity_id.strip(): raise ValueError("entity_id cannot be empty")
        if not entity.ifc_class.startswith("Ifc"): raise ValueError("invalid_ifc_class")
        return {"valid": True, "entity_id": entity.entity_id, "ifc_class": entity.ifc_class, "backend": "aias-semantic-contract"}
