"""Robust two-dimensional line, segment and circle intersection operations."""
from __future__ import annotations
from .primitives import Line2D, Point2D, Circle2D

class IntersectionEngine:
    """Compute geometric intersections while distinguishing parallel and disjoint cases."""
    @staticmethod
    def line_line(a: Line2D, b: Line2D, tolerance=1e-12):
        """Return the intersection of two infinite lines or None when parallel."""
        x1,y1,x2,y2 = a.start.x,a.start.y,a.end.x,a.end.y
        x3,y3,x4,y4 = b.start.x,b.start.y,b.end.x,b.end.y
        den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if abs(den) <= tolerance:
            return None
        px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/den
        py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/den
        p = Point2D(px,py)
        def within(v,a,b): return min(a,b)-tolerance <= v <= max(a,b)+tolerance
        if all((within(px,x1,x2),within(py,y1,y2),within(px,x3,x4),within(py,y3,y4))):
            return p
        return None

    @staticmethod
    def line_circle(line: Line2D, circle: Circle2D, tolerance=1e-12):
        """Return zero, one or two intersections between a line and circle."""
        dx = line.end.x-line.start.x
        dy = line.end.y-line.start.y
        fx = line.start.x-circle.center.x
        fy = line.start.y-circle.center.y
        a = dx*dx+dy*dy
        b = 2*(fx*dx+fy*dy)
        c = fx*fx+fy*fy-circle.radius*circle.radius
        disc = b*b-4*a*c
        if disc < -tolerance:
            return ()
        if abs(disc) <= tolerance:
            t = -b/(2*a)
            return (Point2D(line.start.x+t*dx,line.start.y+t*dy),) if 0<=t<=1 else ()
        disc = disc**0.5
        ts = [(-b-disc)/(2*a),(-b+disc)/(2*a)]
        return tuple(Point2D(line.start.x+t*dx,line.start.y+t*dy) for t in ts if 0<=t<=1)
