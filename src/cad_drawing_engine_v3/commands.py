from dataclasses import dataclass, field
from math import hypot
from cad_professional_kernel.entities import CadCircle,CadLine,CadPolyline
from cad_professional_kernel.geometry import Point2D

class InteractiveCommand:
    name="BASE"
    prompt=""

    def click(self,point:Point2D): raise NotImplementedError
    def preview(self,point:Point2D): return None
    @property
    def finished(self): return False

@dataclass(slots=True)
class LineCommand(InteractiveCommand):
    name="LINE"
    prompt="Precise el primer punto"
    first: Point2D | None=None
    result: CadLine | None=None

    def click(self,point):
        if self.first is None:
            self.first=point; self.prompt="Precise el segundo punto"
        else:
            self.result=CadLine(start=self.first,end=point)
        return self.result

    def preview(self,point):
        return CadLine(start=self.first,end=point) if self.first else None

    @property
    def finished(self): return self.result is not None

@dataclass(slots=True)
class CircleCommand(InteractiveCommand):
    name="CIRCLE"
    prompt="Precise el centro"
    center: Point2D | None=None
    result: CadCircle | None=None

    def click(self,point):
        if self.center is None:
            self.center=point; self.prompt="Precise un punto del radio"
        else:
            radius=self.center.distance_to(point)
            if radius>0: self.result=CadCircle(center=self.center,radius=radius)
        return self.result

    def preview(self,point):
        if self.center is None: return None
        r=self.center.distance_to(point)
        return CadCircle(center=self.center,radius=max(r,1e-9))

    @property
    def finished(self): return self.result is not None

@dataclass(slots=True)
class PolylineCommand(InteractiveCommand):
    name="POLYLINE"
    prompt="Precise el primer punto"
    points:list[Point2D]=field(default_factory=list)
    result:CadPolyline|None=None

    def click(self,point):
        self.points.append(point)
        self.prompt="Precise el siguiente punto o Enter para terminar"
        return None

    def finish(self,closed=False):
        if len(self.points)>=2:
            self.result=CadPolyline(points=list(self.points),closed=closed)
        return self.result

    def preview(self,point):
        if not self.points: return None
        return CadPolyline(points=[*self.points,point],closed=False)

    @property
    def finished(self): return self.result is not None
