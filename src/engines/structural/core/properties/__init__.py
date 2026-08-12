from dataclasses import dataclass
from math import pi,sqrt
from engines.structural.core.sections import SectionShape
@dataclass(frozen=True,slots=True)
class SectionProperties: area:float; ix:float; iy:float; torsion_j:float; rx:float; ry:float; zx:float; zy:float
class SectionPropertyEngine:
 def calculate(self,s):
  d=s.dimensions
  if s.shape is SectionShape.RECTANGLE:
   b,h=d['b'],d['h']; a=b*h; ix=b*h**3/12; iy=h*b**3/12; j=b*h*(b*b+h*h)/12; zx=ix/(h/2); zy=iy/(b/2)
  elif s.shape is SectionShape.CIRCLE:
   dia=d['d']; a=pi*dia**2/4; ix=iy=pi*dia**4/64; j=pi*dia**4/32; zx=zy=ix/(dia/2)
  elif s.shape is SectionShape.PIPE:
   do,di=d['do'],d['di']; a=pi*(do**2-di**2)/4; ix=iy=pi*(do**4-di**4)/64; j=pi*(do**4-di**4)/32; zx=zy=ix/(do/2)
  else: raise NotImplementedError(s.shape.value)
  return SectionProperties(a,ix,iy,j,sqrt(ix/a),sqrt(iy/a),zx,zy)
