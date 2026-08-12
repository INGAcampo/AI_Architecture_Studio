from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MemberCapacity:
    axial_n: float
    mx_nmm: float
    my_nmm: float
    shear_n: float
    torsion_nmm: float = 0.0
