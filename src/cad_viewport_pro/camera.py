from dataclasses import dataclass

@dataclass(slots=True)
class Camera2D:
    center_x: float = 0.0
    center_y: float = 0.0
    zoom: float = 1.0

    def pan(self, dx_world: float, dy_world: float) -> None:
        self.center_x += dx_world
        self.center_y += dy_world

    def set_zoom(self, value: float) -> None:
        self.zoom = max(0.01, min(10000.0, float(value)))

    def zoom_by(self, factor: float) -> None:
        self.set_zoom(self.zoom * float(factor))
