from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MemberDemands:
    axial_n: float = 0.0
    mx_nmm: float = 0.0
    my_nmm: float = 0.0
    shear_n: float = 0.0
    torsion_nmm: float = 0.0
