from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ViewportTheme:
    background: tuple[int, int, int] = (24, 30, 38)
    minor_grid: tuple[int, int, int] = (37, 46, 57)
    major_grid: tuple[int, int, int] = (56, 68, 82)
    axis_x: tuple[int, int, int] = (105, 65, 65)
    axis_y: tuple[int, int, int] = (65, 105, 75)
    entity: tuple[int, int, int] = (225, 232, 240)
    selected: tuple[int, int, int] = (70, 160, 255)
    snap: tuple[int, int, int] = (255, 190, 60)
    crosshair: tuple[int, int, int] = (195, 205, 215)
    selection_window: tuple[int, int, int] = (55, 135, 255)
    selection_crossing: tuple[int, int, int] = (75, 180, 100)
