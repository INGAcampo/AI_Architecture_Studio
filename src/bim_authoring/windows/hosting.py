from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WindowHostResult:
    window_id: str
    wall_id: str
    opening_id: str
    success: bool

class WindowHostAdapter:
    def host(self, window, wall_engine, opening_class):
        wall = wall_engine.walls[window.host_wall_id]
        opening = opening_class(
            opening_id=f"OPEN-{window.window_id}",
            wall_id=window.host_wall_id,
            offset=window.offset,
            width=window.window_type.width,
            sill_height=window.sill_height,
            height=window.window_type.height,
            hosted_element_id=window.window_id,
        )
        wall_engine.add_opening(opening)
        return WindowHostResult(
            window.window_id,
            wall.wall_id,
            opening.opening_id,
            True,
        )
