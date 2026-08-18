from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BraceTensionResult:
    yielding_capacity: float
    rupture_capacity: float
    design_capacity: float
    governing_mode: str

class BraceTensionEngine:
    def calculate(self, profile, material, net_area_factor=0.85, phi_y=0.9, phi_u=0.75):
        yielding=phi_y*material.fy*profile.area
        rupture=phi_u*material.fu*profile.area*net_area_factor
        if yielding<=rupture:
            return BraceTensionResult(yielding,rupture,yielding,"gross_section_yielding")
        return BraceTensionResult(yielding,rupture,rupture,"net_section_rupture")
