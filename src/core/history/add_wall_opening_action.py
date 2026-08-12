"""Undo/Redo para agregar un hueco paramétrico a un muro."""

from engines.architectural.opening_engine import OpeningEngine


class AddWallOpeningAction:
    def __init__(self, scene, wall, opening):
        self.scene = scene
        self.wall = wall
        self.opening = opening

    def _invalidate(self):
        if self.scene is not None:
            self.scene.wall_network_signature = None

    def undo(self):
        OpeningEngine.remove_from_wall(self.wall, self.opening)
        self._invalidate()

    def redo(self):
        OpeningEngine.add_to_wall(self.wall, self.opening)
        self._invalidate()
