from __future__ import annotations

from dataclasses import dataclass

from .model import StructuralMaterial, StructuralMember, StructuralProfile


@dataclass(frozen=True, slots=True)
class StructuralMemberQuantities:
    length: float
    area: float
    volume: float
    mass: float
    weight: float
    midpoint: tuple[float, float, float]
    inertia_y: float
    inertia_z: float


class StructuralQuantityCalculator:
    GRAVITY = 9.80665

    def calculate(
        self,
        member: StructuralMember,
        profile: StructuralProfile,
        material: StructuralMaterial,
    ) -> StructuralMemberQuantities:
        volume = profile.area * member.length
        mass = volume * material.density
        midpoint = member.midpoint
        return StructuralMemberQuantities(
            length=member.length,
            area=profile.area,
            volume=volume,
            mass=mass,
            weight=mass * self.GRAVITY,
            midpoint=(midpoint.x, midpoint.y, midpoint.z),
            inertia_y=profile.inertia_y,
            inertia_z=profile.inertia_z,
        )
