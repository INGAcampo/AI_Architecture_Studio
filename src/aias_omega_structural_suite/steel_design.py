"""Reference steel member demand-capacity verification."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SteelCheck:
    """Steel utilization ratio and pass/fail outcome."""
    axial_utilization: float
    bending_utilization: float
    interaction_utilization: float
    adequate: bool

class SteelMemberDesign:
    """Compare axial and flexural demands with supplied reference capacities."""
    def check(self, axial_n, moment_nm, area_m2, section_modulus_m3, fy_pa, phi=0.9):
        """Validate check for the Omega structural analysis and design suite and report explicit issues."""
        if min(area_m2, section_modulus_m3, fy_pa, phi) <= 0:
            raise ValueError("Invalid steel design input.")
        pn = phi * area_m2 * fy_pa
        mn = phi * section_modulus_m3 * fy_pa
        ua = abs(axial_n) / pn
        um = abs(moment_nm) / mn
        ui = ua + um
        return SteelCheck(ua, um, ui, ui <= 1.0)
