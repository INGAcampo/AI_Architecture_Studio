from dataclasses import dataclass
from math import hypot
@dataclass(frozen=True,slots=True)
class WeldGroupProperties: centroid_x:float; centroid_y:float; total_length:float; polar_moment:float
@dataclass(frozen=True,slots=True)
class WeldSegmentForce: segment_id:str; force_x:float; force_y:float; resultant:float
class WeldGroupEngine:
    def distribute(self,segs,fx,fy,m):
        L=sum(s.length for s in segs); cx=sum((s.x1+s.x2)/2*s.length for s in segs)/L; cy=sum((s.y1+s.y2)/2*s.length for s in segs)/L
        J=sum((((s.x1+s.x2)/2-cx)**2+((s.y1+s.y2)/2-cy)**2)*s.length for s in segs)
        out=[]
        for s in segs:
            x=(s.x1+s.x2)/2-cx; y=(s.y1+s.y2)/2-cy
            sx=fx*s.length/L+(0 if J==0 else -m*y*s.length/J); sy=fy*s.length/L+(0 if J==0 else m*x*s.length/J)
            out.append(WeldSegmentForce(s.segment_id,sx,sy,hypot(sx,sy)))
        return WeldGroupProperties(cx,cy,L,J),tuple(out)
