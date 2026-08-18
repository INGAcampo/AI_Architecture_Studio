"""
AI Architecture Studio
Main Window

Dynamic Input v1 / JOIN Professional 4.3
"""

from pathlib import Path

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
    QMessageBox,
)

from commands.cad.circle_command import CircleCommand
from commands.cad.copy_command import CopyCommand
from commands.cad.line_command import LineCommand
from commands.cad.move_command import MoveCommand
from commands.cad.offset_command import OffsetCommand
from commands.cad.mirror_command import MirrorCommand
from commands.cad.polyline_command import PolylineCommand
from commands.cad.rectangle_command import RectangleCommand
from commands.cad.rotate_command import RotateCommand
from commands.cad.scale_command import ScaleCommand
from commands.cad.trim_command import TrimCommand
from commands.cad.extend_command import ExtendCommand
from commands.cad.fillet_command import FilletCommand
from commands.cad.chamfer_command import ChamferCommand
from commands.cad.join_command import JoinCommand
from commands.architectural.wall_command import WallCommand
from commands.architectural.wall_node_command import WallNodeCommand
from commands.architectural.opening_command import OpeningCommand
from commands.architectural.door_command import DoorCommand
from commands.architectural.window_command import WindowCommand
from commands.architectural.room_command import RoomCommand
from commands.architectural.room_edit_command import RoomEditCommand
from commands.architectural.room_schedule_command import RoomScheduleCommand
from commands.architectural.slab_command import SlabCommand
from commands.architectural.slab_schedule_command import SlabScheduleCommand
from commands.core.standards_command import StandardsCommand
from commands.core.standards_report_command import StandardsReportCommand
from gui.command_line import CommandLine
from gui.dialogs.new_project_dialog import NewProjectDialog
from gui.ribbon import Ribbon
from gui.workspace import Workspace
from gui.project_session import ProjectSessionController
from gui.inspector import BimPropertyInspector, InspectorController
from aias_design_system import render_qss
from aias_i18n import get_translator


class MainWindow(QMainWindow):

    def __init__(self, app_core=None):
        super().__init__()

        self.app_core = app_core
        self.translator = get_translator()

        self.setWindowTitle(
            self.translator.translate("app.title")
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

        self.project_session = ProjectSessionController(self, self.app_core)
        self.rebuild_recent_projects_menu()

    # ---------------------------------------------------------
    # MENÚ
    # ---------------------------------------------------------

    def create_menu(self):
        menu = QMenuBar(self)

        archivo = menu.addMenu(self.translator.translate("menu.file"))
        self.file_menu = archivo

        nuevo = archivo.addAction(self.translator.translate("menu.new_project"))
        nuevo.setShortcut("Ctrl+N")
        nuevo.triggered.connect(self.new_project)

        abrir = archivo.addAction(self.translator.translate("menu.open_project"))
        abrir.setShortcut("Ctrl+O")
        abrir.triggered.connect(self.open_project)

        guardar = archivo.addAction(self.translator.translate("menu.save_project"))
        guardar.setShortcut("Ctrl+S")
        guardar.triggered.connect(self.save_project)

        guardar_como = archivo.addAction(self.translator.translate("menu.save_as"))
        guardar_como.setShortcut("Ctrl+Shift+S")
        guardar_como.triggered.connect(self.save_project_as)

        self.recent_menu = archivo.addMenu(self.translator.translate("menu.recent_projects"))
        archivo.addSeparator()
        archivo.addAction(self.translator.translate("menu.exit"), self.close)

        menu.addMenu(self.translator.translate("menu.edit"))
        menu.addMenu(self.translator.translate("menu.view"))
        menu.addMenu(self.translator.translate("menu.architecture"))
        menu.addMenu(self.translator.translate("menu.structure"))
        menu.addMenu(self.translator.translate("menu.bim"))
        menu.addMenu(self.translator.translate("menu.geotechnics"))
        menu.addMenu(self.translator.translate("menu.costs"))
        menu.addMenu(self.translator.translate("menu.ai"))
        menu.addMenu(self.translator.translate("menu.help"))

        self.setMenuBar(menu)

    # ---------------------------------------------------------
    # ÁREA CENTRAL
    # ---------------------------------------------------------

    def create_central_area(self):
        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        self.ribbon = Ribbon(self)

        self.ribbon.new_project_btn.clicked.connect(self.new_project)
        self.ribbon.open_project_btn.clicked.connect(self.open_project)
        self.ribbon.save_project_btn.clicked.connect(self.save_project)

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

        self.ribbon.mirror_btn.clicked.connect(
            self.activate_mirror_command
        )

        self.ribbon.offset_btn.clicked.connect(
            self.activate_offset_command
        )

        self.ribbon.trim_btn.clicked.connect(
            self.activate_trim_command
        )

        self.ribbon.extend_btn.clicked.connect(
            self.activate_extend_command
        )

        self.ribbon.fillet_btn.clicked.connect(
            self.activate_fillet_command
        )

        self.ribbon.chamfer_btn.clicked.connect(
            self.activate_chamfer_command
        )

        self.ribbon.join_btn.clicked.connect(
            self.activate_join_command
        )

        self.ribbon.wall_btn.clicked.connect(
            self.activate_wall_command
        )

        self.workspace = Workspace(
            scene=self.app_core.scene
        )

        self.command_line = CommandLine(self)
        self.command_line.command_submitted.connect(
            self.handle_command_line_submit
        )
        self.command_line.escape_requested.connect(
            self.handle_command_line_escape
        )
        self.command_line.tab_requested.connect(
            self.handle_dynamic_input_tab
   )

        layout.addWidget(self.ribbon)
        layout.addWidget(self.workspace)
        layout.addWidget(self.command_line)

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
                self.translator.translate("cad.line.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.line.prompt")
            )
            self.command_line.focus_input()

    def activate_polyline_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                PolylineCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                self.translator.translate("cad.pline.active")
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
                self.translator.translate("cad.rectangle.active")
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
                self.translator.translate("cad.circle.active")
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
                self.translator.translate("cad.move.active")
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
                self.translator.translate("cad.copy.active")
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
                self.translator.translate("cad.rotate.active")
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
                self.translator.translate("cad.scale.active")
            )

    def activate_mirror_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                MirrorCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                self.translator.translate("cad.mirror.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.mirror.prompt")
            )
            self.command_line.focus_input()

    def activate_offset_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                OffsetCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                self.translator.translate("cad.offset.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.offset.prompt")
            )
            self.command_line.focus_input()

    def activate_trim_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                TrimCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                self.translator.translate("cad.trim.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.trim.prompt")
            )
            self.command_line.focus_input()


    def activate_extend_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                ExtendCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                self.translator.translate("cad.extend.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.extend.prompt")
            )
            self.command_line.focus_input()


    def activate_fillet_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                FilletCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                self.translator.translate("cad.fillet.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.fillet.prompt")
            )
            self.command_line.focus_input()

    def activate_chamfer_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            canvas.tool_manager.activate(
                ChamferCommand(
                    app_core=self.app_core
                )
            )

            self.statusBar().showMessage(
                self.translator.translate("cad.chamfer.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.chamfer.prompt")
            )
            self.command_line.focus_input()

    def activate_join_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            command = JoinCommand(
                app_core=self.app_core
            )

            canvas.tool_manager.activate(command)

            # Compatibilidad con ToolManager que no invoca begin().
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

            self.statusBar().showMessage(
                self.translator.translate("cad.join.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.join.prompt")
            )
            self.command_line.focus_input()


    def activate_wall_command(self):
        canvas = self.workspace.current_canvas()

        if canvas:
            command = WallCommand(
                app_core=self.app_core
            )

            canvas.tool_manager.activate(command)

            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

            self.statusBar().showMessage(
                self.translator.translate("cad.wall.active")
            )

            self.command_line.set_prompt(
                self.translator.translate("cad.wall.prompt")
            )
            self.command_line.focus_input()

    def activate_wall_node_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = WallNodeCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_opening_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = OpeningCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_door_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = DoorCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_window_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = WindowCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_room_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = RoomCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_room_edit_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = RoomEditCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_room_schedule_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = RoomScheduleCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_slab_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = SlabCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_slab_schedule_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = SlabScheduleCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_standards_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = StandardsCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    def activate_standards_report_command(self):
        canvas = self.workspace.current_canvas()
        if canvas:
            command = StandardsReportCommand(app_core=self.app_core)
            canvas.tool_manager.activate(command)
            begin = getattr(command, "begin", None)
            if callable(begin):
                begin(canvas)

    # ---------------------------------------------------------
    # LÍNEA DE COMANDOS
    # ---------------------------------------------------------

    def handle_command_line_submit(self, text):
        value = str(text).strip()

        if not value:
            return

        command_name = value.upper()

        if command_name in ("LINE", "L"):
            self.activate_line_command()
            return

        if command_name in ("MIRROR", "MI"):
            self.activate_mirror_command()
            return

        if command_name in ("OFFSET", "O"):
            self.activate_offset_command()
            return

        if command_name in ("TRIM", "TR"):
            self.activate_trim_command()
            return

        if command_name in ("EXTEND", "EX"):
            self.activate_extend_command()
            return

        if command_name in ("FILLET", "F"):
            self.activate_fillet_command()
            return

        if command_name in ("CHAMFER", "CHA", "CH"):
            self.activate_chamfer_command()
            return

        if command_name in ("JOIN", "J"):
            self.activate_join_command()
            return

        if command_name in ("WALL", "W", "MURO"):
            self.activate_wall_command()
            return

        if command_name in ("WNODE", "WN", "NODOWALL"):
            self.activate_wall_node_command()
            return

        if command_name in (
            "OPENING",
            "OP",
            "HUECO",
            "ABERTURA",
        ):
            self.activate_opening_command()
            return

        if command_name in (
            "DOOR",
            "PUERTA",
        ):
            self.activate_door_command()
            return

        if command_name in (
            "WINDOW",
            "WIN",
            "VENTANA",
        ):
            self.activate_window_command()
            return

        if command_name in (
            "ROOM",
            "RM",
            "AMBIENTE",
        ):
            self.activate_room_command()
            return

        if command_name in (
            "ROOMEDIT",
            "RE",
            "EDITROOM",
            "EDITARAMBIENTE",
        ):
            self.activate_room_edit_command()
            return

        if command_name in (
            "ROOMSCHEDULE",
            "RS",
            "CUADROAREAS",
            "AREAS",
        ):
            self.activate_room_schedule_command()
            return

        if command_name in (
            "SLAB",
            "LOSA",
            "LJ",
        ):
            self.activate_slab_command()
            return

        if command_name in (
            "SLABSCHEDULE",
            "SS",
            "CUADROLOSAS",
            "LOSAS",
        ):
            self.activate_slab_schedule_command()
            return

        if command_name in (
            "STANDARDS",
            "STANDARD",
            "NORMAS",
            "NORMA",
        ):
            self.activate_standards_command()
            return

        if command_name in (
            "STANDARDSREPORT",
            "NORMASREPORT",
            "REPORTENORMAS",
            "RN",
        ):
            self.activate_standards_report_command()
            return

        if command_name in ("ESC", "CANCEL", "CANCELAR"):
            self.handle_command_line_escape()
            return

        canvas = self.workspace.current_canvas()

        if canvas is None:
            self.statusBar().showMessage(
                self.translator.translate("status.no_canvas")
            )
            return

        current_tool = getattr(
            canvas.tool_manager,
            "current_tool",
            None,
        )

        if current_tool is None:
            self.command_line.reset_prompt()
            self.statusBar().showMessage(
                self.translator.translate("status.unknown_command",value=value)
            )
            return

        text_handler = getattr(
            current_tool,
            "handle_text_input",
            None,
        )

        if not callable(text_handler):
            self.statusBar().showMessage(
                self.translator.translate("status.numeric_input_unsupported")
            )
            return

        accepted = text_handler(
            value,
            canvas,
        )

        if accepted is False:
            self.command_line.focus_input()

    def handle_command_line_escape(self):
        canvas = self.workspace.current_canvas()

        if canvas is not None:
            canvas.tool_manager.cancel(canvas)
            canvas.command_manager.cancel(canvas)

            canvas.preview_geometry = None
            canvas.current_snap_point = None
            canvas.current_snap_type = None

            canvas.highlight.clear()
            canvas.selection_manager.clear()
            canvas.element_selected.emit(None)
            canvas.update()
            canvas.setFocus()

        self.command_line.clear_input()
        self.command_line.reset_prompt()

        self.statusBar().showMessage(
            self.translator.translate("status.command_cancelled")
        )

    def set_command_prompt(self, text):
        self.command_line.set_prompt(text)

    def focus_command_line(self):
        self.command_line.focus_input()

    def handle_dynamic_input_tab(self):
        canvas = self.workspace.current_canvas()

        if canvas is None:
            return

        manager = canvas.get_dynamic_input_manager()

        if (
            manager is None
            or not manager.enabled
            or not manager.visible
        ):
            return

        mode = manager.toggle_mode()

        print(
            f"DYNAMIC INPUT MODE: {mode}"
        )

        self.statusBar().showMessage(
            self.translator.translate("status.dynamic_input",mode=mode)
        )

        canvas.update()

    # ---------------------------------------------------------
    # PROYECTOS NATIVOS .AIAS
    # ---------------------------------------------------------

    def new_project(self):
        if hasattr(self, "project_session"):
            self.project_session.new_project(self.translator.translate("document.untitled"))
        else:
            self.open_new_project_dialog()

    def open_project(self):
        if hasattr(self, "project_session"):
            self.project_session.open_dialog()

    def save_project(self):
        if hasattr(self, "project_session"):
            self.project_session.save()

    def save_project_as(self):
        if hasattr(self, "project_session"):
            self.project_session.save_as()

    def rebuild_recent_projects_menu(self):
        if not hasattr(self, "recent_menu"):
            return
        self.recent_menu.clear()
        session = getattr(self, "project_session", None)
        recent = session.recent_projects() if session is not None else []
        if not recent:
            action = self.recent_menu.addAction(self.translator.translate("recent.none"))
            action.setEnabled(False)
            return
        for path in recent:
            action = self.recent_menu.addAction(Path(path).name)
            action.setToolTip(path)
            action.triggered.connect(lambda checked=False, p=path: self.open_recent_project(p))

    def open_recent_project(self, path):
        if not self.project_session.confirm_discard_changes():
            return
        self.project_session.open_file(path)

    def closeEvent(self, event):
        session = getattr(self, "project_session", None)
        if session is None or session.confirm_discard_changes():
            event.accept()
        else:
            event.ignore()

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
                self.translator.translate("project.created_success",name=nombre)
            )

            self.refresh_project_tree()

    # ---------------------------------------------------------
    # EXPLORADOR DEL PROYECTO
    # ---------------------------------------------------------

    def create_project_explorer(self):
        dock = QDockWidget(
            self.translator.translate("panel.project_explorer"),
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
        dock = QDockWidget(self.translator.translate("panel.bim_inspector"), self)
        property_service = None
        shared_library = None
        kernel = getattr(getattr(self, "app_core", None), "kernel", None)
        if kernel is not None:
            services = getattr(kernel, "services", None)
            if services is not None:
                try:
                    property_service = services.get("property_service")
                except Exception:
                    pass
                try:
                    shared_library = services.get("shared_parameter_library")
                except Exception:
                    pass
        self.properties_inspector = BimPropertyInspector(
            InspectorController(property_service, shared_library), self
        )
        dock.setWidget(self.properties_inspector)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def clear_properties(self):
        self.properties_inspector.clear()

    def show_element_properties(self, element):
        if element is None:
            self.clear_properties()
            self.statusBar().showMessage(self.translator.translate("status.no_selection"))
            return
        self.properties_inspector.inspect(element)
        self.statusBar().showMessage(
            self.translator.translate("status.selected",name=getattr(element,"name",self.translator.translate("element.default")))
        )

    # ---------------------------------------------------------
    # ASISTENTE IA
    # ---------------------------------------------------------

    def create_layers_panel(self):
        dock = QDockWidget(
            self.translator.translate("panel.layers"),
            self,
        )

        container = QWidget()
        layout = QVBoxLayout(container)

        self.layers_list = QListWidget()
        layout.addWidget(self.layers_list)

        buttons_layout = QHBoxLayout()
        self.new_layer_btn = QPushButton(self.translator.translate("layer.new"))
        self.activate_layer_btn = QPushButton(self.translator.translate("layer.activate"))
        self.toggle_visibility_btn = QPushButton(self.translator.translate("layer.visibility"))
        self.toggle_lock_btn = QPushButton(self.translator.translate("layer.lock"))

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
                self.statusBar().showMessage(self.translator.translate("status.layer_visible", name=layer_name))
            else:
                self.statusBar().showMessage(self.translator.translate("status.layer_hidden", name=layer_name))

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
                self.statusBar().showMessage(self.translator.translate("status.layer_locked", name=layer_name))
            else:
                self.statusBar().showMessage(self.translator.translate("status.layer_unlocked", name=layer_name))

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
            self.translator.translate("panel.ai_assistant"),
            self,
        )

        texto = QTextEdit()

        texto.setPlaceholderText(
            self.translator.translate("ai.placeholder")
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
            self.translator.translate("status.ready")
        )

        self.setStatusBar(barra)

    # ---------------------------------------------------------
    # TEMA
    # ---------------------------------------------------------

    def apply_theme(self, theme="dark"):
        """Apply the governed semantic theme to the complete application shell."""
        self.setStyleSheet(render_qss(theme))
        self._aias_theme = theme

    def apply_dark_theme(self):
        """Compatibility entry point retained for existing launchers."""
        self.apply_theme("dark")
