from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True,slots=True)
class AnchorForce:
    anchor_id:str
    tension:float
    shear_x:float
    shear_y:float
    shear:float

class AnchorGroupEngine:
    def distribute(self,anchors,demand):
        if not anchors:return ()
        cx=sum(a.x for a in anchors)/len(anchors)
        cy=sum(a.y for a in anchors)/len(anchors)
        ix=sum((a.y-cy)**2 for a in anchors)
        iy=sum((a.x-cx)**2 for a in anchors)
        out=[]
        for a in anchors:
            t=max(0,demand.axial/len(anchors)+(0 if ix==0 else demand.moment_x*(a.y-cy)/ix)+(0 if iy==0 else demand.moment_y*(a.x-cx)/iy))
            sx=demand.shear_x/len(anchors)
            sy=demand.shear_y/len(anchors)
            out.append(AnchorForce(a.anchor_id,t,sx,sy,hypot(sx,sy)))
        return tuple(out)
