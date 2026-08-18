from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Iterable, Mapping
from uuid import UUID, uuid4


class ObjectType(str, Enum):
    GENERIC = "generic"
    SITE = "site"
    BUILDING = "building"
    LEVEL = "level"
    SPACE = "space"
    WALL = "wall"
    DOOR = "door"
    WINDOW = "window"
    SLAB = "slab"
    ROOF = "roof"
    BEAM = "beam"
    COLUMN = "column"
    STAIR = "stair"


class ObjectState(str, Enum):
    ACTIVE = "active"
    HIDDEN = "hidden"
    LOCKED = "locked"
    ARCHIVED = "archived"
    DELETED = "deleted"


class RelationshipType(str, Enum):
    CONTAINS = "contains"
    HOSTS = "hosts"
    CONNECTS = "connects"
    REFERENCES = "references"
    GROUPS = "groups"


@dataclass(frozen=True, order=True)
class ObjectId:
    value: UUID = field(default_factory=uuid4)

    @classmethod
    def new(cls) -> "ObjectId":
        return cls(uuid4())

    @classmethod
    def parse(cls, value: "ObjectId | UUID | str") -> "ObjectId":
        if isinstance(value, cls):
            return value
        if isinstance(value, UUID):
            return cls(value)
        return cls(UUID(str(value)))

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class MaterialRef:
    material_id: str
    name: str
    role: str = "default"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.material_id.strip():
            raise ValueError("material_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True)
class Relationship:
    source: ObjectId
    target: ObjectId
    relation_type: RelationshipType
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.source == self.target:
            raise ValueError("Una relación no puede apuntar al mismo objeto")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


class PropertyContainer:
    def __init__(self, initial: Mapping[str, Any] | None = None) -> None:
        self._values: dict[str, Any] = {}
        for key, value in (initial or {}).items():
            self.set(key, value)

    def set(self, name: str, value: Any) -> bool:
        key = str(name).strip()
        if not key:
            raise ValueError("El nombre de la propiedad no puede estar vacío")
        if key in self._values and self._values[key] == value:
            return False
        self._values[key] = value
        return True

    def get(self, name: str, default: Any = None) -> Any:
        return self._values.get(name, default)

    def remove(self, name: str) -> Any:
        return self._values.pop(name)

    def contains(self, name: str) -> bool:
        return name in self._values

    def snapshot(self) -> Mapping[str, Any]:
        return MappingProxyType(dict(self._values))

    def __len__(self) -> int:
        return len(self._values)


class MaterialContainer:
    def __init__(self, materials: Iterable[MaterialRef] | None = None) -> None:
        self._materials: dict[str, MaterialRef] = {}
        for material in materials or ():
            self.add(material)

    def add(self, material: MaterialRef) -> bool:
        previous = self._materials.get(material.role)
        if previous == material:
            return False
        self._materials[material.role] = material
        return True

    def get(self, role: str = "default") -> MaterialRef | None:
        return self._materials.get(role)

    def remove(self, role: str = "default") -> MaterialRef:
        return self._materials.pop(role)

    def snapshot(self) -> tuple[MaterialRef, ...]:
        return tuple(self._materials[key] for key in sorted(self._materials))

    def __len__(self) -> int:
        return len(self._materials)


class RelationshipManager:
    def __init__(self) -> None:
        self._relationships: list[Relationship] = []

    def add(self, relationship: Relationship) -> bool:
        if relationship in self._relationships:
            return False
        self._relationships.append(relationship)
        return True

    def remove(self, relationship: Relationship) -> bool:
        if relationship not in self._relationships:
            return False
        self._relationships.remove(relationship)
        return True

    def outgoing(self, source: ObjectId, relation_type: RelationshipType | None = None) -> tuple[Relationship, ...]:
        items = [
            rel for rel in self._relationships
            if rel.source == source and (relation_type is None or rel.relation_type == relation_type)
        ]
        return tuple(sorted(items, key=lambda rel: (rel.relation_type.value, str(rel.target))))

    def incoming(self, target: ObjectId, relation_type: RelationshipType | None = None) -> tuple[Relationship, ...]:
        items = [
            rel for rel in self._relationships
            if rel.target == target and (relation_type is None or rel.relation_type == relation_type)
        ]
        return tuple(sorted(items, key=lambda rel: (rel.relation_type.value, str(rel.source))))

    def remove_object(self, object_id: ObjectId) -> int:
        doomed = [rel for rel in self._relationships if object_id in (rel.source, rel.target)]
        self._relationships = [rel for rel in self._relationships if rel not in doomed]
        return len(doomed)

    def __len__(self) -> int:
        return len(self._relationships)


class BimObject:
    def __init__(
        self,
        name: str,
        object_type: ObjectType = ObjectType.GENERIC,
        *,
        object_id: ObjectId | UUID | str | None = None,
        metadata: Mapping[str, Any] | None = None,
        properties: Mapping[str, Any] | None = None,
        materials: Iterable[MaterialRef] | None = None,
    ) -> None:
        clean_name = str(name).strip()
        if not clean_name:
            raise ValueError("name no puede estar vacío")
        self._id = ObjectId.new() if object_id is None else ObjectId.parse(object_id)
        self.name = clean_name
        self.object_type = ObjectType(object_type)
        self.state = ObjectState.ACTIVE
        self.revision = 0
        self.metadata: dict[str, Any] = dict(metadata or {})
        self.properties = PropertyContainer(properties)
        self.materials = MaterialContainer(materials)

    @property
    def id(self) -> ObjectId:
        return self._id

    def rename(self, name: str) -> bool:
        clean_name = str(name).strip()
        if not clean_name:
            raise ValueError("name no puede estar vacío")
        if clean_name == self.name:
            return False
        self.name = clean_name
        self._touch()
        return True

    def set_state(self, state: ObjectState) -> bool:
        new_state = ObjectState(state)
        if new_state == self.state:
            return False
        if self.state == ObjectState.DELETED and new_state != ObjectState.DELETED:
            raise ValueError("Un objeto eliminado no puede reactivarse")
        self.state = new_state
        self._touch()
        return True

    def set_property(self, name: str, value: Any) -> bool:
        changed = self.properties.set(name, value)
        if changed:
            self._touch()
        return changed

    def add_material(self, material: MaterialRef) -> bool:
        changed = self.materials.add(material)
        if changed:
            self._touch()
        return changed

    def update_metadata(self, **values: Any) -> bool:
        changed = False
        for key, value in values.items():
            if self.metadata.get(key) != value:
                self.metadata[key] = value
                changed = True
        if changed:
            self._touch()
        return changed

    def snapshot(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "id": str(self.id),
            "name": self.name,
            "object_type": self.object_type.value,
            "state": self.state.value,
            "revision": self.revision,
            "metadata": MappingProxyType(dict(self.metadata)),
            "properties": self.properties.snapshot(),
            "materials": self.materials.snapshot(),
        })

    def _touch(self) -> None:
        self.revision += 1
