"""Golden-thread projection from an engineering object to its evidence relationships."""
from __future__ import annotations
from .models import EngineeringObject

class TraceabilityEngine:
    """Build a stable requirement-to-knowledge-to-calculation-to-deliverable matrix."""
    def matrix(self, obj: EngineeringObject) -> dict:
        """Project requirements, knowledge, calculations, geometry and deliverables."""
        return {
            "object_id":obj.object_id,
            "object_type":obj.object_type,
            "version":obj.version,
            "requirements":obj.traceability.get("requirements",[]),
            "knowledge_units":obj.traceability.get("knowledge_units",[]),
            "calculation_units":obj.traceability.get("calculation_units",[]),
            "geometry_source":obj.traceability.get("geometry_source"),
            "deliverables":obj.traceability.get("deliverables",[]),
            "revision":obj.state.revision,
            "lifecycle":obj.state.lifecycle,
        }
