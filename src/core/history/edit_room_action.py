"""Undo / Redo para metadatos BIM de ROOM."""


class EditRoomAction:
    def __init__(self, room, before, after):
        self.room = room
        self.before = dict(before)
        self.after = dict(after)

    def undo(self):
        self.room.apply_data_snapshot(self.before)
        return True

    def redo(self):
        self.room.apply_data_snapshot(self.after)
        return True
