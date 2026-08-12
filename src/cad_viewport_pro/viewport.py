from PySide6.QtCore import Qt, QPointF, QRectF, Signal
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QWidget

from cad_professional_kernel.entities import CadCircle, CadLine, CadPolyline
from cad_professional_kernel.geometry import Point2D
from .camera import Camera2D
from .grid import AdaptiveGrid
from .hit_test import HitTester
from .math2d import ViewTransform

class CadViewport(QWidget):
    coordinatesChanged = Signal(float, float)
    selectionChanged = Signal(tuple)

    def __init__(self, kernel, parent=None):
        super().__init__(parent)
        self.kernel=kernel
        self.camera=Camera2D(0,1,40)
        self.grid=AdaptiveGrid()
        self.hit=HitTester()
        self._panning=False
        self._last=QPointF()
        self._drag_start=None
        self._drag_end=None
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def transform(self):
        return ViewTransform(self.width(),self.height(),self.camera.center_x,self.camera.center_y,self.camera.zoom)

    def paintEvent(self,event):
        painter=QPainter(self)
        painter.fillRect(self.rect(),self.palette().base())
        self._draw_grid(painter)
        selected=set(self.kernel.selection.ids())
        for entity in self.kernel.scene.all():
            pen=QPen()
            pen.setWidthF(2 if entity.entity_id in selected else 1)
            painter.setPen(pen)
            t=self.transform()
            if isinstance(entity,CadLine):
                a=t.world_to_screen(entity.start.x,entity.start.y); b=t.world_to_screen(entity.end.x,entity.end.y)
                painter.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
            elif isinstance(entity,CadCircle):
                c=t.world_to_screen(entity.center.x,entity.center.y); r=entity.radius*t.zoom
                painter.drawEllipse(QRectF(c.x-r,c.y-r,2*r,2*r))
            elif isinstance(entity,CadPolyline):
                pts=[t.world_to_screen(p.x,p.y) for p in entity.points]
                for a,b in zip(pts,pts[1:]):
                    painter.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
                if entity.closed and len(pts)>2:
                    a,b=pts[-1],pts[0]
                    painter.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
        if self._drag_start and self._drag_end:
            painter.drawRect(QRectF(self._drag_start,self._drag_end).normalized())

    def _draw_grid(self,painter):
        t=self.transform(); spacing=self.grid.spacing(self.camera.zoom)
        left=t.screen_to_world(0,0).x; right=t.screen_to_world(self.width(),0).x
        top=t.screen_to_world(0,0).y; bottom=t.screen_to_world(0,self.height()).y
        for ix in range(int(left//spacing)-1,int(right//spacing)+2):
            x=ix*spacing; a=t.world_to_screen(x,bottom); b=t.world_to_screen(x,top)
            painter.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
        for iy in range(int(bottom//spacing)-1,int(top//spacing)+2):
            y=iy*spacing; a=t.world_to_screen(left,y); b=t.world_to_screen(right,y)
            painter.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))

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
        w=self.transform().screen_to_world(event.position().x(),event.position().y())
        self.coordinatesChanged.emit(w.x,w.y)
        if self._panning:
            d=event.position()-self._last
            self.camera.pan(-d.x()/self.camera.zoom,d.y()/self.camera.zoom)
            self._last=event.position(); self.update()
        elif self._drag_start:
            self._drag_end=event.position(); self.update()

    def mouseReleaseEvent(self,event):
        if event.button()==Qt.MiddleButton:
            self._panning=False; return
        if event.button()!=Qt.LeftButton: return
        start=self._drag_start or event.position(); end=event.position()
        self._drag_start=self._drag_end=None
        if (end-start).manhattanLength()<4:
            w=self.transform().screen_to_world(end.x(),end.y())
            tol=6/self.camera.zoom
            found=next((e for e in reversed(self.kernel.scene.all()) if self.hit.hit(e,Point2D(w.x,w.y),tol)),None)
            if found:
                self.kernel.selection.select(found.entity_id,additive=bool(event.modifiers()&Qt.ControlModifier))
            else:
                self.kernel.selection.clear()
        self.selectionChanged.emit(self.kernel.selection.ids()); self.update()
