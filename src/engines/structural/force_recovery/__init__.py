from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MemberEndForces:
    member_id: str
    axial_start: float
    shear_start: float
    moment_start: float
    axial_end: float
    shear_end: float
    moment_end: float
    def __post_init__(self):
        if not self.member_id.strip():
            raise ValueError("member_id obligatorio")

class MemberForceRecovery:
    def recover_axial(self, stiffness, u_start, u_end):
        if stiffness <= 0:
            raise ValueError("stiffness debe ser positiva")
        force = stiffness * (u_end - u_start)
        return (-force, force)
    def envelope(self, items):
        if not items:
            raise ValueError("items no puede estar vacío")
        return {
            "axial_max": max(max(abs(i.axial_start), abs(i.axial_end)) for i in items),
            "shear_max": max(max(abs(i.shear_start), abs(i.shear_end)) for i in items),
            "moment_max": max(max(abs(i.moment_start), abs(i.moment_end)) for i in items),
        }
