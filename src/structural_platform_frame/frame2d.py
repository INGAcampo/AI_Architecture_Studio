from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FrameNode:
    node_id: str
    x_m: float
    y_m: float
    fix_x: bool = False
    fix_y: bool = False
    fix_rz: bool = False


@dataclass(frozen=True)
class FrameElement:
    element_id: str
    start_node: str
    end_node: str
    area_m2: float
    inertia_m4: float
    elastic_modulus_pa: float


@dataclass(frozen=True)
class FrameLoad:
    node_id: str
    fx_n: float = 0.0
    fy_n: float = 0.0
    mz_nm: float = 0.0


@dataclass(frozen=True)
class FrameModel:
    nodes: tuple[FrameNode, ...]
    elements: tuple[FrameElement, ...]
    loads: tuple[FrameLoad, ...] = ()


@dataclass(frozen=True)
class FrameResult:
    displacements: dict[str, tuple[float, float, float]]
    reactions: dict[str, tuple[float, float, float]]


def _solve(matrix, vector):
    n = len(vector)
    a = [list(map(float, matrix[i])) + [float(vector[i])] for i in range(n)]

    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-14:
            raise ValueError("frame stiffness matrix is singular")

        a[col], a[pivot] = a[pivot], a[col]
        q = a[col][col]
        for j in range(col, n + 1):
            a[col][j] /= q

        for row in range(n):
            if row == col:
                continue
            q = a[row][col]
            for j in range(col, n + 1):
                a[row][j] -= q * a[col][j]

    return [a[i][n] for i in range(n)]


def _local_stiffness(ea_l, ei, length):
    l = length
    return [
        [ea_l, 0, 0, -ea_l, 0, 0],
        [0, 12*ei/l**3, 6*ei/l**2, 0, -12*ei/l**3, 6*ei/l**2],
        [0, 6*ei/l**2, 4*ei/l, 0, -6*ei/l**2, 2*ei/l],
        [-ea_l, 0, 0, ea_l, 0, 0],
        [0, -12*ei/l**3, -6*ei/l**2, 0, 12*ei/l**3, -6*ei/l**2],
        [0, 6*ei/l**2, 2*ei/l, 0, -6*ei/l**2, 4*ei/l],
    ]


def _transform(c, s):
    return [
        [c, s, 0, 0, 0, 0],
        [-s, c, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, c, s, 0],
        [0, 0, 0, -s, c, 0],
        [0, 0, 0, 0, 0, 1],
    ]


def _matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def _transpose(a):
    return [list(row) for row in zip(*a)]


def solve_frame_2d(model: FrameModel) -> FrameResult:
    if not model.nodes or not model.elements:
        raise ValueError("frame requires nodes and elements")

    ids = {}
    for i, node in enumerate(model.nodes):
        if node.node_id in ids:
            raise ValueError("duplicate node_id")
        ids[node.node_id] = i

    nd = 3 * len(model.nodes)
    kglobal = [[0.0] * nd for _ in range(nd)]
    force = [0.0] * nd

    for load in model.loads:
        i = ids[load.node_id]
        force[3*i] += load.fx_n
        force[3*i+1] += load.fy_n
        force[3*i+2] += load.mz_nm

    for element in model.elements:
        if element.start_node == element.end_node:
            raise ValueError("element nodes must differ")
        if element.area_m2 <= 0 or element.inertia_m4 <= 0 or element.elastic_modulus_pa <= 0:
            raise ValueError("element properties must be positive")

        i = ids[element.start_node]
        j = ids[element.end_node]
        n1 = model.nodes[i]
        n2 = model.nodes[j]
        dx = n2.x_m - n1.x_m
        dy = n2.y_m - n1.y_m
        length = math.hypot(dx, dy)
        if length <= 0:
            raise ValueError("element length must be positive")

        c = dx / length
        s = dy / length
        local = _local_stiffness(
            element.elastic_modulus_pa * element.area_m2 / length,
            element.elastic_modulus_pa * element.inertia_m4,
            length,
        )
        t = _transform(c, s)
        kg = _matmul(_transpose(t), _matmul(local, t))
        dofs = [3*i,3*i+1,3*i+2,3*j,3*j+1,3*j+2]

        for r in range(6):
            for z in range(6):
                kglobal[dofs[r]][dofs[z]] += kg[r][z]

    fixed = set()
    for i, node in enumerate(model.nodes):
        if node.fix_x:
            fixed.add(3*i)
        if node.fix_y:
            fixed.add(3*i+1)
        if node.fix_rz:
            fixed.add(3*i+2)

    free = [i for i in range(nd) if i not in fixed]
    if not free:
        raise ValueError("frame has no free degrees of freedom")

    reduced_k = [[kglobal[i][j] for j in free] for i in free]
    reduced_f = [force[i] for i in free]
    ufree = _solve(reduced_k, reduced_f)

    u = [0.0] * nd
    for i, dof in enumerate(free):
        u[dof] = ufree[i]

    reactions = [
        sum(kglobal[i][j] * u[j] for j in range(nd)) - force[i]
        for i in range(nd)
    ]

    displacement_by_node = {}
    reaction_by_node = {}
    for i, node in enumerate(model.nodes):
        displacement_by_node[node.node_id] = (
            u[3*i], u[3*i+1], u[3*i+2]
        )
        reaction_by_node[node.node_id] = (
            reactions[3*i], reactions[3*i+1], reactions[3*i+2]
        )

    return FrameResult(
        displacements=displacement_by_node,
        reactions=reaction_by_node,
    )
