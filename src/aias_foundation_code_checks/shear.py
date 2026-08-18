"""One-way and punching shear capacity checks using traceable pack parameters."""
from __future__ import annotations
import math
from .models import CodePack, DesignInput, CheckResult

class ShearCheckEngine:
    """Compare factored shear demands with concrete capacities and equation identifiers."""
    def one_way(self, demand_kn: float, strip_width_m: float, data: DesignInput, pack: CodePack, axis: str) -> CheckResult:
        """Check one-way shear demand against parameter-driven concrete capacity."""
        coeff=pack.parameters["one_way_shear_coefficient"]
        phi=pack.parameters["phi_one_way_shear"]
        capacity_kn=phi*coeff*math.sqrt(data.concrete_strength_mpa)*(strip_width_m*1000)*(data.effective_depth_m*1000)/1000
        util=demand_kn/capacity_kn if capacity_kn>0 else float("inf")
        return CheckResult(
            f"ONE_WAY_SHEAR_{axis}", demand_kn, capacity_kn, util, util<=1.0, "kN",
            "GEN-RC-OWS-001", ["Parameter-driven reference equation; requires verified AEKS code pack."]
        )

    def punching(self, demand_kn: float, data: DesignInput, pack: CodePack) -> CheckResult:
        """Check punching demand on the effective-depth critical perimeter."""
        coeff=pack.parameters["punching_shear_coefficient"]
        phi=pack.parameters["phi_punching"]
        perimeter_m=2*((data.column_width_m+data.effective_depth_m)+(data.column_depth_m+data.effective_depth_m))
        capacity_kn=phi*coeff*math.sqrt(data.concrete_strength_mpa)*(perimeter_m*1000)*(data.effective_depth_m*1000)/1000
        util=demand_kn/capacity_kn if capacity_kn>0 else float("inf")
        return CheckResult(
            "PUNCHING_SHEAR", demand_kn, capacity_kn, util, util<=1.0, "kN",
            "GEN-RC-PUNCH-001", ["Parameter-driven reference equation; requires verified AEKS code pack."]
        )
