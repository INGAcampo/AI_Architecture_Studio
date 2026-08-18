"""Undo / Redo idempotente para ROOM."""

from engines.architectural.room_engine import RoomEngine


class AddRoomAction:
    def __init__(self, scene, room):
        self.scene = scene
        self.room = room
        self.room_id = getattr(room, "room_id", None)
        self.is_applied = room in RoomEngine.scene_rooms(scene)

    def undo(self):
        if not self.is_applied:
            return False
        removed = RoomEngine.remove_from_scene(self.scene, self.room)
        if removed:
            self.is_applied = False
        return removed

    def redo(self):
        if self.is_applied:
            return False

        for candidate in RoomEngine.scene_rooms(self.scene):
            if getattr(candidate, "room_id", None) == self.room_id:
                self.room = candidate
                self.is_applied = True
                return False

        result = RoomEngine.add_to_scene(self.scene, self.room)
        if result:
            self.room = result
            self.is_applied = True
            return True
        return False
