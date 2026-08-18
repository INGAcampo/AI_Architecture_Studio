from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDockWidget,QFormLayout,QLabel,QMainWindow,QStatusBar,QToolBar,QWidget

from cad_professional_kernel.entities import CadCircle,CadLine,CadPolyline
from cad_professional_kernel.geometry import Point2D
from cad_professional_kernel.service import CadKernelService
from .viewport import CadViewport

class PropertiesPanel(QWidget):
    def __init__(self,kernel):
        super().__init__(); self.kernel=kernel
        form=QFormLayout(self)
        self.type=QLabel("-"); self.ident=QLabel("-"); self.layer=QLabel("-")
        form.addRow("Type",self.type); form.addRow("ID",self.ident); form.addRow("Layer",self.layer)
    def refresh(self,ids):
        if len(ids)!=1:
            self.type.setText("-"); self.ident.setText("-"); self.layer.setText("-"); return
        e=self.kernel.scene.get(ids[0])
        self.type.setText(type(e).__name__); self.ident.setText(e.entity_id); self.layer.setText(e.layer)

class CadViewportMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIAS CAD Viewport Professional v1")
        self.resize(1400,900)
        self.kernel=CadKernelService()
        self.viewport=CadViewport(self.kernel)
        self.setCentralWidget(self.viewport)
        props=PropertiesPanel(self.kernel)
        dock=QDockWidget("Properties",self); dock.setWidget(props); self.addDockWidget(Qt.RightDockWidgetArea,dock)
        status=QStatusBar(); self.coords=QLabel("X: 0.000 Y: 0.000"); status.addPermanentWidget(self.coords); self.setStatusBar(status)
        bar=QToolBar("CAD"); self.addToolBar(bar)
        for text,callback in [
            ("Line",self.add_line),("Circle",self.add_circle),("Polyline",self.add_poly),
            ("Undo",self.undo),("Redo",self.redo),("Delete",self.delete),("Fit",self.fit)
        ]:
            action=QAction(text,self); action.triggered.connect(callback); bar.addAction(action)
        self.viewport.coordinatesChanged.connect(lambda x,y:self.coords.setText(f"X: {x:.3f} Y: {y:.3f}"))
        self.viewport.selectionChanged.connect(props.refresh)
        self.kernel.add(CadLine(start=Point2D(-8,-4),end=Point2D(8,-4)))
        self.kernel.add(CadCircle(center=Point2D(0,2),radius=3))
        self.kernel.add(CadPolyline(points=[Point2D(-6,5),Point2D(0,9),Point2D(6,5)]))
    def add_line(self): self.kernel.add(CadLine(start=Point2D(-5,0),end=Point2D(5,0))); self.viewport.update()
    def add_circle(self): self.kernel.add(CadCircle(center=Point2D(0,0),radius=2)); self.viewport.update()
    def add_poly(self): self.kernel.add(CadPolyline(points=[Point2D(-3,-3),Point2D(0,3),Point2D(3,-3)],closed=True)); self.viewport.update()
    def undo(self): self.kernel.undo(); self.viewport.update()
    def redo(self): self.kernel.redo(); self.viewport.update()
    def delete(self):
        for entity_id in tuple(self.kernel.selection.ids()): self.kernel.delete(entity_id)
        self.viewport.update()
    def fit(self):
        self.viewport.camera.center_x=0; self.viewport.camera.center_y=1; self.viewport.camera.set_zoom(40); self.viewport.update()
