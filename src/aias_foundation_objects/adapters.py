"""Adapters from foundation objects to shared object, geometry and calculation contracts."""
from __future__ import annotations
from .models import FoundationObject

class EngineeringObjectAdapter:
    """Project a foundation into the universal engineering-object payload."""
    def to_engineering_object_payload(self, obj: FoundationObject) -> dict:
        """Map a foundation into shared identity, geometry, properties, loads and traceability."""
        return {
            "object_id": obj.object_id,
            "object_type": obj.foundation_type.value,
            "name": obj.name,
            "geometry": obj.to_dict()["geometry"],
            "properties": {
                "concrete_strength_mpa": obj.concrete_strength_mpa,
                "steel_yield_strength_mpa": obj.steel_yield_strength_mpa,
                "cover_m": obj.cover_m,
            },
            "loads": [
                {"load_id": s.support_id, "type":"AXIAL", "magnitude_kn":s.axial_load_kn}
                for s in obj.supports
            ],
            "traceability": obj.traceability,
        }

class GeometryKernelAdapter:
    """Expose the foundation footprint to the shared geometry kernel."""
    def footprint(self, obj: FoundationObject) -> dict:
        """Return rectangular footprint dimensions, area and units for geometry consumers."""
        return {
            "type":"Rectangle2D",
            "width":obj.geometry.width_m,
            "length":obj.geometry.length_m,
            "area":obj.geometry.area_m2,
            "unit":"m",
        }

class ECFAdapter:
    """Extract area, service load and allowable pressure calculation inputs."""
    def calculation_inputs(self, obj: FoundationObject) -> dict:
        """Extract area, total service load and allowable soil pressure for calculation."""
        return {
            "area_m2":obj.geometry.area_m2,
            "total_load_kn":sum(s.axial_load_kn for s in obj.supports),
            "allowable_pressure_kpa":obj.soil.allowable_bearing_pressure_kpa,
        }
