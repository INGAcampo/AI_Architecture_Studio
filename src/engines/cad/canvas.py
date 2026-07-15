"""
AI Architecture Studio
CAD Engine - Canvas

Dynamic Input v2
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QKeySequence, QPainter
from PySide6.QtWidgets import QWidget

from commands.cad.delete_command import DeleteCommand
from commands.command_manager import CommandManager
from commands.tool_manager import ToolManager
from engines.cad.camera import Camera
from engines.cad.coordinates import CoordinateSystem
from engines.cad.grid import Grid
from engines.cad.renderer import Renderer
from engines.geometry.point import Point
from engines.selection.highlight import Highlight
from engines.selection.hit_test import HitTest
from engines.selection.selection_manager import SelectionManager


class CadCanvas(QWidget):

    element_selected = Signal(object)

    def __init__(self, scene=None, parent=None):
        super().__init__(parent)

        self.scene = scene
        self.camera = Camera()
        self.grid = Grid()
        self.renderer = Renderer()
        self.command_manager = CommandManager()
        self.tool_manager = ToolManager()
        self.coordinates = CoordinateSystem()
        self.selection_manager = SelectionManager()
        kernel = getattr(
            self.scene,
            "kernel",
            None,
        )

        if kernel is not None:

            kernel.services.register(
                "selection_manager",
                self.selection_manager,
            )
        self.highlight = Highlight()

        self.cursor_position = (0.0, 0.0)
        self.snapped_cursor_position = (0.0, 0.0)
        self.current_snap_point = None
        self.current_snap_type = None
        self.preview_geometry = None

        self.is_panning = False
        self.last_pan_position = None

        self.is_window_selecting = False
        self.selection_window_start = None
        self.selection_window_end = None
        self.selection_window_additive = False

        self.setMinimumSize(800, 500)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    # ---------------------------------------------------------
    # SERVICIOS
    # ---------------------------------------------------------

    def get_kernel_service(self, service_name):
        kernel = getattr(self.scene, "kernel", None)

        if kernel is None:
            return None

        return kernel.services.get(service_name)

    def get_history_manager(self):
        return self.get_kernel_service("history_manager")

    def get_ortho_manager(self):
        return self.get_kernel_service("ortho_manager")

    def get_snap_engine(self):
        return self.get_kernel_service("snap_engine")

    def get_dynamic_input_manager(self):
        return self.get_kernel_service("dynamic_input_manager")

    # ---------------------------------------------------------
    # CURSOR
    # ---------------------------------------------------------

    def get_raw_cursor_point(self):
        x, y = self.cursor_position
        return Point(x, y, 0.0)

    def update_snap(self):
        cursor_point = self.get_raw_cursor_point()
        snap_engine = self.get_snap_engine()

        if snap_engine is None:
            self.current_snap_point = None
            self.current_snap_type = None
            self.snapped_cursor_position = (
                cursor_point.x,
                cursor_point.y,
            )
            return

        snapped_point, snap_type = snap_engine.snap_point(
            cursor_point,
            self.scene,
        )

        self.current_snap_point = (
            snapped_point if snap_type is not None else None
        )
        self.current_snap_type = snap_type
        self.snapped_cursor_position = (
            snapped_point.x,
            snapped_point.y,
        )

    def get_input_point(self):
        if self.current_snap_point is not None:
            return Point(
                self.current_snap_point.x,
                self.current_snap_point.y,
                self.current_snap_point.z,
            )

        return self.get_raw_cursor_point()

    def update_dynamic_input(self, event=None):
        manager = self.get_dynamic_input_manager()

        if manager is None:
            return

        current_tool = getattr(
            self.tool_manager,
            "current_tool",
            None,
        )
        base_point = getattr(
            current_tool,
            "first_point",
            None,
        )

        if current_tool is None or base_point is None:
            manager.hide()
            return

        current_point = self.get_input_point()
        ortho_manager = self.get_ortho_manager()

        if ortho_manager is not None and ortho_manager.enabled:
            current_point = ortho_manager.apply(
                base_point,
                current_point,
            )

        manager.set_base_point(base_point)
        manager.update_point(current_point)

        if event is not None:
            manager.set_screen_position(
                event.position().x(),
                event.position().y(),
            )

    # ---------------------------------------------------------
    # SELECCIÓN
    # ---------------------------------------------------------

    def emit_selection_state(self):
        selected = self.selection_manager.selected_elements()

        if len(selected) == 1:
            self.element_selected.emit(selected[0])
        else:
            self.element_selected.emit(None)

        main_window = self.window()

        if not hasattr(main_window, "statusBar"):
            return

        count = len(selected)

        if count == 0:
            message = "Ningún objeto seleccionado"
        elif count == 1:
            message = "1 objeto seleccionado"
        else:
            message = f"{count} objetos seleccionados"

        main_window.statusBar().showMessage(message)

    def clear_selection_window(self):
        self.is_window_selecting = False
        self.selection_window_start = None
        self.selection_window_end = None
        self.selection_window_additive = False

    # ---------------------------------------------------------
    # RENDERIZADO
    # ---------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        self.grid.draw(
            painter,
            self.width(),
            self.height(),
            self.camera,
        )

        self.renderer.draw_scene(
            painter=painter,
            camera=self.camera,
            scene=self.scene,
            highlighted=self.highlight.current(),
            selected_elements=(
                self.selection_manager.selected_elements()
            ),
        )

        if self.preview_geometry is not None:
            self.renderer.draw_preview(
                painter,
                self.camera,
                self.preview_geometry,
            )

        if (
            self.is_window_selecting
            and self.selection_window_start is not None
            and self.selection_window_end is not None
        ):
            crossing = (
                self.selection_window_end.x
                < self.selection_window_start.x
            )
            self.renderer.draw_selection_window(
                painter,
                self.camera,
                self.selection_window_start,
                self.selection_window_end,
                crossing=crossing,
            )

        self.renderer.draw_snap_marker(
            painter,
            self.camera,
            self.current_snap_point,
            self.current_snap_type,
        )

        painter.setPen(QColor(200, 200, 200))
        x, y = self.snapped_cursor_position
        painter.drawText(
            20,
            30,
            f"X: {x:.2f} m   Y: {y:.2f} m",
        )

        highlighted = self.highlight.current()
        if highlighted is not None:
            painter.drawText(
                20,
                50,
                f"Objeto: {highlighted.name}",
            )

        status_items = []

        ortho_manager = self.get_ortho_manager()
        if ortho_manager is not None and ortho_manager.enabled:
            status_items.append("ORTHO: ON")

        snap_engine = self.get_snap_engine()
        if snap_engine is not None and snap_engine.enabled:
            status_items.append("SNAP: ON")

        dynamic_input_manager = self.get_dynamic_input_manager()
        if (
            dynamic_input_manager is not None
            and dynamic_input_manager.enabled
        ):
            status_items.append("DYN: ON")

        selected_count = self.selection_manager.selected_count()
        if selected_count:
            status_items.append(f"SELECTED: {selected_count}")

        if status_items:
            painter.drawText(20, 70, " | ".join(status_items))

        painter.end()

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouseMoveEvent(self, event):
        if self.is_panning and self.last_pan_position is not None:
            dx = event.position().x() - self.last_pan_position.x()
            dy = event.position().y() - self.last_pan_position.y()
            self.camera.pan(dx, dy)
            self.last_pan_position = event.position()
            self.update()
            return

        self.cursor_position = self.coordinates.screen_to_world(
            event.position().x(),
            event.position().y(),
            self.camera,
        )

        self.update_snap()
        self.update_dynamic_input(event)

        if self.is_window_selecting:
            self.selection_window_end = self.get_raw_cursor_point()
            self.highlight.clear()
            self.update()
            return

        mouse_point = self.get_input_point()
        grip = self.selection_manager.pick_grip(
            mouse_point
        )

        self.selection_manager.set_hovered_grip(

            grip
        )
        grip
        element = HitTest.pick(mouse_point, self.scene)
        self.highlight.set(element)

        if self.tool_manager.current_tool:
            self.tool_manager.current_tool.mouse_move(event, self)
        else:
            self.command_manager.mouse_move(event, self)

        self.update()

    def mousePressEvent(self, event):
        self.setFocus()

        if event.button() == Qt.MiddleButton:
            self.is_panning = True
            self.last_pan_position = event.position()
            return

        if event.button() != Qt.LeftButton:
            return

        self.update_snap()

        if self.tool_manager.current_tool:
            self.tool_manager.current_tool.mouse_press(event, self)
            self.update_dynamic_input(event)
            self.update()
            return

        mouse_point = self.get_input_point()
        selected = HitTest.pick(mouse_point, self.scene)
        ctrl_pressed = bool(
            event.modifiers() & Qt.ControlModifier
        )

        if selected is not None:
            if ctrl_pressed:
                self.selection_manager.toggle_selection(selected)
            else:
                self.selection_manager.select(selected)

            self.highlight.clear()
            self.emit_selection_state()
            self.update()
            return

        self.is_window_selecting = True
        self.selection_window_start = self.get_raw_cursor_point()
        self.selection_window_end = Point(
            self.selection_window_start.x,
            self.selection_window_start.y,
            self.selection_window_start.z,
        )
        self.selection_window_additive = ctrl_pressed

        if not ctrl_pressed:
            self.selection_manager.clear()
            self.emit_selection_state()

        self.highlight.clear()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.is_panning = False
            self.last_pan_position = None
            self.update()
            return

        if (
            event.button() != Qt.LeftButton
            or not self.is_window_selecting
        ):
            return

        self.selection_window_end = self.get_raw_cursor_point()
        crossing = (
            self.selection_window_end.x
            < self.selection_window_start.x
        )

        selected_elements = HitTest.select_window(
            self.selection_window_start,
            self.selection_window_end,
            self.scene,
            crossing=crossing,
        )

        if self.selection_window_additive:
            self.selection_manager.add_many_to_selection(
                selected_elements
            )
        else:
            self.selection_manager.replace_selection(
                selected_elements
            )

        self.clear_selection_window()
        self.emit_selection_state()
        self.update()

    # ---------------------------------------------------------
    # TECLADO
    # ---------------------------------------------------------

    def keyPressEvent(self, event):
        # DYNAMIC INPUT F12
        if event.key() == Qt.Key_F12:
            manager = self.get_dynamic_input_manager()

            if manager is None:
                print("DYNAMIC INPUT: servicio no disponible")
                return

            enabled = manager.toggle()
            state = "ACTIVADO" if enabled else "DESACTIVADO"
            main_window = self.window()

            if hasattr(main_window, "statusBar"):
                main_window.statusBar().showMessage(
                    f"DYNAMIC INPUT {state}"
                )

            self.update()
            return

        # TAB alterna distancia / ángulo
        if event.key() == Qt.Key_Tab:
            manager = self.get_dynamic_input_manager()

            if (
                manager is not None
                and manager.enabled
                and manager.visible
            ):
                mode = manager.toggle_mode()
                print(f"DYNAMIC INPUT MODE: {mode}")
                self.update()
                return

        # SNAP F3
        if event.key() == Qt.Key_F3:
            snap_engine = self.get_snap_engine()

            if snap_engine is None:
                print("SNAP: servicio no disponible")
                return

            enabled = snap_engine.toggle()
            state = "ACTIVADO" if enabled else "DESACTIVADO"

            if not enabled:
                self.current_snap_point = None
                self.current_snap_type = None

            main_window = self.window()
            if hasattr(main_window, "statusBar"):
                main_window.statusBar().showMessage(
                    f"SNAP {state}"
                )

            self.update()
            return

        # ORTHO F8
        if event.key() == Qt.Key_F8:
            ortho_manager = self.get_ortho_manager()

            if ortho_manager is None:
                print("ORTHO: servicio no disponible")
                return

            enabled = ortho_manager.toggle()
            state = "ACTIVADO" if enabled else "DESACTIVADO"
            main_window = self.window()

            if hasattr(main_window, "statusBar"):
                main_window.statusBar().showMessage(
                    f"ORTHO {state}"
                )

            self.update()
            return

        # UNDO
        if event.matches(QKeySequence.Undo):
            history = self.get_history_manager()
            if history is not None:
                history.undo()

            self.selection_manager.clear()
            self.highlight.clear()
            self.emit_selection_state()
            self.update()
            print("UNDO ejecutado")
            return

        # REDO
        if event.matches(QKeySequence.Redo):
            history = self.get_history_manager()
            if history is not None:
                history.redo()

            self.selection_manager.clear()
            self.highlight.clear()
            self.emit_selection_state()
            self.update()
            print("REDO ejecutado")
            return

        # DELETE
        if event.key() == Qt.Key_Delete:
            delete_command = DeleteCommand()
            delete_command.execute(self)
            self.emit_selection_state()
            self.update()
            return

        # ESCAPE
        if event.key() == Qt.Key_Escape:
            self.clear_selection_window()

            manager = self.get_dynamic_input_manager()
            if manager is not None:
                manager.reset()

            self.tool_manager.cancel(self)
            self.command_manager.cancel(self)
            self.selection_manager.clear()
            self.highlight.clear()
            self.preview_geometry = None
            self.current_snap_point = None
            self.current_snap_type = None
            self.emit_selection_state()
            self.update()
            return

        if self.tool_manager.current_tool:
            self.tool_manager.current_tool.key_press(event, self)
        else:
            self.command_manager.key_press(event, self)

    # ---------------------------------------------------------
    # ZOOM
    # ---------------------------------------------------------

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        if delta > 0:
            self.camera.zoom_at(1.10)
        else:
            self.camera.zoom_at(0.90)

        self.update()