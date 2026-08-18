from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,QKeySequence
from PySide6.QtWidgets import QDockWidget,QFormLayout,QLabel,QLineEdit,QMainWindow,QStatusBar,QToolBar,QVBoxLayout,QWidget

from cad_professional_kernel.entities import CadCircle,CadLine,CadPolyline
from cad_professional_kernel.geometry import Point2D
from cad_professional_kernel.service import CadKernelService
from .controller import DrawingController
from .viewport_v3 import DrawingViewport

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

class DrawingMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIAS CAD Professional Drawing Engine v3")
        self.resize(1550,940)
        self.kernel=CadKernelService()
        self.controller=DrawingController(self.kernel)
        self.viewport=DrawingViewport(self.kernel,self.controller)
        self.command=QLineEdit(); self.command.setPlaceholderText("Escriba un comando")
        central=QWidget(); layout=QVBoxLayout(central); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.viewport,1); layout.addWidget(self.command)
        self.setCentralWidget(central)

        props=PropertiesPanel(self.kernel)
        dock=QDockWidget("Propiedades",self); dock.setWidget(props); self.addDockWidget(Qt.RightDockWidgetArea,dock)

        status=QStatusBar(); self.coords=QLabel("X: 0.000 Y: 0.000"); self.mode=QLabel("GRID | SNAP")
        status.addPermanentWidget(self.coords); status.addPermanentWidget(self.mode); self.setStatusBar(status)

        bar=QToolBar("Drawing Engine v3"); self.addToolBar(bar)
        for text,callback,shortcut in [
            ("Line",lambda:self.start("LINE"),"L"),("Circle",lambda:self.start("CIRCLE"),"C"),
            ("Polyline",lambda:self.start("POLYLINE"),"PL"),("Finish PL",self.finish_poly,None),
            ("Undo",self.undo,QKeySequence.Undo),("Redo",self.redo,QKeySequence.Redo),
            ("Delete",self.delete,QKeySequence.Delete),("Grid",self.viewport.toggle_grid,None),
            ("Snap",self.viewport.toggle_snap,None),("Ortho",self.viewport.toggle_ortho,None),
            ("Polar",self.viewport.toggle_polar,None),("Fit",self.fit,None)
        ]:
            a=QAction(text,self); a.triggered.connect(callback)
            if shortcut: a.setShortcut(shortcut)
            bar.addAction(a)

        self.viewport.coordinatesChanged.connect(lambda x,y:self.coords.setText(f"X: {x:.3f} Y: {y:.3f}"))
        self.viewport.selectionChanged.connect(props.refresh)
        self.viewport.commandPromptChanged.connect(self.command.setPlaceholderText)
        self.command.returnPressed.connect(self.execute_command)
        self.kernel.add(CadLine(start=Point2D(-8,-4),end=Point2D(8,-4)))
        self.kernel.add(CadCircle(center=Point2D(0,2),radius=3))
        self.kernel.add(CadPolyline(points=[Point2D(-6,5),Point2D(0,9),Point2D(6,5)]))

    def start(self,name):
        self.controller.start(name); self.command.setPlaceholderText(self.controller.dynamic.prompt); self.viewport.setFocus()

    def finish_poly(self):
        self.controller.finish_polyline(False); self.command.setPlaceholderText("Comando:"); self.viewport.update()

    def execute_command(self):
        cmd=self.command.text().strip().upper(); self.command.clear()
        if cmd in {"L","LINE"}: self.start("LINE")
        elif cmd in {"C","CIRCLE"}: self.start("CIRCLE")
        elif cmd in {"PL","POLYLINE"}: self.start("POLYLINE")
        elif cmd in {"ENTER","FINISH"}: self.finish_poly()
        elif cmd=="UNDO": self.undo()
        elif cmd=="REDO": self.redo()
        elif cmd=="DELETE": self.delete()
        elif cmd=="GRID": self.viewport.toggle_grid()
        elif cmd=="SNAP": self.viewport.toggle_snap()
        elif cmd=="ORTHO": self.viewport.toggle_ortho()
        elif cmd=="POLAR": self.viewport.toggle_polar()
        elif cmd=="FIT": self.fit()
        else: self.statusBar().showMessage(f"Comando desconocido: {cmd}",2500)

    def undo(self): self.kernel.undo(); self.viewport.update()
    def redo(self): self.kernel.redo(); self.viewport.update()
    def delete(self):
        for entity_id in tuple(self.kernel.selection.ids()): self.kernel.delete(entity_id)
        self.viewport.update()
    def fit(self):
        self.viewport.camera.center_x=0; self.viewport.camera.center_y=1; self.viewport.camera.set_zoom(40); self.viewport.update()
