"""Linear-elastic planar frame assembly, solution and element-force recovery."""
from dataclasses import dataclass
from math import hypot
from .linear_algebra import solve_linear_system
from .model import StructuralModel2D

@dataclass(frozen=True, slots=True)
class ElementForce2D:
    """Recovered local axial, shear and bending end-force vector."""
    element_id: str
    axial_i_n: float
    shear_i_n: float
    moment_i_nm: float
    axial_j_n: float
    shear_j_n: float
    moment_j_nm: float

@dataclass(frozen=True, slots=True)
class FrameResult2D:
    """Global displacements, support reactions and member-force results."""
    displacements: dict
    reactions: dict
    element_forces: dict

class Frame2DSolver:
    """Assemble stiffness, enforce restraints and solve planar frame equilibrium."""
    def solve(self, model: StructuralModel2D) -> FrameResult2D:
        """Execute the public Frame2DSolver.solve operation for the Omega structural analysis and design suite using explicit caller inputs."""
        model.validate()
        node_ids = list(model.nodes)
        dof = {nid: (3*i, 3*i+1, 3*i+2) for i, nid in enumerate(node_ids)}
        ndof = 3 * len(node_ids)
        K = [[0.0] * ndof for _ in range(ndof)]
        F = [0.0] * ndof

        for load in model.loads:
            ux, uy, rz = dof[load.node_id]
            F[ux] += load.fx_n
            F[uy] += load.fy_n
            F[rz] += load.mz_nm

        element_data = {}
        for e in model.elements.values():
            ni, nj = model.nodes[e.node_i], model.nodes[e.node_j]
            dx, dy = nj.x - ni.x, nj.y - ni.y
            L = hypot(dx, dy)
            c, s = dx / L, dy / L
            mat = model.materials[e.material_id]
            sec = model.sections[e.section_id]
            EA_L = mat.elastic_modulus_pa * sec.area_m2 / L
            EI = mat.elastic_modulus_pa * sec.inertia_m4
            k = [
                [EA_L, 0, 0, -EA_L, 0, 0],
                [0, 12*EI/L**3, 6*EI/L**2, 0, -12*EI/L**3, 6*EI/L**2],
                [0, 6*EI/L**2, 4*EI/L, 0, -6*EI/L**2, 2*EI/L],
                [-EA_L, 0, 0, EA_L, 0, 0],
                [0, -12*EI/L**3, -6*EI/L**2, 0, 12*EI/L**3, -6*EI/L**2],
                [0, 6*EI/L**2, 2*EI/L, 0, -6*EI/L**2, 4*EI/L],
            ]
            T = [
                [c,s,0,0,0,0],[-s,c,0,0,0,0],[0,0,1,0,0,0],
                [0,0,0,c,s,0],[0,0,0,-s,c,0],[0,0,0,0,0,1],
            ]
            def mm(a,b):
                return [[sum(a[i][q]*b[q][j] for q in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
            TT = [list(x) for x in zip(*T)]
            kg = mm(TT, mm(k, T))
            mapd = [*dof[e.node_i], *dof[e.node_j]]
            for i in range(6):
                for j in range(6):
                    K[mapd[i]][mapd[j]] += kg[i][j]
            element_data[e.element_id] = (k, T, mapd)

        fixed = set()
        for n in model.nodes.values():
            ux, uy, rz = dof[n.node_id]
            if n.restraint_x: fixed.add(ux)
            if n.restraint_y: fixed.add(uy)
            if n.restraint_rz: fixed.add(rz)

        free = [i for i in range(ndof) if i not in fixed]
        Kr = [[K[i][j] for j in free] for i in free]
        Fr = [F[i] for i in free]
        ur = solve_linear_system(Kr, Fr)
        U = [0.0] * ndof
        for i, v in zip(free, ur):
            U[i] = v
        R = [sum(K[i][j] * U[j] for j in range(ndof)) - F[i] for i in range(ndof)]

        element_forces = {}
        for eid, (k, T, mapd) in element_data.items():
            ug = [U[d] for d in mapd]
            ul = [sum(T[i][j]*ug[j] for j in range(6)) for i in range(6)]
            fl = [sum(k[i][j]*ul[j] for j in range(6)) for i in range(6)]
            element_forces[eid] = ElementForce2D(eid, *fl)

        return FrameResult2D(
            {nid: tuple(U[i] for i in dof[nid]) for nid in node_ids},
            {nid: tuple(R[i] for i in dof[nid]) for nid in node_ids},
            element_forces,
        )
