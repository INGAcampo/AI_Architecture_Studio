from PySide6.QtCore import Qt,QPointF,QRectF,Signal
from PySide6.QtGui import QColor,QPainter,QPen,QBrush
from cad_professional_kernel.entities import CadCircle,CadLine,CadPolyline
from cad_professional_kernel.geometry import Point2D
from cad_viewport_pro_v2.viewport_widget import ProfessionalViewport

class DrawingViewport(ProfessionalViewport):
    commandPromptChanged=Signal(str)

    def __init__(self,kernel,controller,parent=None):
        super().__init__(kernel,parent)
        self.controller=controller

    def paintEvent(self,event):
        super().paintEvent(event)
        p=QPainter(self)
        p.setRenderHint(QPainter.Antialiasing,True)
        self._draw_preview(p)
        self._draw_grips(p)

    def _draw_preview(self,p):
        e=self.controller.preview_entity
        if e is None: return
        t=self.transform()
        pen=QPen(QColor(255,190,60,210)); pen.setStyle(Qt.DashLine); pen.setWidthF(1.4); p.setPen(pen)
        if isinstance(e,CadLine):
            a=t.world_to_screen(e.start.x,e.start.y); b=t.world_to_screen(e.end.x,e.end.y)
            p.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))
        elif isinstance(e,CadCircle):
            c=t.world_to_screen(e.center.x,e.center.y); r=e.radius*t.zoom
            p.drawEllipse(QRectF(c.x-r,c.y-r,2*r,2*r))
        elif isinstance(e,CadPolyline):
            pts=[t.world_to_screen(q.x,q.y) for q in e.points]
            for a,b in zip(pts,pts[1:]): p.drawLine(QPointF(a.x,a.y),QPointF(b.x,b.y))

    def _draw_grips(self,p):
        from .grips import GripEngine
        t=self.transform()
        p.setPen(QPen(QColor(70,160,255))); p.setBrush(QBrush(QColor(70,160,255)))
        engine=GripEngine()
        for entity_id in self.kernel.selection.ids():
            entity=self.kernel.scene.get(entity_id)
            for grip in engine.grips(entity):
                q=t.world_to_screen(grip.point.x,grip.point.y)
                p.drawRect(QRectF(q.x-4,q.y-4,8,8))

    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
        if self.controller.active:
            w=self.transform().screen_to_world(event.position().x(),event.position().y())
            point=Point2D(w.x,w.y)
            if self._snap_candidate: point=self._snap_candidate.point
            self.controller.move(point)
            self.commandPromptChanged.emit(self.controller.dynamic.prompt)
            self.update()

    def mouseReleaseEvent(self,event):
        if event.button()==Qt.RightButton and self.controller.active:
            self.controller.cancel()
            self.commandPromptChanged.emit("Comando:")
            self.update()
            return
        if event.button()==Qt.LeftButton and self.controller.active:
            w=self.transform().screen_to_world(event.position().x(),event.position().y())
            point=Point2D(w.x,w.y)
            if self._snap_candidate: point=self._snap_candidate.point
            self.controller.click(point)
            self.commandPromptChanged.emit(self.controller.dynamic.prompt)
            self.update()
            return
        super().mouseReleaseEvent(event)
