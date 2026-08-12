from dataclasses import dataclass

@dataclass(slots=True)
class ViewportSettings:
    grid_enabled: bool = True
    snap_enabled: bool = True
    ortho_enabled: bool = False
    polar_enabled: bool = False
    major_grid_every: int = 5
    minor_grid_alpha: int = 38
    major_grid_alpha: int = 72
    entity_line_width: float = 1.25
    selected_line_width: float = 2.25
    snap_tolerance_pixels: float = 10.0
    crosshair_size_pixels: int = 18
