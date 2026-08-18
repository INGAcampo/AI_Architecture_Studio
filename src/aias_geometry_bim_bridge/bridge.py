from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True, slots=True)
class BridgeRecord:
    object_id: str
    ifc_class: str
    geometry_kind: str
    geometry_parameters: dict[str, Any]
    def to_payload(self) -> dict[str, Any]:
        return {"object_id":self.object_id,"ifc_class":self.ifc_class,"geometry":{"kind":self.geometry_kind,"parameters":dict(self.geometry_parameters)}}
class GeometryBimBridge:
    """Preserve identity while translating between semantic BIM and geometry payloads."""
    def export_record(self, record: BridgeRecord) -> dict[str, Any]:
        if not record.object_id.strip(): raise ValueError("object_id cannot be empty")
        if not record.ifc_class.startswith("Ifc"): raise ValueError("invalid_ifc_class")
        if not record.geometry_kind.strip(): raise ValueError("geometry_kind cannot be empty")
        return record.to_payload()
    def import_record(self, payload: dict[str, Any]) -> BridgeRecord:
        geometry = payload.get("geometry") or {}
        record = BridgeRecord(str(payload.get("object_id", "")), str(payload.get("ifc_class", "")), str(geometry.get("kind", "")), dict(geometry.get("parameters") or {}))
        self.export_record(record)
        return record
    def round_trip(self, record: BridgeRecord) -> dict[str, Any]:
        imported = self.import_record(self.export_record(record))
        return {"stable_identity": imported.object_id == record.object_id, "same_ifc_class": imported.ifc_class == record.ifc_class, "same_geometry": imported.geometry_kind == record.geometry_kind and imported.geometry_parameters == record.geometry_parameters}
