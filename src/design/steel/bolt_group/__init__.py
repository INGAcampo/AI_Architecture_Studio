from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class BoltPoint:
    bolt_id:str
    x:float
    y:float

@dataclass(frozen=True, slots=True)
class BoltForce:
    bolt_id:str
    shear_x:float
    shear_y:float
    resultant:float

class BoltGroupEngine:
    def distribute(self,points,total_shear_x,total_shear_y,moment=0.0):
        if not points: return ()
        cx=sum(p.x for p in points)/len(points)
        cy=sum(p.y for p in points)/len(points)
        polar=sum((p.x-cx)**2+(p.y-cy)**2 for p in points)
        out=[]
        for p in points:
            dx=p.x-cx; dy=p.y-cy
            direct_x=total_shear_x/len(points)
            direct_y=total_shear_y/len(points)
            torsion_x=0.0 if polar==0 else -moment*dy/polar
            torsion_y=0.0 if polar==0 else moment*dx/polar
            sx=direct_x+torsion_x; sy=direct_y+torsion_y
            out.append(BoltForce(p.bolt_id,sx,sy,hypot(sx,sy)))
        return tuple(out)
