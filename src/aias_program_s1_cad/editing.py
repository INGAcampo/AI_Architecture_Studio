"""Reversible geometric editing primitives and multi-entity transformations."""
from __future__ import annotations
from copy import deepcopy
from .entities import Line, Circle, Arc, Polyline, Ellipse, Polygon
from .geometry import Point, rotate_point

def move_point(p, dx, dy):
    """Translate a point by explicit x and y displacements."""
    return Point(p.x+dx,p.y+dy)
def scale_point(p, base, factor):
    """Scale a point relative to a fixed base coordinate."""
    return Point(base.x+(p.x-base.x)*factor,base.y+(p.y-base.y)*factor)
def mirror_point_x(p, axis_y):
    """Mirror a point across a horizontal axis."""
    return Point(p.x, 2*axis_y-p.y)
def mirror_point_y(p, axis_x):
    """Mirror a point across a vertical axis."""
    return Point(2*axis_x-p.x, p.y)

class EditingEngine:
    """Apply move, copy, rotate, scale, mirror, trim and extend operations."""
    def copy(self, entity):
        """Execute the public EditingEngine.copy operation for the S1 professional CAD foundation program using explicit caller inputs."""
        copied=deepcopy(entity)
        copied.entity_id = type(entity)().entity_id
        return copied

    def move(self, entity, dx, dy):
        """Execute the public EditingEngine.move operation for the S1 professional CAD foundation program using explicit caller inputs."""
        e=deepcopy(entity)
        if isinstance(e,Line):
            e.start=move_point(e.start,dx,dy); e.end=move_point(e.end,dx,dy)
        elif isinstance(e,(Circle,Arc,Ellipse)):
            e.center=move_point(e.center,dx,dy)
        elif isinstance(e,(Polyline,Polygon)):
            e.points=[move_point(p,dx,dy) for p in e.points]
        return e

    def rotate(self, entity, base, angle):
        """Execute the public EditingEngine.rotate operation for the S1 professional CAD foundation program using explicit caller inputs."""
        e=deepcopy(entity)
        if isinstance(e,Line):
            e.start=rotate_point(e.start,base,angle); e.end=rotate_point(e.end,base,angle)
        elif isinstance(e,(Circle,Arc,Ellipse)):
            e.center=rotate_point(e.center,base,angle)
        elif isinstance(e,(Polyline,Polygon)):
            e.points=[rotate_point(p,base,angle) for p in e.points]
        return e

    def scale(self, entity, base, factor):
        """Execute the public EditingEngine.scale operation for the S1 professional CAD foundation program using explicit caller inputs."""
        if factor <= 0: raise ValueError("Scale factor must be positive.")
        e=deepcopy(entity)
        if isinstance(e,Line):
            e.start=scale_point(e.start,base,factor); e.end=scale_point(e.end,base,factor)
        elif isinstance(e,Circle):
            e.center=scale_point(e.center,base,factor); e.radius*=factor
        elif isinstance(e,Arc):
            e.center=scale_point(e.center,base,factor); e.radius*=factor
        elif isinstance(e,Ellipse):
            e.center=scale_point(e.center,base,factor); e.radius_x*=factor; e.radius_y*=factor
        elif isinstance(e,(Polyline,Polygon)):
            e.points=[scale_point(p,base,factor) for p in e.points]
        return e

    def mirror_x(self, entity, axis_y=0.0):
        """Execute the public EditingEngine.mirror_x operation for the S1 professional CAD foundation program using explicit caller inputs."""
        e=deepcopy(entity)
        if isinstance(e,Line):
            e.start=mirror_point_x(e.start,axis_y); e.end=mirror_point_x(e.end,axis_y)
        elif isinstance(e,(Circle,Arc,Ellipse)):
            e.center=mirror_point_x(e.center,axis_y)
        elif isinstance(e,(Polyline,Polygon)):
            e.points=[mirror_point_x(p,axis_y) for p in e.points]
        return e

    def rectangular_array(self, entity, rows, columns, row_spacing, column_spacing):
        """Execute the public EditingEngine.rectangular_array operation for the S1 professional CAD foundation program using explicit caller inputs."""
        if rows < 1 or columns < 1:
            raise ValueError("Rows and columns must be positive.")
        result=[]
        for r in range(rows):
            for c in range(columns):
                item=self.copy(entity)
                item=self.move(item,c*column_spacing,r*row_spacing)
                result.append(item)
        return result
