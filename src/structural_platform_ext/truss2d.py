from __future__ import annotations
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class TrussNode:
    node_id:str; x_m:float; y_m:float; fix_x:bool=False; fix_y:bool=False
@dataclass(frozen=True)
class TrussMember:
    member_id:str; start_node:str; end_node:str; area_m2:float; elastic_modulus_pa:float
@dataclass(frozen=True)
class TrussLoad:
    node_id:str; fx_n:float=0.; fy_n:float=0.
@dataclass(frozen=True)
class TrussModel:
    nodes:tuple[TrussNode,...]; members:tuple[TrussMember,...]; loads:tuple[TrussLoad,...]=()
@dataclass(frozen=True)
class TrussResult:
    displacements_m:dict; reactions_n:dict; member_axial_forces_n:dict

def _solve(a,b):
    n=len(b); m=[list(map(float,a[i]))+[float(b[i])] for i in range(n)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(m[r][c]))
        if abs(m[p][c])<1e-14: raise ValueError("structural stiffness matrix is singular")
        m[c],m[p]=m[p],m[c]
        q=m[c][c]
        for j in range(c,n+1): m[c][j]/=q
        for r in range(n):
            if r==c: continue
            q=m[r][c]
            for j in range(c,n+1): m[r][j]-=q*m[c][j]
    return [m[i][n] for i in range(n)]

def solve_truss_2d(model:TrussModel)->TrussResult:
    ids={}
    for i,n in enumerate(model.nodes):
        if n.node_id in ids: raise ValueError("duplicate node_id")
        ids[n.node_id]=i
    nd=2*len(model.nodes); K=[[0.]*nd for _ in range(nd)]; F=[0.]*nd; geom={}
    for load in model.loads:
        i=ids[load.node_id]; F[2*i]+=load.fx_n; F[2*i+1]+=load.fy_n
    for m in model.members:
        if m.start_node==m.end_node or m.area_m2<=0 or m.elastic_modulus_pa<=0: raise ValueError("invalid member")
        i=ids[m.start_node]; j=ids[m.end_node]; a=model.nodes[i]; b=model.nodes[j]
        dx=b.x_m-a.x_m; dy=b.y_m-a.y_m; L=math.hypot(dx,dy)
        if L<=0: raise ValueError("invalid member length")
        c=dx/L; s=dy/L; k=m.area_m2*m.elastic_modulus_pa/L
        q=[[c*c,c*s,-c*c,-c*s],[c*s,s*s,-c*s,-s*s],[-c*c,-c*s,c*c,c*s],[-c*s,-s*s,c*s,s*s]]
        d=[2*i,2*i+1,2*j,2*j+1]
        for r in range(4):
            for z in range(4): K[d[r]][d[z]]+=k*q[r][z]
        geom[m.member_id]=(m,L,c,s,d)
    fixed=set()
    for i,n in enumerate(model.nodes):
        if n.fix_x: fixed.add(2*i)
        if n.fix_y: fixed.add(2*i+1)
    free=[i for i in range(nd) if i not in fixed]
    if not free: raise ValueError("no free degrees of freedom")
    ufree=_solve([[K[i][j] for j in free] for i in free],[F[i] for i in free])
    U=[0.]*nd
    for i,d in enumerate(free): U[d]=ufree[i]
    R=[sum(K[i][j]*U[j] for j in range(nd))-F[i] for i in range(nd)]
    disp={n.node_id:(U[2*i],U[2*i+1]) for i,n in enumerate(model.nodes)}
    react={n.node_id:(R[2*i],R[2*i+1]) for i,n in enumerate(model.nodes)}
    axial={}
    for mid,(m,L,c,s,d) in geom.items():
        u=[U[x] for x in d]; ext=-c*u[0]-s*u[1]+c*u[2]+s*u[3]
        axial[mid]=m.area_m2*m.elastic_modulus_pa/L*ext
    return TrussResult(disp,react,axial)
