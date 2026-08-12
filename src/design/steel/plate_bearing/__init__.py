from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PlateBearingResult:
    nominal_capacity:float
    design_capacity:float
    edge_distance:float
    spacing:float

class PlateBearingEngine:
    def calculate(self,bolt_diameter,plate_thickness,plate_fu,edge_distance,spacing,phi=0.75):
        lc_edge=max(edge_distance-bolt_diameter/2.0,0.0)
        lc_spacing=max(spacing-bolt_diameter,0.0)
        rn_edge=min(1.2*lc_edge*plate_thickness*plate_fu,2.4*bolt_diameter*plate_thickness*plate_fu)
        rn_spacing=min(1.2*lc_spacing*plate_thickness*plate_fu,2.4*bolt_diameter*plate_thickness*plate_fu)
        nominal=min(rn_edge,rn_spacing)
        return PlateBearingResult(nominal,phi*nominal,edge_distance,spacing)
