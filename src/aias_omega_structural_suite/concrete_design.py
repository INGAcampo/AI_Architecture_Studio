"""Reference rectangular reinforced-concrete beam flexural sizing."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ConcreteBeamCheck:
    """Required steel, minimum steel and governing reinforcement result."""
    nominal_moment_nm: float
    design_moment_nm: float
    utilization: float
    adequate: bool

class RectangularConcreteBeamDesign:
    """Estimate longitudinal steel using explicit material and section inputs."""
    def flexural_check(self, width_m, effective_depth_m, steel_area_m2, fy_pa, fc_pa, demand_moment_nm, phi=0.9):
        """Execute the public RectangularConcreteBeamDesign.flexural_check operation for the Omega structural analysis and design suite using explicit caller inputs."""
        if min(width_m,effective_depth_m,steel_area_m2,fy_pa,fc_pa,phi) <= 0:
            raise ValueError("Invalid concrete design input.")
        a = steel_area_m2 * fy_pa / (0.85 * fc_pa * width_m)
        mn = steel_area_m2 * fy_pa * (effective_depth_m - a/2)
        design = phi * mn
        u = abs(demand_moment_nm) / design
        return ConcreteBeamCheck(mn, design, u, u <= 1.0)
