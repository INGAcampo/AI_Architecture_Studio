"""
AI Architecture Studio
History Action - Move

Dynamic Input Universal - Package 3.3
"""

from engines.transform.transform_manager import TransformManager


class MoveAction:
    """
    Acción reversible para MOVE.

    Los objetos ya están desplazados cuando la acción entra
    al HistoryManager. undo() aplica el vector contrario y
    redo() vuelve a aplicar el vector original.
    """

    def __init__(
        self,
        elements,
        dx,
        dy,
        dz=0.0,
    ):
        self.elements = list(elements or [])
        self.dx = float(dx)
        self.dy = float(dy)
        self.dz = float(dz)

    def undo(self):
        TransformManager.move_elements(
            self.elements,
            -self.dx,
            -self.dy,
            -self.dz,
        )

    def redo(self):
        TransformManager.move_elements(
            self.elements,
            self.dx,
            self.dy,
            self.dz,
        )
