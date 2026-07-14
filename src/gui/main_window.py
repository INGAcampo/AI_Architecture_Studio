"""
AI Architecture Studio
Main Window

Foundation 4.2
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QListWidget,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QTextEdit,
    QTreeWidget,
    QListWidgetItem,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
)

from commands.cad.circle_command import CircleCommand
from commands.cad.copy_command import CopyCommand
from commands.cad.line_command import LineCommand
from commands.cad.move_command import MoveCommand
from commands.cad.polyline_command import PolylineCommand
from commands.cad.rectangle_command import RectangleCommand
from commands.cad.rotate_command import RotateCommand
from commands.cad.scale_command import ScaleCommand
from gui.dialogs.new_project_dialog import NewProjectDialog
from gui.ribbon import Ribbon
from gui.workspace import Workspace


class MainWindow(QMainWindow):

    def __init__(self, app_core=None):
        super().__init__()

        self.app_core = app_core

        self.setWindowTitle(
            "AI Architecture Studio - Foundation 4.2"
        )
        self.resize(1600, 900)

        self.create_menu()
        self.create_central_area()
        self.create_project_explorer()
        self.create_properties_panel()
        self.create_layers_panel()
        self.create_ai_panel()
        self.create_status_bar()
        self.apply_dark_theme()

        self.connect_current_canvas()
        self.refresh_project_tree()
        self.clear_properties()

    # ---------------------------------------------------------
    # MENÚ
    # ---------------------------------------------------------

    def create_menu(self):
        menu = QMenuBar(self)

        archivo = menu.addMenu("Archivo")

        nuevo = archivo.addAction("Nuevo Proyecto")
        nuevo.triggered.connect(
            self.open_new_project_dialog
        )

        archivo.addAction("Abrir Proyecto")
        archivo.addAction("Guardar Proyecto")
        archivo.addSeparator()
        archivo.addAction("Salir", self.close)

        menu.addMenu("Editar")
        menu.addMenu("Ver")
        menu.addMenu("Arquitectura")
        menu.addMenu("Estructuras")
        menu.addMenu("BIM")
        menu.addMenu("Geotecnia")
        menu.addMenu("Costos")
        menu.addMenu("IA")
        menu.addMenu("Ayuda")

        self.setMenuBar(menu)

    # ---------------------------------------------------------
    # ÁREA CENTRAL
    # ---------------------------------------------------------

    def create_central_area(self):
        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        self.ribbon = Ribbon(self)

        self.ribbon.new_project_btn.clicked.connect(
            self.open_new_project_dialog
        )

        self.ribbon.line_btn.clicked.connect(
            self.activate_line_command
        )

        self.ribbon.polyline_btn.clicked.connect(
            self.activate_polyline_command
        )

        self.ribbon.rectangle_btn.clicked.connect(
            self.activate_rectangle_command
        )

        self.ribbon.circle_btn.clicked.connect(
            self.activate_circle_command
        )

        self.ribbon.move_btn.clicked.connect(
            self.activate_move_command
        )

        self.ribbon.copy_btn.clicked.connect(
            self.activate_copy_command
        )

        self.ribbon.rotate_btn.clicked.connect(
            self.activate_rotate_command
        )

        self.ribbon.scale_btn.clicked.connect(
            self.activate_scale_command
        )

        self.workspace = Workspace(
            scene=self.app_core.scene
        )

        layout.addWidget(self.ribbon)
        layout.addWidget(self.workspace)

        self.setCentralWidget(container)

    def connect_current_canvas(self):
        canvas = self.workspace.current_canvas()

        if canvas is None:
            return

        if getattr(
            canvas,
            "_properties_signal_connected",
            False,
        ):
            return

        canvas.element_selected.connect(
            self.show_element_properties
        )

        canvas._properties_signal_connected = True

    # ---------------------------------------------------------
    # COMANDOS CAD
    # ---------------------------------------------------------

    def activate_line_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                LineCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "LINE activo: selecciona dos puntos"
            )

    def activate_polyline_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                PolylineCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "PLINE activo: varios clics y ENTER para finalizar"
            )

    def activate_rectangle_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                RectangleCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "RECTANGLE activo: selecciona dos esquinas"
            )

    def activate_circle_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                CircleCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "CIRCLE activo: selecciona centro y radio"
            )

    def activate_move_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                MoveCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "MOVE activo: selecciona un objeto, "
                "luego punto base y destino"
            )

    def activate_copy_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                CopyCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "COPY activo: selecciona un objeto, "
                "luego punto base y destino"
            )

    def activate_rotate_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                RotateCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "ROTATE activo: selecciona un objeto, "
                "luego punto base y ángulo"
            )

    def activate_scale_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                ScaleCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                "SCALE activo: selecciona un objeto, "
                "luego punto base, referencia y final"
            )

    # ---------------------------------------------------------
    # PROYECTOS
    # ---------------------------------------------------------

    def open_new_project_dialog(self):
        if self.app_core is None:
            return

        dialog = NewProjectDialog(
            project_manager=self.app_core.project_manager,
            parent=self,
        )

        if dialog.exec():
            nombre = dialog.name_input.text().strip()

            self.workspace.add_document_tab(nombre)
            self.connect_current_canvas()

            self.statusBar().showMessage(
                f"Proyecto '{nombre}' creado correctamente."
            )

            self.refresh_project_tree()

    # ---------------------------------------------------------
    # EXPLORADOR DEL PROYECTO
    # ---------------------------------------------------------

    def create_project_explorer(self):
        dock = QDockWidget(
            "Explorador del Proyecto",
            self,
        )

        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderHidden(True)

        dock.setWidget(self.project_tree)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            dock,
        )

    def refresh_project_tree(self):
        if not hasattr(self, "project_tree"):
            return

        self.project_tree.clear()

        if self.app_core is None:
            return

        root_node = self.app_core.scene.root
        root_item = self.create_tree_item(
            root_node
        )

        self.project_tree.addTopLevelItem(
            root_item
        )

        root_item.setExpanded(True)

        for index in range(
            root_item.childCount()
        ):
            root_item.child(index).setExpanded(
                True
            )

    def create_tree_item(self, scene_node):
        item = QTreeWidgetItem(
            [scene_node.name]
        )

        item.setData(
            0,
            Qt.UserRole,
            scene_node,
        )

        for child in scene_node.children:
            item.addChild(
                self.create_tree_item(child)
            )

        return item

    # ---------------------------------------------------------
    # PANEL DE PROPIEDADES
    # ---------------------------------------------------------

    def create_properties_panel(self):
        dock = QDockWidget(
            "Propiedades",
            self,
        )

        self.properties_list = QListWidget()

        dock.setWidget(
            self.properties_list
        )

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            dock,
        )

    def clear_properties(self):
        self.properties_list.clear()

        self.properties_list.addItems([
            "Nombre: Sin selección",
            "Tipo: -",
        ])

    def show_element_properties(self, element):
        self.properties_list.clear()

        if element is None:
            self.clear_properties()

            self.statusBar().showMessage(
                "Ningún objeto seleccionado"
            )
            return

        information = element.info()

        for key, value in information.items():
            if (
                key == "Propiedades"
                and isinstance(value, dict)
            ):
                self.properties_list.addItem(
                    "── Propiedades ──"
                )

                for (
                    property_name,
                    property_value,
                ) in value.items():
                    self.properties_list.addItem(
                        f"{property_name}: "
                        f"{property_value}"
                    )
            else:
                self.properties_list.addItem(
                    f"{key}: {value}"
                )

        self.statusBar().showMessage(
            f"Seleccionado: {element.name}"
        )

    # ---------------------------------------------------------
    # ASISTENTE IA
    # ---------------------------------------------------------

    def create_layers_panel(self):
        dock = QDockWidget(
            "Capas",
            self,
        )

        container = QWidget()
        layout = QVBoxLayout(container)

        self.layers_list = QListWidget()
        layout.addWidget(self.layers_list)

        buttons_layout = QHBoxLayout()
        self.new_layer_btn = QPushButton("Nueva capa")
        self.activate_layer_btn = QPushButton("Activar")
        self.toggle_visibility_btn = QPushButton("Mostrar/Ocultar")
        self.toggle_lock_btn = QPushButton("Bloquear/Desbloq.")

        buttons_layout.addWidget(self.new_layer_btn)
        buttons_layout.addWidget(self.activate_layer_btn)
        buttons_layout.addWidget(self.toggle_visibility_btn)
        buttons_layout.addWidget(self.toggle_lock_btn)

        layout.addLayout(buttons_layout)

        self.new_layer_btn.clicked.connect(self.create_new_layer)
        self.activate_layer_btn.clicked.connect(self.activate_selected_layer)
        self.toggle_visibility_btn.clicked.connect(self.toggle_selected_layer_visibility)
        self.toggle_lock_btn.clicked.connect(self.toggle_selected_layer_lock)

        dock.setWidget(container)

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            dock,
        )

        self.refresh_layers_panel()

    def refresh_layers_panel(self):
        if not hasattr(self, "layers_list"):
            return

        self.layers_list.clear()

        if self.app_core is None:
            return

        layer_manager = None
        if self.app_core is not None and getattr(self.app_core, "kernel", None) is not None:
            layer_manager = self.app_core.kernel.services.get("layer_manager")
        if layer_manager is None:
            return

        for layer in layer_manager.all_layers():
            status = []
            if layer.visible:
                status.append("V")
            else:
                status.append("H")
            if layer.locked:
                status.append("L")
            else:
                status.append("U")
            if layer_manager.current_layer and layer.name == layer_manager.current_layer.name:
                status.append("A")

            item = QListWidgetItem(
                f"{layer.name} [{' '.join(status)}]"
            )
            item.setData(Qt.UserRole, layer.name)
            self.layers_list.addItem(item)

    def create_new_layer(self):
        if self.app_core is None:
            return

        layer_manager = None
        if self.app_core is not None and getattr(self.app_core, "kernel", None) is not None:
            layer_manager = self.app_core.kernel.services.get("layer_manager")
        if layer_manager is None:
            return

        name = f"Layer{len(layer_manager.all_layers()) + 1}"
        layer_manager.create_layer(name)
        self.refresh_layers_panel()

    def activate_selected_layer(self):
        if self.app_core is None:
            return

        selected = self.layers_list.currentItem()
        if selected is None:
            return

        layer_name = selected.data(Qt.UserRole)
        if not layer_name:
            layer_name = selected.text().split(" ")[0]

        layer_manager = None
        if self.app_core is not None and getattr(self.app_core, "kernel", None) is not None:
            layer_manager = self.app_core.kernel.services.get("layer_manager")
        if layer_manager is None:
            return

        layer_manager.set_current_layer(layer_name)
        self.refresh_layers_panel()

    def toggle_selected_layer_visibility(self):
        if self.app_core is None:
            return

        selected = self.layers_list.currentItem()
        if selected is None:
            return

        layer_name = selected.data(Qt.UserRole)
        if not layer_name:
            layer_name = selected.text().split(" ")[0]

        layer_manager = None
        if self.app_core is not None and getattr(self.app_core, "kernel", None) is not None:
            layer_manager = self.app_core.kernel.services.get("layer_manager")
        if layer_manager is None:
            return

        layer = layer_manager.get_layer(layer_name)
        if layer is not None:
            layer_manager.set_visibility(layer_name, not layer.visible)
            if layer.visible:
                self.statusBar().showMessage(f"Capa {layer_name} visible")
            else:
                self.statusBar().showMessage(f"Capa {layer_name} oculta")

            canvas = self.workspace.current_canvas()
            if canvas is not None:
                canvas.highlight.clear()
                canvas.selection_manager.clear()
                canvas.element_selected.emit(None)
                canvas.update()

            self.refresh_layers_panel()
            self._restore_layer_selection(layer_name)

    def toggle_selected_layer_lock(self):
        if self.app_core is None:
            return

        selected = self.layers_list.currentItem()
        if selected is None:
            return

        layer_name = selected.data(Qt.UserRole)
        if not layer_name:
            layer_name = selected.text().split(" ")[0]

        layer_manager = None
        if self.app_core is not None and getattr(self.app_core, "kernel", None) is not None:
            layer_manager = self.app_core.kernel.services.get("layer_manager")
        if layer_manager is None:
            return

        layer = layer_manager.get_layer(layer_name)
        if layer is not None:
            layer_manager.set_locked(layer_name, not layer.locked)
            if layer.locked:
                self.statusBar().showMessage(f"Capa {layer_name} bloqueada")
            else:
                self.statusBar().showMessage(f"Capa {layer_name} desbloqueada")

            canvas = self.workspace.current_canvas()
            if canvas is not None:
                canvas.highlight.clear()
                canvas.selection_manager.clear()
                canvas.element_selected.emit(None)
                canvas.update()

            self.refresh_layers_panel()
            self._restore_layer_selection(layer_name)

    def _restore_layer_selection(self, layer_name):
        if not hasattr(self, "layers_list"):
            return

        for index in range(self.layers_list.count()):
            item = self.layers_list.item(index)
            if item.data(Qt.UserRole) == layer_name:
                self.layers_list.setCurrentItem(item)
                break

    def create_ai_panel(self):
        dock = QDockWidget(
            "Asistente IA",
            self,
        )

        texto = QTextEdit()

        texto.setPlaceholderText(
            "Describe lo que deseas diseñar..."
        )

        dock.setWidget(texto)

        self.addDockWidget(
            Qt.BottomDockWidgetArea,
            dock,
        )

    # ---------------------------------------------------------
    # BARRA DE ESTADO
    # ---------------------------------------------------------

    def create_status_bar(self):
        barra = QStatusBar()

        barra.showMessage(
            "AIAS Foundation 4.2 listo"
        )

        self.setStatusBar(barra)

    # ---------------------------------------------------------
    # TEMA
    # ---------------------------------------------------------

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background: #2b2b2b;
            }

            QMenuBar {
                background: #202020;
                color: white;
                padding: 4px;
            }

            QMenuBar::item {
                padding: 6px 12px;
            }

            QMenuBar::item:selected {
                background: #3a3a3a;
            }

            QDockWidget {
                color: white;
            }

            QTreeWidget,
            QListWidget,
            QTextEdit {
                background: #1e1e1e;
                color: white;
                border: 1px solid #3a3a3a;
            }

            QListWidget::item {
                padding: 3px;
            }

            QStatusBar {
                background: #202020;
                color: white;
            }
        """)