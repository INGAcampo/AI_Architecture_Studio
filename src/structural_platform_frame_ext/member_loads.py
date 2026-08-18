from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UniformMemberLoad:
    wy_n_per_m: float


def fixed_end_forces_local(load: UniformMemberLoad, length_m: float):
    if length_m <= 0:
        raise ValueError("length_m must be positive")

    w=float(load.wy_n_per_m)
    l=float(length_m)

    return (
        0.0,
        -w*l/2.0,
        -w*l*l/12.0,
        0.0,
        -w*l/2.0,
        w*l*l/12.0,
    )


def recover_local_end_forces(
    local_stiffness,
    local_displacements,
    fixed_end_forces,
):
    if len(local_displacements)!=6 or len(fixed_end_forces)!=6:
        raise ValueError("frame local vectors must contain six values")

    internal=[
        sum(local_stiffness[i][j]*local_displacements[j] for j in range(6))
        + fixed_end_forces[i]
        for i in range(6)
    ]
    return tuple(internal)
