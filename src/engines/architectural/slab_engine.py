"""Motor BIM para losas asociadas a ROOM."""

from models.architectural.slab import Slab


class SlabEngine:

    @staticmethod
    def scene_slabs(scene):
        if scene is None:
            return []
        getter = getattr(scene, "get_elements", None)
        elements = getter() if callable(getter) else []
        return [
            element
            for element in elements
            if element.__class__.__name__ == "Slab"
        ]

    @classmethod
    def find_by_room(cls, scene, room):
        room_id = getattr(room, "room_id", None)
        for slab in cls.scene_slabs(scene):
            if getattr(slab, "host_room_id", None) == room_id:
                return slab
        return None

    @classmethod
    def create_from_room(
        cls,
        room,
        thickness=0.15,
        material="Concreto armado",
        elevation=0.0,
    ):
        if room is None or not getattr(room, "valid", False):
            return None
        return Slab(
            host_room=room,
            thickness=thickness,
            material=material,
            elevation=elevation,
        )

    @classmethod
    def add_to_scene(cls, scene, slab):
        if scene is None or slab is None:
            return False

        existing = cls.find_by_room(scene, slab.host_room)
        if existing is not None:
            return existing

        adder = getattr(scene, "add_element", None)
        if callable(adder):
            adder(slab)
            return slab
        return False

    @classmethod
    def remove_from_scene(cls, scene, slab):
        if scene is None or slab is None:
            return False

        remover = getattr(scene, "remove_element", None)
        if callable(remover):
            remover(slab)
            return True

        elements = getattr(scene, "elements", None)
        if isinstance(elements, list) and slab in elements:
            elements.remove(slab)
            return True
        return False

    @classmethod
    def update_scene_slabs(cls, scene):
        slabs = cls.scene_slabs(scene)
        for slab in slabs:
            room = getattr(slab, "host_room", None)
            if room is None or not getattr(room, "valid", False):
                slab.invalidate()
                continue

            slab.host_room_id = getattr(room, "room_id", None)
            slab.name = f"Losa - {getattr(room, 'name', 'Ambiente')}"
            slab.update_geometry(getattr(room, "boundary", []))
        return slabs

    @classmethod
    def totals(cls, scene):
        slabs = [
            slab
            for slab in cls.scene_slabs(scene)
            if getattr(slab, "valid", False)
        ]
        return {
            "count": len(slabs),
            "area": sum(slab.area for slab in slabs),
            "volume": sum(slab.volume for slab in slabs),
        }
