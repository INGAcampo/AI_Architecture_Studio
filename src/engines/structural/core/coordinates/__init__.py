from dataclasses import dataclass
from math import sqrt
@dataclass(frozen=True,slots=True)
class LocalAxes: x:tuple[float,float,float]; y:tuple[float,float,float]; z:tuple[float,float,float]
class StructuralCoordinateSystem:
 def member_axes(self,a,b):
  d=(b[0]-a[0],b[1]-a[1],b[2]-a[2]); L=sqrt(sum(v*v for v in d))
  if L==0: raise ValueError('Longitud cero')
  x=tuple(v/L for v in d); ref=(0.,0.,1.) if abs(x[2])<.99 else (0.,1.,0.)
  y=(ref[1]*x[2]-ref[2]*x[1],ref[2]*x[0]-ref[0]*x[2],ref[0]*x[1]-ref[1]*x[0]); yl=sqrt(sum(v*v for v in y)); y=tuple(v/yl for v in y)
  z=(x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]); return LocalAxes(x,y,z)
 def to_local(self,v,a): return tuple(sum(v[i]*axis[i] for i in range(3)) for axis in (a.x,a.y,a.z))
