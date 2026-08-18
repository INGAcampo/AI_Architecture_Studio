from __future__ import annotations

from .contracts import LoadCase, LoadCombination, PointLoad, UniformLoad


def combine_load_cases(
    cases: dict[str, LoadCase],
    combination: LoadCombination,
) -> LoadCase:
    combination.validate()

    uniform = []
    points = []

    for case_name, factor in combination.factors.items():
        if case_name not in cases:
            raise KeyError(case_name)

        case = cases[case_name]

        for load in case.uniform_loads:
            uniform.append(
                UniformLoad(
                    magnitude_n_per_m=load.magnitude_n_per_m * factor,
                    start_m=load.start_m,
                    end_m=load.end_m,
                )
            )

        for load in case.point_loads:
            points.append(
                PointLoad(
                    magnitude_n=load.magnitude_n * factor,
                    position_m=load.position_m,
                )
            )

    return LoadCase(
        name=combination.name,
        uniform_loads=tuple(uniform),
        point_loads=tuple(points),
    )
