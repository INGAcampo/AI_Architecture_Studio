from dataclasses import dataclass
from cad_professional_kernel.geometry import Point2D

@dataclass(slots=True)
class RubberBand:
    anchor: Point2D | None = None
    cursor: Point2D | None = None
    visible: bool = False

    def start(self, anchor: Point2D) -> None:
        self.anchor = anchor
        self.cursor = anchor
        self.visible = True

    def update(self, cursor: Point2D) -> None:
        if self.visible:
            self.cursor = cursor

    def stop(self) -> None:
        self.anchor = None
        self.cursor = None
        self.visible = False
