"""Undo/Redo para edición paramétrica de nodos WALL 5.0.4.4."""

from engines.geometry.point import Point
from engines.architectural.wall_network import WallNetwork


class MoveWallNodeAction:
    def __init__(self, scene, before_paths, after_paths):
        self.scene = scene
        self.before_paths = self._clone_map(before_paths)
        self.after_paths = self._clone_map(after_paths)

    @staticmethod
    def _clone_map(source):
        return {
            wall: [Point(p.x, p.y, getattr(p, "z", 0.0)) for p in path]
            for wall, path in source.items()
        }

    def _apply(self, paths):
        for wall, path in paths.items():
            setter = getattr(wall, "set_path", None)
            if callable(setter):
                setter(path)
            else:
                wall.path = [Point(p.x, p.y, getattr(p, "z", 0.0)) for p in path]
                rebuild = getattr(wall, "rebuild_wall_geometry", None)
                if callable(rebuild):
                    rebuild()
        if self.scene is not None:
            self.scene.wall_network_signature = None
            WallNetwork.ensure_scene(self.scene)

    def undo(self):
        self._apply(self.before_paths)

    def redo(self):
        self._apply(self.after_paths)
