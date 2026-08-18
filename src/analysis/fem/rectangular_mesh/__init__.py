from analysis.fem.fem_domain import FemNode,FemElement
class RectangularMesh:
 def generate(self,w,h,nx,ny):
  nodes=tuple(FemNode(f'N{j*(nx+1)+i+1}',(w*i/nx,h*j/ny)) for j in range(ny+1) for i in range(nx+1))
  elems=[]
  for j in range(ny):
   for i in range(nx):
    n=j*(nx+1)+i+1; elems.append(FemElement(f'E{j*nx+i+1}',(f'N{n}',f'N{n+1}',f'N{n+nx+2}',f'N{n+nx+1}'),'MAT'))
  return nodes,tuple(elems)
