from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SteelMember:
    member_id: str
    length_m: float
    kx: float = 1.0
    ky: float = 1.0
    unbraced_length_m: float = 0.0
