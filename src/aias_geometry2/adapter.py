from __future__ import annotations
from dataclasses import dataclass
import importlib.util
from typing import Any
@dataclass(frozen=True, slots=True)
class KernelAvailability:
    native_aias: bool
    occt: bool
    production_ready: bool
    reason: str
@dataclass(frozen=True, slots=True)
class SemanticShape:
    shape_id: str
    kind: str
    parameters: dict[str, Any]
class GeometryKernelAdapter:
    """Safe facade: AIAS semantics remain usable while external OCCT is absent."""
    def availability(self) -> KernelAvailability:
        occt = importlib.util.find_spec("OCC") is not None
        return KernelAvailability(True, occt, False, "OCCT runtime unavailable" if not occt else "external runtime and license gates pending")
    def validate_semantic_shape(self, shape: SemanticShape) -> dict[str, Any]:
        if not shape.shape_id.strip(): raise ValueError("shape_id cannot be empty")
        if shape.kind not in {"line", "arc", "polyline", "spline", "surface", "solid"}: raise ValueError("unsupported_shape_kind:" + shape.kind)
        return {"valid": True, "shape_id": shape.shape_id, "kind": shape.kind, "backend": "aias-native-contract"}
