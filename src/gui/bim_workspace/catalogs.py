from __future__ import annotations

from collections import defaultdict
from dataclasses import replace
from typing import Iterable

from .entities import FamilyDefinition, FamilyTypeDefinition, MaterialDefinition
from aias_i18n import tr


class MaterialCatalog:
    def __init__(self) -> None:
        self._materials: dict[str, MaterialDefinition] = {}
        self.revision = 0

    def register(self, material: MaterialDefinition, *, replace_existing: bool = False) -> None:
        if material.material_id in self._materials and not replace_existing:
            raise KeyError(tr("error.material_duplicate",material_id=material.material_id))
        self._materials[material.material_id] = material
        self.revision += 1

    def get(self, material_id: str) -> MaterialDefinition:
        try:
            return self._materials[material_id]
        except KeyError as exc:
            raise KeyError(tr("error.material_unknown",material_id=material_id)) from exc

    def remove(self, material_id: str) -> MaterialDefinition:
        material = self.get(material_id)
        self._materials.pop(material_id)
        self.revision += 1
        return material

    def all(self) -> tuple[MaterialDefinition, ...]:
        return tuple(self._materials[key] for key in sorted(self._materials))

    def by_category(self) -> dict[str, tuple[MaterialDefinition, ...]]:
        grouped: dict[str, list[MaterialDefinition]] = defaultdict(list)
        for material in self.all():
            grouped[material.category].append(material)
        return {key: tuple(value) for key, value in sorted(grouped.items())}

    def search(self, query: str) -> tuple[MaterialDefinition, ...]:
        text = query.strip().casefold()
        if not text:
            return self.all()
        return tuple(
            material for material in self.all()
            if text in material.name.casefold()
            or text in material.category.casefold()
            or text in material.material_id.casefold()
        )


class FamilyCatalog:
    def __init__(self) -> None:
        self._families: dict[str, FamilyDefinition] = {}
        self.revision = 0

    def register(self, family: FamilyDefinition, *, replace_existing: bool = False) -> None:
        if family.family_id in self._families and not replace_existing:
            raise KeyError(tr("error.family_duplicate",family_id=family.family_id))
        self._families[family.family_id] = family
        self.revision += 1

    def get(self, family_id: str) -> FamilyDefinition:
        try:
            return self._families[family_id]
        except KeyError as exc:
            raise KeyError(tr("error.family_unknown",family_id=family_id)) from exc

    def remove(self, family_id: str) -> FamilyDefinition:
        family = self.get(family_id)
        self._families.pop(family_id)
        self.revision += 1
        return family

    def add_type(self, family_id: str, family_type: FamilyTypeDefinition) -> FamilyDefinition:
        family = self.get(family_id)
        if family_type.family_id != family_id:
            raise ValueError(tr("error.type_not_in_family"))
        if any(item.type_id == family_type.type_id for item in family.types):
            raise KeyError(tr("error.type_duplicate",type_id=family_type.type_id))
        updated = replace(family, types=family.types + (family_type,))
        self._families[family_id] = updated
        self.revision += 1
        return updated

    def all(self) -> tuple[FamilyDefinition, ...]:
        return tuple(self._families[key] for key in sorted(self._families))

    def by_category(self) -> dict[str, tuple[FamilyDefinition, ...]]:
        grouped: dict[str, list[FamilyDefinition]] = defaultdict(list)
        for family in self.all():
            grouped[family.category].append(family)
        return {key: tuple(value) for key, value in sorted(grouped.items())}

    def search(self, query: str) -> tuple[FamilyDefinition, ...]:
        text = query.strip().casefold()
        if not text:
            return self.all()
        return tuple(
            family for family in self.all()
            if text in family.name.casefold()
            or text in family.category.casefold()
            or text in family.family_id.casefold()
            or any(text in family_type.name.casefold() for family_type in family.types)
        )
