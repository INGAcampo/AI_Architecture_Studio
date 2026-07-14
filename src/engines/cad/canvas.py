"""
AI Architecture Studio
CAD Engine - Canvas

SNAP Professional v2
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

    def __init__(
        self,
        scene=None,
        parent=None,
    ):
        super().__init__(parent)

        self.scene = scene

        self.camera = Camera()
        self.grid = Grid()
        self.renderer = Renderer()

        self.command_manager = CommandManager()
        self.tool_manager = ToolManager()

        self.coordinates = CoordinateSystem()

        self.selection_manager = (
            SelectionManager()
        )

        self.highlight = Highlight()

        self.cursor_position = (
            0.0,
            0.0,
        )

        self.snapped_cursor_position = (
            0.0,
            0.0,
        )

        self.current_snap_point = None
        self.current_snap_type = None

        self.preview_geometry = None

        self.is_panning = False
        self.last_pan_position = None

        self.setMinimumSize(
            800,
            500,
        )

        self.setMouseTracking(True)
        self.setFocusPolicy(
            Qt.StrongFocus
        )

    # ---------------------------------------------------------
    # SERVICIOS
    # ---------------------------------------------------------

    def get_kernel_service(
        self,
        service_name,
    ):
        kernel = getattr(
            self.scene,
            "kernel",
            None,
        )

        if kernel is None:
            return None

        return kernel.services.get(
            service_name
        )

    def get_history_manager(self):
        return self.get_kernel_service(
            "history_manager"
        )

    def get_ortho_manager(self):
        return self.get_kernel_service(
            "ortho_manager"
        )

    def get_snap_engine(self):
        return self.get_kernel_service(
            "snap_engine"
        )

    # ---------------------------------------------------------
    # CURSOR CAD
    # ---------------------------------------------------------

    def update_snap(self):
        x, y = self.cursor_position

        cursor_point = Point(
            x,
            y,
            0.0,
        )

        snap_engine = (
            self.get_snap_engine()
        )

        if snap_engine is None:
            self.current_snap_point = None
            self.current_snap_type = None
            self.snapped_cursor_position = (
                x,
                y,
            )
            return

        snapped_point, snap_type = (
            snap_engine.snap_point(
                cursor_point,
                self.scene,
            )
        )

        self.current_snap_point = (
            snapped_point
            if snap_type is not None
            else None
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

        x, y = self.cursor_position

        return Point(
            x,
            y,
            0.0,
        )

    # ---------------------------------------------------------
    # RENDERIZADO
    # ---------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            QColor(30, 30, 30),
        )

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
            highlighted=(
                self.highlight.current()
            ),
        )

        if self.preview_geometry is not None:
            self.renderer.draw_preview(
                painter,
                self.camera,
                self.preview_geometry,
            )

        self.renderer.draw_snap_marker(
            painter,
            self.camera,
            self.current_snap_point,
            self.current_snap_type,
        )

        painter.setPen(
            QColor(200, 200, 200)
        )

        x, y = (
            self.snapped_cursor_position
        )

        painter.drawText(
            20,
            30,
            f"X: {x:.2f} m   "
            f"Y: {y:.2f} m",
        )

        highlighted = (
            self.highlight.current()
        )

        if highlighted is not None:
            painter.drawText(
                20,
                50,
                f"Objeto: "
                f"{highlighted.name}",
            )

        ortho_manager = (
            self.get_ortho_manager()
        )

        snap_engine = (
            self.get_snap_engine()
        )

        status_items = []

        if (
            ortho_manager is not None
            and ortho_manager.enabled
        ):
            status_items.append(
                "ORTHO: ON"
            )

        if (
            snap_engine is not None
            and snap_engine.enabled
        ):
            status_items.append(
                "SNAP: ON"
            )

        if status_items:
            painter.drawText(
                20,
                70,
                " | ".join(status_items),
            )

        painter.end()

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouseMoveEvent(self, event):
        if (
            self.is_panning
            and self.last_pan_position
            is not None
        ):
            dx = (
                event.position().x()
                - self.last_pan_position.x()
            )

            dy = (
                event.position().y()
                - self.last_pan_position.y()
            )

            self.camera.pan(
                dx,
                dy,
            )

            self.last_pan_position = (
                event.position()
            )

            self.update()
            return

        self.cursor_position = (
            self.coordinates.screen_to_world(
                event.position().x(),
                event.position().y(),
                self.camera,
            )
        )

        self.update_snap()

        mouse_point = (
            self.get_input_point()
        )

        element = HitTest.pick(
            mouse_point,
            self.scene,
        )

        self.highlight.set(element)

        if self.tool_manager.current_tool:
            self.tool_manager.current_tool.mouse_move(
                event,
                self,
            )
        else:
            self.command_manager.mouse_move(
                event,
                self,
            )

        self.update()

    def mousePressEvent(self, event):
        self.setFocus()

        if event.button() == Qt.MiddleButton:
            self.is_panning = True
            self.last_pan_position = (
                event.position()
            )
            return

        self.update_snap()

        mouse_point = (
            self.get_input_point()
        )

        selected = HitTest.pick(
            mouse_point,
            self.scene,
        )

        if selected is not None:
            self.selection_manager.select(
                selected
            )

            self.element_selected.emit(
                selected
            )

            print(
                f"Seleccionado: "
                f"{selected.name}"
            )
        else:
            self.selection_manager.clear()
            self.element_selected.emit(None)

        if self.tool_manager.current_tool:
            self.tool_manager.current_tool.mouse_press(
                event,
                self,
            )
        else:
            self.command_manager.mouse_press(
                event,
                self,
            )

        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.is_panning = False
            self.last_pan_position = None
            self.update()

    # ---------------------------------------------------------
    # TECLADO
    # ---------------------------------------------------------

    def keyPressEvent(self, event):
        # SNAP F3
        if event.key() == Qt.Key_F3:
            snap_engine = (
                self.get_snap_engine()
            )

            if snap_engine is None:
                print(
                    "SNAP: servicio no disponible"
                )
                return

            enabled = snap_engine.toggle()

            state = (
                "ACTIVADO"
                if enabled
                else "DESACTIVADO"
            )

            if not enabled:
                self.current_snap_point = None
                self.current_snap_type = None

            main_window = self.window()

            if hasattr(
                main_window,
                "statusBar",
            ):
                main_window.statusBar().showMessage(
                    f"SNAP {state}"
                )

            self.update()
            return

        # ORTHO F8
        if event.key() == Qt.Key_F8:
            ortho_manager = (
                self.get_ortho_manager()
            )

            if ortho_manager is None:
                print(
                    "ORTHO: servicio no disponible"
                )
                return

            enabled = ortho_manager.toggle()

            state = (
                "ACTIVADO"
                if enabled
                else "DESACTIVADO"
            )

            main_window = self.window()

            if hasattr(
                main_window,
                "statusBar",
            ):
                main_window.statusBar().showMessage(
                    f"ORTHO {state}"
                )

            self.update()
            return

        if event.matches(
            QKeySequence.Undo
        ):
            history = (
                self.get_history_manager()
            )

            if history is not None:
                history.undo()

            self.selection_manager.clear()
            self.highlight.clear()
            self.element_selected.emit(None)
            self.update()

            print("UNDO ejecutado")
            return

        if event.matches(
            QKeySequence.Redo
        ):
            history = (
                self.get_history_manager()
            )

            if history is not None:
                history.redo()

            self.selection_manager.clear()
            self.highlight.clear()
            self.element_selected.emit(None)
            self.update()

            print("REDO ejecutado")
            return

        if event.key() == Qt.Key_Delete:
            delete_command = DeleteCommand()
            delete_command.execute(self)

            self.element_selected.emit(None)
            self.update()
            return

        if event.key() == Qt.Key_Escape:
            self.tool_manager.cancel(self)
            self.command_manager.cancel(self)

            self.selection_manager.clear()
            self.highlight.clear()
            self.element_selected.emit(None)

            self.preview_geometry = None
            self.current_snap_point = None
            self.current_snap_type = None

            self.update()
            return

        if self.tool_manager.current_tool:
            self.tool_manager.current_tool.key_press(
                event,
                self,
            )
        else:
            self.command_manager.key_press(
                event,
                self,
            )

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