"""Traceable generic shear, punching and flexural demand calculations."""
from __future__ import annotations
from .models import FoundationInput, LoadCase, BearingResult, DemandResult

class StructuralDemandEngine:
    """Estimate conservative footing demands from maximum uniform soil pressure."""
    def calculate(self, data: FoundationInput, load: LoadCase, bearing: BearingResult) -> DemandResult:
        """Estimate shear, punching and flexural demands from conservative pressure."""
        b,l=data.width_m,data.length_m
        cx,cy=data.column_width_m,data.column_depth_m
        d=max(data.thickness_m-data.cover_m,1e-6)
        projection_x=max((b-cx)/2,0.0)
        projection_y=max((l-cy)/2,0.0)

        # Conservative uniform-pressure demand model for traceable generic calculations.
        q=max(bearing.q_max_kpa,0.0)

        one_way_x=q*l*max(projection_x-d,0.0)
        one_way_y=q*b*max(projection_y-d,0.0)

        critical_b=max(cx+d,0.0)
        critical_l=max(cy+d,0.0)
        punching_area=max(b*l-critical_b*critical_l,0.0)
        punching=q*punching_area

        moment_x=q*l*projection_x**2/2
        moment_y=q*b*projection_y**2/2
        return DemandResult(one_way_x,one_way_y,punching,moment_x,moment_y)
