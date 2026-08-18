from __future__ import annotations

from .contracts import BridgeEntityRef, BridgeGeometryPayload
from .ifc_adapter import entity_ref
from .occt_adapter import topology_summary, triangulate
from .runtime import discover_runtime


class GeometryBimBridge:
    """Contract-first bridge between BIM semantics and geometry payloads."""

    @staticmethod
    def runtime():
        return discover_runtime()

    @staticmethod
    def from_ifc_entity_and_shape(
        ifc_entity,
        occt_shape,
        *,
        linear_deflection: float = 0.5,
        metadata: dict | None = None,
    ) -> BridgeGeometryPayload:
        ref = entity_ref(ifc_entity)
        topology = topology_summary(occt_shape)
        mesh = triangulate(occt_shape, linear_deflection=linear_deflection)

        return BridgeGeometryPayload(
            entity=ref,
            geometry_kind="OCCT_BREP",
            topology=topology,
            mesh=mesh,
            native_shape=occt_shape,
            metadata=dict(metadata or {}),
        )

    @staticmethod
    def from_aias_semantic_ref_and_shape(
        entity_id: str,
        entity_type: str,
        occt_shape,
        *,
        global_id: str | None = None,
        linear_deflection: float = 0.5,
        metadata: dict | None = None,
    ) -> BridgeGeometryPayload:
        ref = BridgeEntityRef(
            source="AIAS",
            entity_id=str(entity_id),
            entity_type=str(entity_type),
            global_id=global_id,
        )
        topology = topology_summary(occt_shape)
        mesh = triangulate(occt_shape, linear_deflection=linear_deflection)

        return BridgeGeometryPayload(
            entity=ref,
            geometry_kind="OCCT_BREP",
            topology=topology,
            mesh=mesh,
            native_shape=occt_shape,
            metadata=dict(metadata or {}),
        )
