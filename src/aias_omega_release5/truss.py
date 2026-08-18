"""Public module supporting the fifth Omega integrated product release."""
from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class Node:
    """Execute the public Node operation for the fifth Omega integrated product release using explicit caller inputs."""
    node_id: str
    x: float
    y: float
    fix_x: bool = False
    fix_y: bool = False
    load_x: float = 0.0
    load_y: float = 0.0

@dataclass(frozen=True, slots=True)
class Bar:
    """Execute the public Bar operation for the fifth Omega integrated product release using explicit caller inputs."""
    bar_id: str
    start: str
    end: str
    area_m2: float
    elastic_modulus_pa: float

@dataclass(frozen=True, slots=True)
class TrussResult:
    """Execute the public TrussResult operation for the fifth Omega integrated product release using explicit caller inputs."""
    displacements: dict[str, tuple[float,float]]
    reactions: dict[str, tuple[float,float]]
    axial_forces: dict[str, float]

def solve_linear_system(a,b):
    """Execute the public solve_linear_system operation for the fifth Omega integrated product release using explicit caller inputs."""
    n=len(b); m=[list(map(float,row))+[float(b[i])] for i,row in enumerate(a)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda r:abs(m[r][col]))
        if abs(m[pivot][col])<1e-14: raise ValueError("Singular stiffness matrix.")
        m[col],m[pivot]=m[pivot],m[col]
        p=m[col][col]
        for j in range(col,n+1): m[col][j]/=p
        for r in range(n):
            if r==col: continue
            f=m[r][col]
            for j in range(col,n+1): m[r][j]-=f*m[col][j]
    return [m[i][n] for i in range(n)]

class Truss2DSolver:
    """Execute the public Truss2DSolver operation for the fifth Omega integrated product release using explicit caller inputs."""
    def solve(self,nodes,bars):
        """Execute the public Truss2DSolver.solve operation for the fifth Omega integrated product release using explicit caller inputs."""
        by_id={n.node_id:n for n in nodes}; ids=[n.node_id for n in nodes]; dof={nid:(2*i,2*i+1) for i,nid in enumerate(ids)}
        ndof=2*len(nodes); K=[[0.0]*ndof for _ in range(ndof)]; F=[0.0]*ndof
        for n in nodes:
            ix,iy=dof[n.node_id]; F[ix]=n.load_x; F[iy]=n.load_y
        geom={}
        for bar in bars:
            n1,n2=by_id[bar.start],by_id[bar.end]; dx=n2.x-n1.x; dy=n2.y-n1.y; L=hypot(dx,dy)
            if L<=0 or bar.area_m2<=0 or bar.elastic_modulus_pa<=0: raise ValueError("Invalid bar.")
            c,s=dx/L,dy/L; k=bar.area_m2*bar.elastic_modulus_pa/L
            ke=[[k*c*c,k*c*s,-k*c*c,-k*c*s],[k*c*s,k*s*s,-k*c*s,-k*s*s],
                [-k*c*c,-k*c*s,k*c*c,k*c*s],[-k*c*s,-k*s*s,k*c*s,k*s*s]]
            mapd=[*dof[bar.start],*dof[bar.end]]
            for i in range(4):
                for j in range(4): K[mapd[i]][mapd[j]]+=ke[i][j]
            geom[bar.bar_id]=(bar,c,s,L,mapd)
        fixed=set()
        for n in nodes:
            ix,iy=dof[n.node_id]
            if n.fix_x: fixed.add(ix)
            if n.fix_y: fixed.add(iy)
        free=[i for i in range(ndof) if i not in fixed]
        Kr=[[K[i][j] for j in free] for i in free]; Fr=[F[i] for i in free]
        ur=solve_linear_system(Kr,Fr); U=[0.0]*ndof
        for i,v in zip(free,ur): U[i]=v
        R=[sum(K[i][j]*U[j] for j in range(ndof))-F[i] for i in range(ndof)]
        axial={}
        for bid,(bar,c,s,L,mapd) in geom.items():
            u=[U[d] for d in mapd]; extension=(-c)*u[0]+(-s)*u[1]+c*u[2]+s*u[3]
            axial[bid]=bar.area_m2*bar.elastic_modulus_pa/L*extension
        return TrussResult(
            {nid:(U[dof[nid][0]],U[dof[nid][1]]) for nid in ids},
            {nid:(R[dof[nid][0]],R[dof[nid][1]]) for nid in ids},
            axial
        )
