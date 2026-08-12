"""Qt workspace presenting foundational CAD tools and interactive drawing state."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,QFormLayout,QLabel,QMainWindow,QPlainTextEdit,QTableWidget,
    QTableWidgetItem,QToolBar,QWidget,QVBoxLayout
)
from PySide6.QtGui import QAction

from .entities import Line,Circle,Ellipse,Polyline
from .geometry import Point
from .service import CadFoundationService

class CadProgramS1Window(QMainWindow):
    """Desktop CAD foundation window integrating canvas, actions and status feedback."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIAS Program S1 — Professional CAD Foundation")
        self.resize(1500,920)
        self.service=CadFoundationService()
        self.table=QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["ID","Type","Layer","Visible","Locked"])
        self.setCentralWidget(self.table)
        self.output=QPlainTextEdit(); self.output.setReadOnly(True)
        dock=QDockWidget("Engineering Output",self); dock.setWidget(self.output)
        self.addDockWidget(Qt.BottomDockWidgetArea,dock)
        bar=QToolBar("Program S1"); self.addToolBar(bar)
        for text,callback in [
            ("Add Line",self.add_line),("Add Circle",self.add_circle),
            ("Add Ellipse",self.add_ellipse),("Add Polyline",self.add_polyline),
            ("Create Layer",self.create_layer),("Array Selected",self.array_selected),
            ("Save Demo",self.save_demo)
        ]:
            action=QAction(text,self); action.triggered.connect(callback); bar.addAction(action)
        self.add_line(); self.add_circle()

    def refresh(self):
        """Execute the public CadProgramS1Window.refresh operation for the S1 professional CAD foundation program using explicit caller inputs."""
        self.table.setRowCount(0)
        for e in self.service.entities:
            row=self.table.rowCount(); self.table.insertRow(row)
            values=[e.entity_id,type(e).__name__,e.layer,str(e.visible),str(e.locked)]
            for col,value in enumerate(values): self.table.setItem(row,col,QTableWidgetItem(value))

    def add_line(self):
        """Add line to the S1 professional CAD foundation program while enforcing identity constraints."""
        self.service.add(Line(start=Point(0,0),end=Point(10,0))); self.refresh()
    def add_circle(self):
        """Add circle to the S1 professional CAD foundation program while enforcing identity constraints."""
        self.service.add(Circle(center=Point(5,5),radius=2)); self.refresh()
    def add_ellipse(self):
        """Add ellipse to the S1 professional CAD foundation program while enforcing identity constraints."""
        self.service.add(Ellipse(center=Point(8,4),radius_x=3,radius_y=1.5)); self.refresh()
    def add_polyline(self):
        """Add polyline to the S1 professional CAD foundation program while enforcing identity constraints."""
        self.service.add(Polyline(points=[Point(0,0),Point(3,4),Point(8,1)])); self.refresh()
    def create_layer(self):
        """Build the layer required by the S1 professional CAD foundation program from explicit inputs."""
        name=f"LAYER_{len(self.service.layers.all())}"
        self.service.layers.create(name)
        self.output.appendPlainText(f"Layer created: {name}")
    def array_selected(self):
        """Execute the public CadProgramS1Window.array_selected operation for the S1 professional CAD foundation program using explicit caller inputs."""
        if not self.service.entities: return
        source=self.service.entities[-1]
        created=self.service.editing.rectangular_array(source,2,3,5,5)
        self.service.entities.extend(created)
        self.output.appendPlainText(f"Rectangular array: {len(created)} entities")
        self.refresh()
    def save_demo(self):
        """Persist demo for the S1 professional CAD foundation program in its stable external representation."""
        from pathlib import Path
        from .document import DocumentSerializer
        path=Path("aias_program_s1_demo.json").resolve()
        DocumentSerializer().save(self.service.entities,path)
        self.output.appendPlainText(f"Saved: {path}")
