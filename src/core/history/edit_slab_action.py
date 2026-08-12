"""Undo / Redo para edición completa de parámetros SLAB."""


class EditSlabAction:
    def __init__(self, slab, before, after):
        self.slab = slab
        self.before = dict(before)
        self.after = dict(after)

    def undo(self):
        self.slab.apply_data_snapshot(self.before)
        return True

    def redo(self):
        self.slab.apply_data_snapshot(self.after)
        return True
