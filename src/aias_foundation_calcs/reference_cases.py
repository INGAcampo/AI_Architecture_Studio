"""Reproducible footing input and acceptance cases for calculation regression."""
from .models import FoundationInput,LoadCase,LoadCombination
from .engine import FoundationCalculationEngine

def reference_input():
    """Build the canonical two-combination rectangular-footing example in SI units."""
    return FoundationInput(
        width_m=2.0,length_m=2.5,thickness_m=0.5,
        column_width_m=0.4,column_depth_m=0.4,
        allowable_bearing_pressure_kpa=250.0,
        soil_modulus_mpa=25.0,
        load_cases={
            "D":LoadCase("D",600.0,20.0,10.0),
            "L":LoadCase("L",200.0,10.0,5.0),
        },
        combinations=[
            LoadCombination("SVC-1",{"D":1.0,"L":1.0}),
            LoadCombination("SVC-2",{"D":1.0,"L":0.5}),
        ],
    )

def run_reference_cases():
    """Verify combinations, pressures, demands, settlement and review boundaries."""
    pkg=FoundationCalculationEngine().calculate(reference_input())
    r1=pkg.results[0]
    return [
        {"id":"FCE-000001","passed":len(pkg.results)==2},
        {"id":"FCE-000002","passed":r1.resultant.axial_kn==800.0},
        {"id":"FCE-000003","passed":r1.bearing.q_avg_kpa>160.0},
        {"id":"FCE-000004","passed":r1.bearing.q_max_kpa>r1.bearing.q_avg_kpa},
        {"id":"FCE-000005","passed":r1.bearing.q_min_kpa<r1.bearing.q_avg_kpa},
        {"id":"FCE-000006","passed":r1.demands.punching_shear_kn>0},
        {"id":"FCE-000007","passed":r1.settlement.available},
        {"id":"FCE-000008","passed":pkg.qa["human_review_required"]},
    ]
