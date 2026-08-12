"""Boundary adapters connecting engineering objects to geometry, calculation, knowledge and enterprise registries."""
from __future__ import annotations
from pathlib import Path
import json
from .models import EngineeringObject

class GeometryKernelAdapter:
    """Expose deterministic planar-area operations required by engineering consumers."""
    def area(self, obj: EngineeringObject) -> float:
        """Return area for supported rectangle or circle geometry payloads."""
        g=obj.geometry
        if g.get("type")=="Rectangle":
            return float(g["width"])*float(g["length"])
        if g.get("type")=="Circle":
            import math
            return math.pi*float(g["radius"])**2
        raise ValueError("unsupported_geometry")

class ECFAdapter:
    """Translate object loads and geometry into Enterprise Calculation Framework inputs."""
    def total_vertical_load(self, obj: EngineeringObject) -> float:
        """Sum magnitudes of loads acting in the negative global vertical direction."""
        return sum(load.magnitude for load in obj.loads if load.direction[2] < 0)

    def bearing_pressure(self, obj: EngineeringObject) -> float:
        """Divide total downward load by positive supported footprint area."""
        area=GeometryKernelAdapter().area(obj)
        if area <= 0:
            raise ValueError("non_positive_area")
        return self.total_vertical_load(obj)/area

class AEKSAdapter:
    """Load and minimally validate versioned AEKS engineering knowledge units."""
    def load_knowledge_unit(self, path: Path) -> dict:
        """Load JSON knowledge only when its engineering knowledge identifier exists."""
        data=json.loads(path.read_text(encoding="utf-8"))
        if "eku_id" not in data:
            raise ValueError("invalid_eku")
        return data

class EnterpriseRegistryAdapter:
    """Project an engineering object into the stable enterprise-asset contract."""
    def record(self, obj: EngineeringObject) -> dict:
        """Create an enterprise asset record from object identity and lifecycle state."""
        return {
            "asset_id":obj.object_id,
            "asset_type":"ENGINEERING_OBJECT",
            "object_type":obj.object_type,
            "version":obj.version,
            "status":obj.state.lifecycle,
        }
