from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any


class StructuralElementKind(str, Enum):
    COLUMN = "column"
    BEAM = "beam"
    BRACE = "brace"
    GIRDER = "girder"
    TRUSS_MEMBER = "truss_member"


class StructuralMaterialKind(str, Enum):
    STEEL = "steel"
    CONCRETE = "concrete"
    WOOD = "wood"
    ALUMINUM = "aluminum"
    COMPOSITE = "composite"
    GENERIC = "generic"


class ProfileShape(str, Enum):
    I = "I"
    H = "H"
    C = "C"
    L = "L"
    RHS = "RHS"
    CHS = "CHS"
    RECTANGULAR = "rectangular"
    CIRCULAR = "circular"
    GENERIC = "generic"


@dataclass(frozen=True, slots=True)
class StructuralPoint:
    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.x, self.y, self.z)):
            raise ValueError("Las coordenadas deben ser finitas")


@dataclass(frozen=True, slots=True)
class StructuralMaterial:
    material_id: str
    name: str
    kind: StructuralMaterialKind
    density: float
    elastic_modulus: float | None = None
    yield_strength: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.material_id.strip():
            raise ValueError("material_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if self.density <= 0:
            raise ValueError("density debe ser positiva")
        if self.elastic_modulus is not None and self.elastic_modulus <= 0:
            raise ValueError("elastic_modulus debe ser positivo")
        if self.yield_strength is not None and self.yield_strength <= 0:
            raise ValueError("yield_strength debe ser positivo")


@dataclass(frozen=True, slots=True)
class StructuralProfile:
    profile_id: str
    name: str
    shape: ProfileShape
    area: float
    inertia_y: float
    inertia_z: float
    torsion_constant: float = 0.0
    section_modulus_y: float = 0.0
    section_modulus_z: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.profile_id.strip():
            raise ValueError("profile_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if self.area <= 0:
            raise ValueError("area debe ser positiva")
        if min(self.inertia_y, self.inertia_z, self.torsion_constant,
               self.section_modulus_y, self.section_modulus_z) < 0:
            raise ValueError("Las propiedades de sección no pueden ser negativas")


@dataclass(slots=True)
class StructuralMember:
    member_id: str
    kind: StructuralElementKind
    start: StructuralPoint
    end: StructuralPoint
    profile_id: str
    material_id: str
    rotation_degrees: float = 0.0
    release_start: tuple[bool, bool, bool, bool, bool, bool] = (False,) * 6
    release_end: tuple[bool, bool, bool, bool, bool, bool] = (False,) * 6
    eccentricity_start: StructuralPoint = StructuralPoint(0.0, 0.0, 0.0)
    eccentricity_end: StructuralPoint = StructuralPoint(0.0, 0.0, 0.0)
    revision: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.member_id.strip():
            raise ValueError("member_id no puede estar vacío")
        if not self.profile_id.strip() or not self.material_id.strip():
            raise ValueError("profile_id y material_id son obligatorios")
        if self.length <= 0:
            raise ValueError("El elemento debe tener longitud positiva")

    @property
    def length(self) -> float:
        return (
            (self.end.x - self.start.x) ** 2
            + (self.end.y - self.start.y) ** 2
            + (self.end.z - self.start.z) ** 2
        ) ** 0.5

    @property
    def midpoint(self) -> StructuralPoint:
        return StructuralPoint(
            (self.start.x + self.end.x) / 2.0,
            (self.start.y + self.end.y) / 2.0,
            (self.start.z + self.end.z) / 2.0,
        )

    def touch(self) -> int:
        self.revision += 1
        return self.revision
