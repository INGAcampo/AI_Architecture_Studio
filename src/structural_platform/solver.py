from __future__ import annotations

from dataclasses import dataclass

from .contracts import LoadCase, PointLoad, SimplySupportedBeam, UniformLoad


@dataclass(frozen=True)
class BeamResult:
    reaction_left_n: float
    reaction_right_n: float
    max_positive_moment_nm: float
    max_deflection_m: float
    governing_position_m: float


def _full_span_uniform_load(load: UniformLoad, length: float) -> float:
    end = length if load.end_m is None else load.end_m
    if abs(load.start_m) > 1e-12 or abs(end - length) > 1e-12:
        raise NotImplementedError(
            "STRUCTURAL-001 supports full-span uniform loads only"
        )
    return float(load.magnitude_n_per_m)


def _validate_point(load: PointLoad, length: float) -> None:
    if load.position_m < 0 or load.position_m > length:
        raise ValueError("point load position is outside beam span")


def _reactions(beam: SimplySupportedBeam, case: LoadCase) -> tuple[float, float]:
    length = beam.length_m
    total_load = 0.0
    moment_about_left = 0.0

    for load in case.uniform_loads:
        w = _full_span_uniform_load(load, length)
        resultant = w * length
        total_load += resultant
        moment_about_left += resultant * length / 2.0

    for load in case.point_loads:
        _validate_point(load, length)
        total_load += load.magnitude_n
        moment_about_left += load.magnitude_n * load.position_m

    right = moment_about_left / length
    left = total_load - right
    return left, right


def _bending_moment(
    x: float,
    beam: SimplySupportedBeam,
    case: LoadCase,
    reaction_left: float,
) -> float:
    moment = reaction_left * x

    for load in case.uniform_loads:
        w = _full_span_uniform_load(load, beam.length_m)
        moment -= w * x * x / 2.0

    for load in case.point_loads:
        if x >= load.position_m:
            moment -= load.magnitude_n * (x - load.position_m)

    return moment


def _deflection_full_span_udl(
    x: float,
    length: float,
    w: float,
    elastic_modulus: float,
    inertia: float,
) -> float:
    return (
        w
        * x
        * (length**3 - 2.0 * length * x**2 + x**3)
        / (24.0 * elastic_modulus * inertia)
    )


def _deflection_point_load(
    x: float,
    length: float,
    load: PointLoad,
    elastic_modulus: float,
    inertia: float,
) -> float:
    p = load.magnitude_n
    a = load.position_m
    b = length - a

    if a <= 0 or b <= 0:
        return 0.0

    if x <= a:
        return (
            p
            * b
            * x
            * (length**2 - b**2 - x**2)
            / (6.0 * length * elastic_modulus * inertia)
        )

    return (
        p
        * a
        * (length - x)
        * (length**2 - a**2 - (length - x) ** 2)
        / (6.0 * length * elastic_modulus * inertia)
    )


def solve_simply_supported_beam(
    beam: SimplySupportedBeam,
    case: LoadCase,
    *,
    sample_count: int = 1001,
) -> BeamResult:
    beam.validate()
    if sample_count < 11:
        raise ValueError("sample_count must be at least 11")

    left, right = _reactions(beam, case)
    length = beam.length_m
    e = beam.material.elastic_modulus_pa
    inertia = beam.section.inertia_y_m4

    max_moment = float("-inf")
    max_deflection = float("-inf")
    governing_position = 0.0

    for index in range(sample_count):
        x = length * index / (sample_count - 1)
        moment = _bending_moment(x, beam, case, left)

        deflection = 0.0
        for load in case.uniform_loads:
            w = _full_span_uniform_load(load, length)
            deflection += _deflection_full_span_udl(x, length, w, e, inertia)
        for load in case.point_loads:
            deflection += _deflection_point_load(x, length, load, e, inertia)

        if moment > max_moment:
            max_moment = moment

        if deflection > max_deflection:
            max_deflection = deflection
            governing_position = x

    return BeamResult(
        reaction_left_n=left,
        reaction_right_n=right,
        max_positive_moment_nm=max_moment,
        max_deflection_m=max_deflection,
        governing_position_m=governing_position,
    )
