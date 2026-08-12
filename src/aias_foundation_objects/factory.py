"""Factory methods for all supported shallow-foundation object families."""
from __future__ import annotations
import uuid
from .models import FoundationObject, FoundationGeometry, SoilProfile, ColumnSupport
from .enums import FoundationType, ShapeType

class FoundationFactory:
    """Issue stable identities and assemble traceable foundation aggregates."""
    def _id(self) -> str:
        return "FND-" + uuid.uuid4().hex[:10].upper()

    def isolated(self, *, name: str, width_m: float, length_m: float, thickness_m: float,
                 soil: SoilProfile, support: ColumnSupport, concrete_strength_mpa: float = 30.0,
                 steel_yield_strength_mpa: float = 420.0, cover_m: float = 0.075) -> FoundationObject:
        """Create a one-support isolated footing and infer square or rectangular shape."""
        shape = ShapeType.SQUARE if abs(width_m-length_m) < 1e-12 else ShapeType.RECTANGULAR
        return FoundationObject(
            self._id(), FoundationType.ISOLATED, name,
            FoundationGeometry(shape, width_m, length_m, thickness_m),
            soil, [support], concrete_strength_mpa, steel_yield_strength_mpa, cover_m,
            traceability={"source":"ECP-000001A","consumer":"ECP-000001B"}
        )

    def combined(self, *, name: str, width_m: float, length_m: float, thickness_m: float,
                 soil: SoilProfile, supports: list[ColumnSupport], concrete_strength_mpa: float = 30.0,
                 steel_yield_strength_mpa: float = 420.0, cover_m: float = 0.075) -> FoundationObject:
        """Create a combined footing and require at least two column supports."""
        if len(supports) < 2:
            raise ValueError("combined_foundation_requires_two_supports")
        return FoundationObject(
            self._id(), FoundationType.COMBINED, name,
            FoundationGeometry(ShapeType.RECTANGULAR, width_m, length_m, thickness_m),
            soil, supports, concrete_strength_mpa, steel_yield_strength_mpa, cover_m,
            traceability={"source":"ECP-000001A","consumer":"ECP-000001B"}
        )

    def strip(self, *, name: str, width_m: float, length_m: float, thickness_m: float,
              soil: SoilProfile, line_load_kn_m: float, concrete_strength_mpa: float = 30.0,
              steel_yield_strength_mpa: float = 420.0, cover_m: float = 0.075) -> FoundationObject:
        """Create a strip footing and convert line load into an equivalent support load."""
        support = ColumnSupport("WALL-LINE", length_m/2, width_m/2, length_m, 0.20, line_load_kn_m*length_m)
        return FoundationObject(
            self._id(), FoundationType.STRIP, name,
            FoundationGeometry(ShapeType.RECTANGULAR, width_m, length_m, thickness_m),
            soil, [support], concrete_strength_mpa, steel_yield_strength_mpa, cover_m,
            metadata={"line_load_kn_m": line_load_kn_m},
            traceability={"source":"ECP-000001A","consumer":"ECP-000001B"}
        )

    def mat(self, *, name: str, width_m: float, length_m: float, thickness_m: float,
            soil: SoilProfile, supports: list[ColumnSupport], concrete_strength_mpa: float = 30.0,
            steel_yield_strength_mpa: float = 420.0, cover_m: float = 0.075) -> FoundationObject:
        """Create a mat foundation supporting an arbitrary column collection."""
        return FoundationObject(
            self._id(), FoundationType.MAT, name,
            FoundationGeometry(ShapeType.RECTANGULAR, width_m, length_m, thickness_m),
            soil, supports, concrete_strength_mpa, steel_yield_strength_mpa, cover_m,
            traceability={"source":"ECP-000001A","consumer":"ECP-000001B"}
        )

    def pedestal(self, *, name: str, width_m: float, length_m: float, height_m: float,
                 soil: SoilProfile, support: ColumnSupport, concrete_strength_mpa: float = 30.0,
                 steel_yield_strength_mpa: float = 420.0, cover_m: float = 0.05) -> FoundationObject:
        """Create a concrete pedestal represented by rectangular plan and height."""
        return FoundationObject(
            self._id(), FoundationType.PEDESTAL, name,
            FoundationGeometry(ShapeType.RECTANGULAR, width_m, length_m, height_m),
            soil, [support], concrete_strength_mpa, steel_yield_strength_mpa, cover_m,
            traceability={"source":"ECP-000001A","consumer":"ECP-000001B"}
        )

    def foundation_beam(self, *, name: str, width_m: float, length_m: float, depth_m: float,
                        soil: SoilProfile, supports: list[ColumnSupport],
                        concrete_strength_mpa: float = 30.0, steel_yield_strength_mpa: float = 420.0,
                        cover_m: float = 0.05) -> FoundationObject:
        """Create a grade or foundation beam joining supplied supports."""
        return FoundationObject(
            self._id(), FoundationType.FOUNDATION_BEAM, name,
            FoundationGeometry(ShapeType.RECTANGULAR, width_m, length_m, depth_m),
            soil, supports, concrete_strength_mpa, steel_yield_strength_mpa, cover_m,
            traceability={"source":"ECP-000001A","consumer":"ECP-000001B"}
        )
