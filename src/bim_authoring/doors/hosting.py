from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DoorHostResult:
    door_id: str
    wall_id: str
    opening_id: str
    success: bool

class DoorHostAdapter:
    def host(self, door, wall_engine, opening_class):
        wall = wall_engine.walls[door.host_wall_id]
        opening = opening_class(
            opening_id=f"OPEN-{door.door_id}",
            wall_id=door.host_wall_id,
            offset=door.offset,
            width=door.door_type.width,
            sill_height=door.sill_height,
            height=door.door_type.height,
            hosted_element_id=door.door_id,
        )
        wall_engine.add_opening(opening)
        return DoorHostResult(
            door.door_id,
            wall.wall_id,
            opening.opening_id,
            True,
        )
