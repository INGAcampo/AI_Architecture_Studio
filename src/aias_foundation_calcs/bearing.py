"""Service bearing-pressure, eccentricity and kern calculations for rectangular footings."""
from __future__ import annotations
from .models import FoundationInput, LoadCase, BearingResult

class BearingPressureEngine:
    """Calculate average and extreme soil pressures including biaxial load eccentricity."""
    def calculate(self, data: FoundationInput, load: LoadCase) -> BearingResult:
        """Compute self-weight, eccentricities, extreme pressures and service flags."""
        b,l=data.width_m,data.length_m
        area=b*l
        self_weight=area*data.thickness_m*data.concrete_unit_weight_kn_m3
        p=load.axial_kn+self_weight
        if p <= 0:
            raise ValueError("non_positive_vertical_resultant")
        ex=load.moment_y_knm/p
        ey=load.moment_x_knm/p
        qavg=p/area
        qx=6*load.moment_y_knm/(l*b*b)
        qy=6*load.moment_x_knm/(b*l*l)
        qmax=qavg+abs(qx)+abs(qy)
        qmin=qavg-abs(qx)-abs(qy)
        kern_ok=abs(ex)<=b/6 and abs(ey)<=l/6 and qmin>=0
        allowable_ok=qmax<=data.allowable_bearing_pressure_kpa and qmin>=0
        return BearingResult(qavg,qmax,qmin,ex,ey,kern_ok,allowable_ok)
