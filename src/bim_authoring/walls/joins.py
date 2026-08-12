from dataclasses import dataclass
from enum import Enum

class WallJoinType(str, Enum):
    BUTT = "butt"
    MITER = "miter"
    SQUARE_OFF = "square_off"

@dataclass(frozen=True, slots=True)
class WallJoin:
    join_id: str
    wall_a_id: str
    wall_b_id: str
    join_type: WallJoinType

class WallJoinManager:
    def __init__(self):
        self._joins = {}

    def connect(self, join):
        if join.wall_a_id == join.wall_b_id:
            raise ValueError("No se puede unir un muro consigo mismo")
        self._joins[join.join_id] = join
        return join

    def for_wall(self, wall_id):
        return tuple(
            join for join in self._joins.values()
            if wall_id in {join.wall_a_id, join.wall_b_id}
        )

    def disconnect(self, join_id):
        return self._joins.pop(join_id)
