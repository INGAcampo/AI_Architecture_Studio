from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ScreenPoint:
    x: float
    y: float

@dataclass(slots=True)
class ViewTransform:
    width: float
    height: float
    center_x: float
    center_y: float
    zoom: float

    def world_to_screen(self, x: float, y: float) -> ScreenPoint:
        return ScreenPoint(
            self.width/2 + (x-self.center_x)*self.zoom,
            self.height/2 - (y-self.center_y)*self.zoom,
        )

    def screen_to_world(self, x: float, y: float) -> ScreenPoint:
        return ScreenPoint(
            self.center_x + (x-self.width/2)/self.zoom,
            self.center_y - (y-self.height/2)/self.zoom,
        )
