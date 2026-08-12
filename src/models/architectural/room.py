"""AI Architecture Studio
Architectural Core 5.0.7.4 — ROOM Data & Properties.
"""

from uuid import uuid4

from engines.geometry.point import Point
from models.base_object import BaseObject


class Room(BaseObject):
    GENERIC = "generic"
    LIVING = "living"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    SERVICE = "service"
    CIRCULATION = "circulation"
    EXTERIOR = "exterior"

    CATEGORY_LABELS = {
        GENERIC: "General",
        LIVING: "Sala / Estar",
        BEDROOM: "Dormitorio",
        KITCHEN: "Cocina",
        BATHROOM: "Baño",
        SERVICE: "Servicio",
        CIRCULATION: "Circulación",
        EXTERIOR: "Exterior",
    }

    def __init__(
        self,
        boundary=None,
        name="Ambiente",
        seed_point=None,
        room_id=None,
        category=GENERIC,
        number="",
        comments="",
    ):
        super().__init__(name=str(name), object_type="Room")

        # BaseObject administra self.id.
        self.room_id = str(room_id or uuid4())
        self.boundary = [
            Point(point.x, point.y, getattr(point, "z", 0.0))
            for point in (boundary or [])
        ]
        self.seed_point = (
            Point(
                seed_point.x,
                seed_point.y,
                getattr(seed_point, "z", 0.0),
            )
            if seed_point is not None
            else None
        )

        self.category = self.normalize_category(category)
        self.number = str(number or "")
        self.comments = str(comments or "")
        self.visible = True
        self.valid = bool(self.boundary)
        self.area = 0.0
        self.perimeter = 0.0
        self.boundary_key = None
        self.update_geometry(self.boundary)

    @classmethod
    def normalize_category(cls, value):
        key = str(value or "").strip().lower()
        aliases = {
            "general": cls.GENERIC,
            "generico": cls.GENERIC,
            "genérico": cls.GENERIC,
            "sala": cls.LIVING,
            "estar": cls.LIVING,
            "living": cls.LIVING,
            "dormitorio": cls.BEDROOM,
            "habitacion": cls.BEDROOM,
            "habitación": cls.BEDROOM,
            "bedroom": cls.BEDROOM,
            "cocina": cls.KITCHEN,
            "kitchen": cls.KITCHEN,
            "baño": cls.BATHROOM,
            "bano": cls.BATHROOM,
            "bathroom": cls.BATHROOM,
            "servicio": cls.SERVICE,
            "service": cls.SERVICE,
            "circulacion": cls.CIRCULATION,
            "circulación": cls.CIRCULATION,
            "pasillo": cls.CIRCULATION,
            "circulation": cls.CIRCULATION,
            "exterior": cls.EXTERIOR,
        }
        key = aliases.get(key, key)
        return key if key in cls.CATEGORY_LABELS else cls.GENERIC

    @property
    def category_label(self):
        return self.CATEGORY_LABELS.get(
            self.category,
            self.CATEGORY_LABELS[self.GENERIC],
        )

    @property
    def label_position(self):
        if self.seed_point is not None:
            return self.seed_point
        if not self.boundary:
            return Point(0.0, 0.0, 0.0)
        count = len(self.boundary)
        return Point(
            sum(point.x for point in self.boundary) / count,
            sum(point.y for point in self.boundary) / count,
            0.0,
        )

    def set_name(self, value):
        value = str(value or "").strip()
        if value:
            self.name = value
        self._update_properties()

    def set_category(self, value):
        self.category = self.normalize_category(value)
        self._update_properties()

    def set_number(self, value):
        self.number = str(value or "").strip()
        self._update_properties()

    def set_comments(self, value):
        self.comments = str(value or "").strip()
        self._update_properties()

    def update_geometry(self, boundary, boundary_key=None):
        from engines.architectural.room_engine import RoomEngine

        self.boundary = [
            Point(point.x, point.y, getattr(point, "z", 0.0))
            for point in (boundary or [])
        ]
        self.valid = len(self.boundary) >= 3
        self.area = RoomEngine.compute_area(self.boundary)
        self.perimeter = RoomEngine.compute_perimeter(self.boundary)
        self.boundary_key = (
            boundary_key
            if boundary_key is not None
            else RoomEngine.boundary_key(self.boundary)
        )
        self._update_properties()
        return self

    def invalidate(self):
        self.valid = False
        self._update_properties()

    def clone(self):
        return Room(
            boundary=self.boundary,
            name=self.name,
            seed_point=self.seed_point,
            category=self.category,
            number=self.number,
            comments=self.comments,
        )

    def data_snapshot(self):
        return {
            "name": self.name,
            "category": self.category,
            "number": self.number,
            "comments": self.comments,
        }

    def apply_data_snapshot(self, data):
        self.name = str(data.get("name", self.name))
        self.category = self.normalize_category(
            data.get("category", self.category)
        )
        self.number = str(data.get("number", self.number))
        self.comments = str(data.get("comments", self.comments))
        self._update_properties()

    def _update_properties(self):
        values = {
            "Nombre": self.name,
            "Número": self.number or "-",
            "Categoría": self.category_label,
            "Área útil": round(self.area, 3),
            "Perímetro": round(self.perimeter, 3),
            "Válido": "Sí" if self.valid else "No",
            "Vértices": len(self.boundary),
            "Comentarios": self.comments or "-",
            "ROOM Core": "5.0.7.4",
        }
        self.properties.clear()
        for key, value in values.items():
            setter = getattr(self, "set_property", None)
            if callable(setter):
                setter(key, value)
            else:
                self.properties[key] = value

    def info(self):
        data = super().info()
        data.update(
            {
                "Número": self.number or "-",
                "Categoría": self.category_label,
                "Área útil": round(self.area, 3),
                "Perímetro": round(self.perimeter, 3),
                "Válido": "Sí" if self.valid else "No",
                "Comentarios": self.comments or "-",
                "ROOM Core": "5.0.7.4",
            }
        )
        return data
