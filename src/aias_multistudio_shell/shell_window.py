"""Public module supporting the coordinated multi-studio desktop shell."""
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDockWidget, QLabel, QMainWindow, QStackedWidget, QStatusBar,
    QTabWidget, QToolBar
)

from .cad_studio import CadStudio
from .documents import StudioDocument
from .home_studio import HomeStudio
from .output_console import OutputConsole
from .project_explorer import ProjectExplorer
from .properties_panel import GlobalPropertiesPanel
from .services import ShellServices
from .studio_placeholders import PlaceholderStudio
from .studios import StudioDescriptor

class MultiStudioShellWindow(QMainWindow):
    """Execute the public MultiStudioShellWindow operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AI Architecture Studio — Multi‑Studio Platform")
        self.resize(1600, 980)
        self.services = ShellServices.create_default()
        self._register_studios()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        self.setCentralWidget(self.tabs)

        self.project_explorer = ProjectExplorer(self.services.project)
        project_dock = QDockWidget("Project Explorer", self)
        project_dock.setWidget(self.project_explorer)
        self.addDockWidget(Qt.LeftDockWidgetArea, project_dock)

        self.properties = GlobalPropertiesPanel()
        properties_dock = QDockWidget("Properties", self)
        properties_dock.setWidget(self.properties)
        self.addDockWidget(Qt.RightDockWidgetArea, properties_dock)

        self.output = OutputConsole()
        output_dock = QDockWidget("Output", self)
        output_dock.setWidget(self.output)
        self.addDockWidget(Qt.BottomDockWidgetArea, output_dock)

        self.status = QStatusBar()
        self.status_label = QLabel("Listo")
        self.status.addPermanentWidget(self.status_label)
        self.setStatusBar(self.status)

        self._build_toolbar()
        self.open_home()
        self.services.events.subscribe("*", lambda event: self.output.write_message(
            f"[{event.name}] {event.payload}"
        ))

    def _register_studios(self) -> None:
        definitions = [
            ("cad", "CAD Studio", "Diseño", lambda: CadStudio(), "Dibujo 2D profesional y edición interactiva."),
            ("bim", "BIM Architecture", "Arquitectura", lambda: PlaceholderStudio("BIM Architecture", "Muros, puertas, ventanas, losas, cubiertas e IFC."), "Modelado BIM arquitectónico nativo."),
            ("structural", "Structural Studio", "Ingeniería", lambda: PlaceholderStudio("Structural Studio", "Modelo analítico, cargas, combinaciones y diseño."), "Análisis y diseño estructural integrado."),
            ("fem", "FEM & Simulation", "Ingeniería", lambda: PlaceholderStudio("FEM & Simulation", "Mallas, solvers, no linealidad y dinámica."), "Simulación avanzada por elementos finitos."),
            ("civil", "Civil & Roads", "Infraestructura", lambda: PlaceholderStudio("Civil & Roads", "Superficies, alineamientos, perfiles y corredores."), "Diseño vial, movimiento de tierra y obra civil."),
            ("survey", "Survey & Topography", "Infraestructura", lambda: PlaceholderStudio("Survey & Topography", "Puntos, superficies, coordenadas y replanteo."), "Topografía y levantamientos."),
            ("mep", "MEP Studio", "Instalaciones", lambda: PlaceholderStudio("MEP Studio", "Eléctrico, sanitario, HVAC y coordinación."), "Diseño y coordinación de instalaciones."),
            ("cost", "Quantity & Cost", "Gestión", lambda: PlaceholderStudio("Quantity & Cost", "Cómputos, precios, presupuestos y planificación."), "Cantidades, costos y control de obra."),
            ("docs", "Documentation", "Documentación", lambda: PlaceholderStudio("Documentation", "Planos, láminas, tablas y publicaciones."), "Documentación ejecutiva coordinada."),
            ("render", "Visualization", "Visualización", lambda: PlaceholderStudio("Visualization", "Materiales, iluminación, render y recorrido."), "Visualización y presentación."),
            ("ai", "AI Engineering Assistant", "IA", lambda: PlaceholderStudio("AI Engineering Assistant", "Diseño generativo, revisión y automatización."), "Asistente multidisciplinario de ingeniería."),
        ]
        for studio_id, name, category, factory, description in definitions:
            self.services.studios.register(
                StudioDescriptor(studio_id, name, category, factory, description)
            )

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Studios")
        self.addToolBar(toolbar)
        home = QAction("Inicio", self)
        home.triggered.connect(self.open_home)
        toolbar.addAction(home)
        for descriptor in self.services.studios.all():
            action = QAction(descriptor.name, self)
            action.triggered.connect(lambda checked=False, sid=descriptor.studio_id: self.open_studio(sid))
            toolbar.addAction(action)

    def open_home(self) -> None:
        """Load home for the coordinated multi-studio desktop shell while preserving typed state."""
        home = HomeStudio(self.services.studios.all())
        home.studioRequested.connect(self.open_studio)
        index = self.tabs.addTab(home, "Inicio")
        self.tabs.setCurrentIndex(index)
        self.properties.set_context(self.services.project.name, "Inicio", "-")

    def open_studio(self, studio_id: str) -> None:
        """Load studio for the coordinated multi-studio desktop shell while preserving typed state."""
        descriptor = self.services.studios.get(studio_id)
        widget = descriptor.factory()
        document = StudioDocument(f"{descriptor.name} Document", studio_id)
        self.services.documents.add(document)
        index = self.tabs.addTab(widget, descriptor.name)
        self.tabs.setCurrentIndex(index)
        self.properties.set_context(
            self.services.project.name,
            descriptor.name,
            document.title,
        )
        self.status_label.setText(f"Studio activo: {descriptor.name}")
        from .events import StudioEvent
        self.services.events.publish(StudioEvent("studio.opened", {
            "studio_id": studio_id,
            "document_id": document.document_id,
        }))

    def _close_tab(self, index: int) -> None:
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        widget.deleteLater()
