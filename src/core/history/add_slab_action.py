"""Undo / Redo idempotente para SLAB."""

from engines.architectural.slab_engine import SlabEngine


class AddSlabAction:

    def __init__(self, scene, slab):
        self.scene = scene
        self.slab = slab
        self.slab_id = getattr(slab, "slab_id", None)
        self.is_applied = slab in SlabEngine.scene_slabs(scene)

    def undo(self):
        if not self.is_applied:
            return False
        removed = SlabEngine.remove_from_scene(self.scene, self.slab)
        if removed:
            self.is_applied = False
        return removed

    def redo(self):
        if self.is_applied:
            return False

        for candidate in SlabEngine.scene_slabs(self.scene):
            if getattr(candidate, "slab_id", None) == self.slab_id:
                self.slab = candidate
                self.is_applied = True
                return False

        result = SlabEngine.add_to_scene(self.scene, self.slab)
        if result:
            self.slab = result
            self.is_applied = True
            return True
        return False
