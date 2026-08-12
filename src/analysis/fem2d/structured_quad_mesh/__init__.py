from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Node: node_id:str; coordinates:tuple
@dataclass(frozen=True,slots=True)
class Element: element_id:str; node_ids:tuple
class StructuredQuadMeshGenerator:
    def generate(self,w,h,nx,ny):
        nodes=tuple(Node(f"N{j*(nx+1)+i+1}",(w*i/nx,h*j/ny)) for j in range(ny+1) for i in range(nx+1)); els=[]
        for j in range(ny):
            for i in range(nx):
                n=j*(nx+1)+i+1; els.append(Element(f"E{j*nx+i+1}",(f"N{n}",f"N{n+1}",f"N{n+nx+2}",f"N{n+nx+1}")))
        return nodes,tuple(els)