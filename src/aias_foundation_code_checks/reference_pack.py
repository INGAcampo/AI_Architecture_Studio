"""Non-normative generic pack and input fixture for safe framework validation."""
from .models import CodePack, DesignInput

def generic_reference_pack():
    """Build a clearly labelled reference-only reinforced-concrete parameter pack."""
    return CodePack(
        code_id="AIAS-GENERIC-RC-FOUNDATION-1.0",
        title="AIAS Generic Reinforced Concrete Foundation Reference Pack",
        jurisdiction="NONE",
        edition="1.0",
        legal_status="REFERENCE_ONLY",
        parameters={
            "phi_flexure":0.90,
            "phi_one_way_shear":0.75,
            "phi_punching":0.75,
            "min_reinforcement_ratio":0.0018,
            "max_bar_spacing_mm":300.0,
            "one_way_shear_coefficient":0.17,
            "punching_shear_coefficient":0.33,
            "steel_stress_limit_factor":1.0,
            "minimum_cover_mm":75.0,
            "minimum_thickness_mm":300.0
        },
        applicability=["ISOLATED_FOOTING","COMBINED_FOOTING","STRIP_FOOTING","MAT_FOUNDATION"],
        source_metadata={
            "status":"NON_NORMATIVE_REFERENCE",
            "warning":"Not a legal design standard. Replace with verified AEKS code pack."
        }
    )

def reference_input():
    """Build a deterministic footing design-input fixture for acceptance tests."""
    return DesignInput(
        width_m=2.0,length_m=2.5,thickness_m=0.55,effective_depth_m=0.45,
        column_width_m=0.4,column_depth_m=0.4,
        concrete_strength_mpa=30.0,steel_yield_strength_mpa=420.0,cover_m=0.075,
        factored_moment_x_knm=120.0,factored_moment_y_knm=95.0,
        factored_one_way_shear_x_kn=180.0,factored_one_way_shear_y_kn=150.0,
        factored_punching_shear_kn=550.0
    )
