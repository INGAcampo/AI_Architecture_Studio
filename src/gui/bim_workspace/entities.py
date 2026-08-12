from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from aias_i18n import tr


class BimWorkspaceNodeKind(str, Enum):
    ROOT = "root"
    GROUP = "group"
    LEVEL = "level"
    CATEGORY = "category"
    FAMILY = "family"
    TYPE = "type"
    INSTANCE = "instance"
    MATERIAL = "material"
    PHASE = "phase"


@dataclass(slots=True)
class BimWorkspaceNode:
    node_id: str
    title: str
    kind: BimWorkspaceNodeKind
    parent_id: str | None = None
    object_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError(tr("error.empty_node_id"))
        if not self.title.strip():
            raise ValueError(tr("error.empty_title"))

    def snapshot(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "title": self.title,
            "kind": self.kind.value,
            "parent_id": self.parent_id,
            "object_id": self.object_id,
            "metadata": dict(self.metadata),
            "children": list(self.children),
        }


@dataclass(frozen=True, slots=True)
class MaterialDefinition:
    material_id: str
    name: str
    category: str = "General"
    density: float | None = None
    thermal_conductivity: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.material_id.strip():
            raise ValueError(tr("error.empty_material_id"))
        if not self.name.strip():
            raise ValueError(tr("error.empty_name"))
        if self.density is not None and self.density < 0:
            raise ValueError(tr("error.negative_density"))


@dataclass(frozen=True, slots=True)
class FamilyTypeDefinition:
    type_id: str
    name: str
    family_id: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.type_id.strip():
            raise ValueError(tr("error.empty_type_id"))
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if not self.family_id.strip():
            raise ValueError(tr("error.empty_family_id"))


@dataclass(frozen=True, slots=True)
class FamilyDefinition:
    family_id: str
    name: str
    category: str
    types: tuple[FamilyTypeDefinition, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.family_id.strip():
            raise ValueError(tr("error.empty_family_id"))
        if not self.name.strip():
            raise ValueError(tr("error.empty_name"))
        if not self.category.strip():
            raise ValueError(tr("error.empty_category"))
        for family_type in self.types:
            if family_type.family_id != self.family_id:
                raise ValueError(tr("error.family_type_mismatch"))
