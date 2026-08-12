from PySide6.QtCore import Qt, QPointF, QRectF, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QBrush
from PySide6.QtWidgets import QWidget

from cad_professional_kernel.entities import CadCircle, CadLine, CadPolyline
from cad_professional_kernel.geometry import Point2D
from cad_viewport_pro.camera import Camera2D
from cad_viewport_pro.math2d import ViewTransform
from cad_viewport_pro.hit_test import HitTester
from .grid_engine import ProfessionalGridEngine
from .settings import ViewportSettings
from .theme import ViewportTheme
from .snap_engine import ProfessionalSnapEngine
from .tracking import TrackingEngine

def color(rgb, alpha=255):
    return QColor(rgb[0],rgb[1],rgb[2],alpha)

class ProfessionalViewport(QWidget):
    coordinatesChanged=Signal(float,float)
    selectionChanged=Signal(tuple)
    snapChanged=Signal(str)
    modeChanged=Signal(str)

    def __init__(self,kernel,parent=None):
        super().__init__(parent)
        self.kernel=kernel
        self.camera=Camera2D(0,1,40)
        self.settings=ViewportSettings()
        self.theme=ViewportTheme()
        self.grid_engine=ProfessionalGridEngine()
        self.snap_engine=ProfessionalSnapEngine()
        self.tracking=TrackingEngine()
        self.hit=HitTester()
        self._panning=False
        self._last=QPointF()
        self._drag_start=None
        self._drag_end=None
        self._cursor=QPointF()
        self._snap_candidate=None
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def transform(self):
        return ViewTransform(self.width(),self.height(),self.camera.center_x,self.camera.center_y,self.camera.zoom)

    def paintEvent(self,event):
        p=QPainter(self)
        p.setRenderHint(QPainter.Antialiasing,True)
        p.fillRect(self.rect(),color(self.theme.background))
        if self.settings.grid_enabled:
            self._draw_grid(p)
        self._draw_axes(p)
        self._draw_entities(p)
        self._draw_snap(p)
        self._draw_crosshair(p)
        self._draw_selection_box(p)

    def _draw_grid(self,p):
        t=self.transform()
        spec=self.grid_engine.spec(self.camera.zoom,major_every=self.settings.major_grid_every)
        left=t.screen_to_world(0,0).x; right=t.screen_to_world(self.width(),0).x
        top=t.screen_to_world(0,0).y; bottom=t.screen_to_world(0,self.height()).y
        start_x=int(left//spec.minor_spacing)-1; end_x=int(right//spec.minor_spacing)+1
        start_y=int(bottom//spec.minor_spacing)-1; end_y=int(top//spec.minor_spacing)+1
        for ix in range(start_x,end_x+1):
            x=ix*spec.minor_spacing
            major=(ix % spec.major_every)==0
            pen=QPen(color(self.theme.major_grid if major else self.theme.minor_grid,
                           self.settings.major_grid_alpha if major else self.settings.minor_grid_alpha))
            pen.setWidthF(0.0)
            p.setPen(pen)
            a=t.world_to_screen(x,bottom); b=t.world_to_screen(x,top)
            p.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
        for iy in range(start_y,end_y+1):
            y=iy*spec.minor_spacing
            major=(iy % spec.major_every)==0
            pen=QPen(color(self.theme.major_grid if major else self.theme.minor_grid,
                           self.settings.major_grid_alpha if major else self.settings.minor_grid_alpha))
            pen.setWidthF(0.0)
            p.setPen(pen)
            a=t.world_to_screen(left,y); b=t.world_to_screen(right,y)
            p.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))

    def _draw_axes(self,p):
        t=self.transform()
        x0=t.world_to_screen(0,0)
        px=QPen(color(self.theme.axis_x,100)); px.setWidthF(1.0); p.setPen(px)
        p.drawLine(QPointF(0,x0.y),QPointF(self.width(),x0.y))
        py=QPen(color(self.theme.axis_y,100)); py.setWidthF(1.0); p.setPen(py)
        p.drawLine(QPointF(x0.x,0),QPointF(x0.x,self.height()))

    def _draw_entities(self,p):
        t=self.transform()
        selected=set(self.kernel.selection.ids())
        for e in self.kernel.scene.all():
            if not e.visible: continue
            pen=QPen(color(self.theme.selected if e.entity_id in selected else self.theme.entity))
            pen.setWidthF(self.settings.selected_line_width if e.entity_id in selected else self.settings.entity_line_width)
            p.setPen(pen)
            if isinstance(e,CadLine):
                a=t.world_to_screen(e.start.x,e.start.y); b=t.world_to_screen(e.end.x,e.end.y)
                p.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
            elif isinstance(e,CadCircle):
                c=t.world_to_screen(e.center.x,e.center.y); r=e.radius*t.zoom
                p.drawEllipse(QRectF(c.x-r,c.y-r,2*r,2*r))
            elif isinstance(e,CadPolyline):
                pts=[t.world_to_screen(q.x,q.y) for q in e.points]
                for a,b in zip(pts,pts[1:]):
                    p.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
                if e.closed and len(pts)>2:
                    a,b=pts[-1],pts[0]
                    p.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))

    def _draw_snap(self,p):
        if not self._snap_candidate: return
        t=self.transform()
        q=t.world_to_screen(self._snap_candidate.point.x,self._snap_candidate.point.y)
        pen=QPen(color(self.theme.snap)); pen.setWidthF(1.6); p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawRect(QRectF(q.x-5,q.y-5,10,10))

    def _draw_crosshair(self,p):
        s=self.settings.crosshair_size_pixels
        pen=QPen(color(self.theme.crosshair,170)); pen.setWidthF(0.0); p.setPen(pen)
        p.drawLine(QPointF(self._cursor.x()-s,self._cursor.y()),QPointF(self._cursor.x()+s,self._cursor.y()))
        p.drawLine(QPointF(self._cursor.x(),self._cursor.y()-s),QPointF(self._cursor.x(),self._cursor.y()+s))

    def _draw_selection_box(self,p):
        if not(self._drag_start and self._drag_end): return
        crossing=self._drag_end.x()<self._drag_start.x()
        c=self.theme.selection_crossing if crossing else self.theme.selection_window
        pen=QPen(color(c,220)); pen.setStyle(Qt.DashLine); p.setPen(pen)
        p.setBrush(QBrush(color(c,28)))
        p.drawRect(QRectF(self._drag_start,self._drag_end).normalized())

    def wheelEvent(self,event):
        factor=1.15 if event.angleDelta().y()>0 else 1/1.15
        before=self.transform().screen_to_world(event.position().x(),event.position().y())
        self.camera.zoom_by(factor)
        after=self.transform().screen_to_world(event.position().x(),event.position().y())
        self.camera.pan(before.x-after.x,before.y-after.y)
        self.update()

    def mousePressEvent(self,event):
        self._last=event.position()
        if event.button()==Qt.MiddleButton:
            self._panning=True
        elif event.button()==Qt.LeftButton:
            self._drag_start=event.position(); self._drag_end=event.position()

    def mouseMoveEvent(self,event):
        self._cursor=event.position()
        w=self.transform().screen_to_world(event.position().x(),event.position().y())
        world=Point2D(w.x,w.y)
        self.coordinatesChanged.emit(world.x,world.y)
        if self.settings.snap_enabled:
            self._snap_candidate=self.snap_engine.nearest(world,self.kernel.scene.all(),
                self.settings.snap_tolerance_pixels/self.camera.zoom)
            self.snapChanged.emit(self._snap_candidate.kind if self._snap_candidate else "")
        if self._panning:
            d=event.position()-self._last
            self.camera.pan(-d.x()/self.camera.zoom,d.y()/self.camera.zoom)
            self._last=event.position()
        elif self._drag_start:
            self._drag_end=event.position()
        self.update()

    def mouseReleaseEvent(self,event):
        if event.button()==Qt.MiddleButton:
            self._panning=False; return
        if event.button()!=Qt.LeftButton: return
        start=self._drag_start or event.position(); end=event.position()
        self._drag_start=self._drag_end=None
        if (end-start).manhattanLength()<4:
            w=self.transform().screen_to_world(end.x(),end.y())
            point=Point2D(w.x,w.y)
            tol=6/self.camera.zoom
            hit=next((e for e in reversed(self.kernel.scene.all()) if self.hit.hit(e,point,tol)),None)
            if hit:
                self.kernel.selection.select(hit.entity_id,additive=bool(event.modifiers()&Qt.ControlModifier))
            else:
                self.kernel.selection.clear()
        self.selectionChanged.emit(self.kernel.selection.ids())
        self.update()

    def toggle_grid(self):
        self.settings.grid_enabled=not self.settings.grid_enabled
        self.modeChanged.emit("GRID ON" if self.settings.grid_enabled else "GRID OFF")
        self.update()

    def toggle_snap(self):
        self.settings.snap_enabled=not self.settings.snap_enabled
        self.modeChanged.emit("SNAP ON" if self.settings.snap_enabled else "SNAP OFF")
        self.update()

    def toggle_ortho(self):
        self.settings.ortho_enabled=not self.settings.ortho_enabled
        self.modeChanged.emit("ORTHO ON" if self.settings.ortho_enabled else "ORTHO OFF")

    def toggle_polar(self):
        self.settings.polar_enabled=not self.settings.polar_enabled
        self.modeChanged.emit("POLAR ON" if self.settings.polar_enabled else "POLAR OFF")
