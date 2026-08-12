from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QDockWidget,QFormLayout,QLabel,QLineEdit,QMainWindow,QStatusBar,QToolBar,QVBoxLayout,QWidget
)

from cad_professional_kernel.entities import CadCircle,CadLine,CadPolyline
from cad_professional_kernel.geometry import Point2D
from cad_professional_kernel.service import CadKernelService
from .viewport_widget import ProfessionalViewport

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

class ProfessionalMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIAS CAD Viewport Professional v2")
        self.resize(1500,920)
        self.kernel=CadKernelService()
        self.viewport=ProfessionalViewport(self.kernel)
        self.command_line=QLineEdit()
        self.command_line.setPlaceholderText("Escriba un comando")
        central=QWidget(); layout=QVBoxLayout(central); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.viewport,1); layout.addWidget(self.command_line,0)
        self.setCentralWidget(central)

        props=PropertiesPanel(self.kernel)
        dock=QDockWidget("Propiedades",self); dock.setWidget(props); self.addDockWidget(Qt.RightDockWidgetArea,dock)

        status=QStatusBar()
        self.coords=QLabel("X: 0.000 Y: 0.000")
        self.snap_label=QLabel("")
        self.mode_label=QLabel("GRID ON | SNAP ON")
        status.addPermanentWidget(self.coords); status.addPermanentWidget(self.snap_label); status.addPermanentWidget(self.mode_label)
        self.setStatusBar(status)

        bar=QToolBar("CAD Pro v2"); self.addToolBar(bar)
        actions=[
            ("Line",self.add_line,None),("Circle",self.add_circle,None),("Polyline",self.add_poly,None),
            ("Undo",self.undo,QKeySequence.Undo),("Redo",self.redo,QKeySequence.Redo),
            ("Delete",self.delete,QKeySequence.Delete),("Fit",self.fit,None),
            ("Grid",self.viewport.toggle_grid,None),("Snap",self.viewport.toggle_snap,None),
            ("Ortho",self.viewport.toggle_ortho,None),("Polar",self.viewport.toggle_polar,None),
        ]
        for text,callback,shortcut in actions:
            a=QAction(text,self); a.triggered.connect(callback)
            if shortcut: a.setShortcut(shortcut)
            bar.addAction(a)

        self.viewport.coordinatesChanged.connect(lambda x,y:self.coords.setText(f"X: {x:.3f}  Y: {y:.3f}"))
        self.viewport.selectionChanged.connect(props.refresh)
        self.viewport.snapChanged.connect(lambda kind:self.snap_label.setText(f"SNAP: {kind.upper()}" if kind else ""))
        self.viewport.modeChanged.connect(lambda text:self.mode_label.setText(text))
        self.command_line.returnPressed.connect(self.execute_command)

        self.kernel.add(CadLine(start=Point2D(-8,-4),end=Point2D(8,-4)))
        self.kernel.add(CadCircle(center=Point2D(0,2),radius=3))
        self.kernel.add(CadPolyline(points=[Point2D(-6,5),Point2D(0,9),Point2D(6,5)]))

    def execute_command(self):
        cmd=self.command_line.text().strip().lower()
        self.command_line.clear()
        mapping={
            "line":self.add_line,"circle":self.add_circle,"polyline":self.add_poly,
            "undo":self.undo,"redo":self.redo,"delete":self.delete,
            "fit":self.fit,"grid":self.viewport.toggle_grid,"snap":self.viewport.toggle_snap,
            "ortho":self.viewport.toggle_ortho,"polar":self.viewport.toggle_polar
        }
        if cmd in mapping: mapping[cmd]()
        else: self.statusBar().showMessage(f"Comando desconocido: {cmd}",3000)

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
