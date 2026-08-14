import math

from structural_platform.combinations import combine_load_cases
from structural_platform.contracts import (
    BeamSection,
    LoadCase,
    LoadCombination,
    Material,
    PointLoad,
    SimplySupportedBeam,
    UniformLoad,
)
from structural_platform.solver import solve_simply_supported_beam
from structural_platform.units import gpa, kn, kn_per_m


def make_beam():
    return SimplySupportedBeam(
        length_m=6.0,
        material=Material(
            name="Steel",
            elastic_modulus_pa=gpa(200.0),
            density_kg_m3=7850.0,
        ),
        section=BeamSection(
            name="Test Section",
            area_m2=0.01,
            inertia_y_m4=8.0e-5,
        ),
    )


def test_uniform_load_reactions_and_moment_match_closed_form():
    beam = make_beam()
    w = kn_per_m(10.0)
    case = LoadCase(
        name="UDL",
        uniform_loads=(UniformLoad(w),),
    )

    result = solve_simply_supported_beam(beam, case, sample_count=1201)

    expected_reaction = w * beam.length_m / 2.0
    expected_moment = w * beam.length_m**2 / 8.0

    assert math.isclose(result.reaction_left_n, expected_reaction, rel_tol=1e-12)
    assert math.isclose(result.reaction_right_n, expected_reaction, rel_tol=1e-12)
    assert math.isclose(result.max_positive_moment_nm, expected_moment, rel_tol=1e-6)


def test_uniform_load_deflection_matches_closed_form():
    beam = make_beam()
    w = kn_per_m(8.0)
    case = LoadCase(name="UDL", uniform_loads=(UniformLoad(w),))

    result = solve_simply_supported_beam(beam, case, sample_count=1201)

    expected = (
        5.0
        * w
        * beam.length_m**4
        / (384.0 * beam.material.elastic_modulus_pa * beam.section.inertia_y_m4)
    )

    assert math.isclose(result.max_deflection_m, expected, rel_tol=1e-6)
    assert math.isclose(result.governing_position_m, beam.length_m / 2.0, rel_tol=1e-6)


def test_midspan_point_load_matches_closed_form():
    beam = make_beam()
    p = kn(30.0)
    case = LoadCase(
        name="POINT",
        point_loads=(PointLoad(p, beam.length_m / 2.0),),
    )

    result = solve_simply_supported_beam(beam, case, sample_count=1201)

    expected_reaction = p / 2.0
    expected_moment = p * beam.length_m / 4.0
    expected_deflection = (
        p
        * beam.length_m**3
        / (48.0 * beam.material.elastic_modulus_pa * beam.section.inertia_y_m4)
    )

    assert math.isclose(result.reaction_left_n, expected_reaction, rel_tol=1e-12)
    assert math.isclose(result.reaction_right_n, expected_reaction, rel_tol=1e-12)
    assert math.isclose(result.max_positive_moment_nm, expected_moment, rel_tol=1e-6)
    assert math.isclose(result.max_deflection_m, expected_deflection, rel_tol=1e-6)


def test_asymmetric_point_load_reactions_match_statics():
    beam = make_beam()
    p = kn(20.0)
    a = 2.0
    case = LoadCase(name="ASYM", point_loads=(PointLoad(p, a),))

    result = solve_simply_supported_beam(beam, case)

    expected_left = p * (beam.length_m - a) / beam.length_m
    expected_right = p * a / beam.length_m

    assert math.isclose(result.reaction_left_n, expected_left, rel_tol=1e-12)
    assert math.isclose(result.reaction_right_n, expected_right, rel_tol=1e-12)


def test_load_combination_scales_cases_deterministically():
    dead = LoadCase(
        name="D",
        uniform_loads=(UniformLoad(kn_per_m(5.0)),),
    )
    live = LoadCase(
        name="L",
        point_loads=(PointLoad(kn(10.0), 3.0),),
    )
    combo = LoadCombination(name="1.2D+1.6L", factors={"D": 1.2, "L": 1.6})

    combined = combine_load_cases({"D": dead, "L": live}, combo)

    assert combined.uniform_loads[0].magnitude_n_per_m == kn_per_m(6.0)
    assert combined.point_loads[0].magnitude_n == kn(16.0)


def test_invalid_beam_geometry_fails_closed():
    failed = False
    try:
        bad = SimplySupportedBeam(
            length_m=0.0,
            material=Material("Steel", gpa(200.0), 7850.0),
            section=BeamSection("Section", 0.01, 8.0e-5),
        )
        solve_simply_supported_beam(bad, LoadCase(name="EMPTY"))
    except ValueError:
        failed = True

    assert failed is True
