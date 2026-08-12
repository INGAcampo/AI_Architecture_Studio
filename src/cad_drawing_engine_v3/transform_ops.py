from copy import deepcopy
from math import cos, sin, radians
from cad_professional_kernel.entities import CadCircle, CadLine, CadPolyline
from cad_professional_kernel.geometry import Point2D

def move_point(p,dx,dy): return Point2D(p.x+dx,p.y+dy)

def rotate_point(p,base,angle_deg):
    a=radians(angle_deg); x=p.x-base.x; y=p.y-base.y
    return Point2D(base.x+x*cos(a)-y*sin(a),base.y+x*sin(a)+y*cos(a))

def scale_point(p,base,factor):
    return Point2D(base.x+(p.x-base.x)*factor,base.y+(p.y-base.y)*factor)

class TransformEngine:
    def move(self,entity,dx,dy):
        e=deepcopy(entity)
        if isinstance(e,CadLine):
            e.start=move_point(e.start,dx,dy); e.end=move_point(e.end,dx,dy)
        elif isinstance(e,CadCircle):
            e.center=move_point(e.center,dx,dy)
        elif isinstance(e,CadPolyline):
            e.points=[move_point(p,dx,dy) for p in e.points]
        return e

    def rotate(self,entity,base,angle_deg):
        e=deepcopy(entity)
        if isinstance(e,CadLine):
            e.start=rotate_point(e.start,base,angle_deg); e.end=rotate_point(e.end,base,angle_deg)
        elif isinstance(e,CadCircle):
            e.center=rotate_point(e.center,base,angle_deg)
        elif isinstance(e,CadPolyline):
            e.points=[rotate_point(p,base,angle_deg) for p in e.points]
        return e

    def scale(self,entity,base,factor):
        if factor <= 0: raise ValueError("Scale factor must be positive.")
        e=deepcopy(entity)
        if isinstance(e,CadLine):
            e.start=scale_point(e.start,base,factor); e.end=scale_point(e.end,base,factor)
        elif isinstance(e,CadCircle):
            e.center=scale_point(e.center,base,factor); e.radius*=factor
        elif isinstance(e,CadPolyline):
            e.points=[scale_point(p,base,factor) for p in e.points]
        return e
