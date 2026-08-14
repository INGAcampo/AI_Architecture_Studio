from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Material:
    name: str
    elastic_modulus_pa: float
    density_kg_m3: float

    def validate(self) -> None:
        if self.elastic_modulus_pa <= 0:
            raise ValueError("elastic_modulus_pa must be positive")
        if self.density_kg_m3 <= 0:
            raise ValueError("density_kg_m3 must be positive")


@dataclass(frozen=True)
class BeamSection:
    name: str
    area_m2: float
    inertia_y_m4: float

    def validate(self) -> None:
        if self.area_m2 <= 0:
            raise ValueError("area_m2 must be positive")
        if self.inertia_y_m4 <= 0:
            raise ValueError("inertia_y_m4 must be positive")


@dataclass(frozen=True)
class UniformLoad:
    magnitude_n_per_m: float
    start_m: float = 0.0
    end_m: float | None = None


@dataclass(frozen=True)
class PointLoad:
    magnitude_n: float
    position_m: float


@dataclass(frozen=True)
class LoadCase:
    name: str
    uniform_loads: tuple[UniformLoad, ...] = ()
    point_loads: tuple[PointLoad, ...] = ()


@dataclass(frozen=True)
class LoadCombination:
    name: str
    factors: dict[str, float] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.factors:
            raise ValueError("load combination requires at least one factor")


@dataclass(frozen=True)
class SimplySupportedBeam:
    length_m: float
    material: Material
    section: BeamSection

    def validate(self) -> None:
        if self.length_m <= 0:
            raise ValueError("length_m must be positive")
        self.material.validate()
        self.section.validate()
