"""Comando WNODE — selección y movimiento de nodos WALL 5.0.4.4."""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.move_wall_node_action import MoveWallNodeAction
from engines.architectural.wall_network import WallNetwork
from engines.architectural.wall_node_editor import WallNodeEditor
from engines.geometry.point import Point


class WallNodeCommand(BaseCommand):
    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "WNODE"
        self.selected_node_id = None

    def _window(self, canvas):
        getter = getattr(canvas, "window", None)
        return getter() if callable(getter) else None

    def _status(self, canvas, text):
        window = self._window(canvas)
        if window is not None:
            window.statusBar().showMessage(text)

    def _prompt(self, canvas, text):
        window = self._window(canvas)
        command_line = getattr(window, "command_line", None)
        if command_line is not None:
            command_line.set_prompt(text)
            command_line.focus_input()

    def _scene(self, canvas):
        return getattr(self.app_core, "scene", getattr(canvas, "scene", None))

    def _point(self, canvas):
        getter = getattr(canvas, "get_input_point", None)
        if callable(getter):
            return getter()
        x, y = canvas.cursor_position
        return Point(x, y, 0.0)

    def begin(self, canvas):
        scene = self._scene(canvas)
        network = WallNetwork.ensure_scene(scene)
        scene.show_wall_nodes = True
        scene.active_wall_node_id = None
        self._prompt(canvas, "Seleccione nodo WALL:")
        self._status(canvas, f"WNODE activo: {len(network.nodes)} nodo(s) disponibles")
        canvas.update()

    def _node_by_id(self, network, node_id):
        for node in network.nodes:
            if node.node_id == node_id:
                return node
        return None

    def mouse_press(self, event, canvas):
        scene = self._scene(canvas)
        network = WallNetwork.ensure_scene(scene)
        point = self._point(canvas)

        if self.selected_node_id is None:
            node = WallNodeEditor.nearest_node(network, point)
            if node is None:
                self._status(canvas, "WNODE: no se encontró un nodo cercano")
                return
            self.selected_node_id = node.node_id
            scene.active_wall_node_id = node.node_id
            self._prompt(canvas, "Nuevo punto del nodo:")
            self._status(canvas, f"WNODE: {node.node_id} ({node.node_type}) seleccionado")
            canvas.update()
            return

        node = self._node_by_id(network, self.selected_node_id)
        if node is None:
            self.selected_node_id = None
            scene.active_wall_node_id = None
            self._status(canvas, "WNODE: el nodo cambió; selecciónelo nuevamente")
            canvas.update()
            return

        before, after = WallNodeEditor.move_node(scene, node, point)
        if before and self.app_core is not None:
            self.app_core.history.push(MoveWallNodeAction(scene, before, after))

        updated = WallNetwork.ensure_scene(scene)
        nearest = WallNodeEditor.nearest_node(updated, point, tolerance=1.0e-3)
        self.selected_node_id = nearest.node_id if nearest else None
        scene.active_wall_node_id = self.selected_node_id

        self._status(canvas, "WNODE: nodo movido; seleccione otro nodo o ESC")
        self._prompt(canvas, "Seleccione nodo WALL:")
        self.selected_node_id = None
        scene.active_wall_node_id = None
        canvas.update()

    def key_press(self, event, canvas):
        if event.key() == Qt.Key_Escape:
            self.cancel(canvas)

    def cancel(self, canvas=None):
        self.selected_node_id = None
        if canvas is not None:
            scene = self._scene(canvas)
            if scene is not None:
                scene.active_wall_node_id = None
                scene.show_wall_nodes = False
            self._prompt(canvas, "Comando:")
            self._status(canvas, "WNODE cancelado")
            canvas.update()

    def deactivate(self):
        self.selected_node_id = None
