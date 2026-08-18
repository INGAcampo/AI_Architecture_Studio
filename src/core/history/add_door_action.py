"""Undo/Redo idempotente para una puerta BIM."""

from engines.architectural.door_engine import DoorEngine


class AddDoorAction:
    def __init__(
        self,
        scene,
        wall,
        door,
    ):
        self.scene = scene
        self.wall = wall
        self.door = door
        self.door_id = getattr(
            door,
            "door_id",
            None,
        )
        self.opening = getattr(
            door,
            "opening",
            None,
        )
        self.opening_id = getattr(
            self.opening,
            "opening_id",
            None,
        )
        self.is_applied = DoorEngine.contains_door(
            wall,
            door=door,
            door_id=self.door_id,
        )

    def _invalidate(self):
        if self.scene is not None:
            self.scene.wall_network_signature = None

    def undo(self):
        if not self.is_applied:
            return False

        removed = DoorEngine.remove_from_wall(
            self.wall,
            self.door,
        )

        if removed:
            self.is_applied = False
            self._invalidate()

        return removed

    def redo(self):
        if self.is_applied:
            return False

        existing = DoorEngine.find_door(
            self.wall,
            door_id=self.door_id,
        )

        if existing is not None:
            self.door = existing
            self.opening = existing.opening
            self.is_applied = True
            self._invalidate()
            return False

        self.opening.attach_door(
            self.door
        )
        result = DoorEngine.add_to_wall(
            self.wall,
            self.door,
        )

        self.door = result
        self.opening = result.opening
        self.is_applied = True
        self._invalidate()
        return True
