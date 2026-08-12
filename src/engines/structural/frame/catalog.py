from __future__ import annotations

from .model import StructuralMaterial, StructuralProfile


class StructuralMaterialCatalog:
    def __init__(self) -> None:
        self._items: dict[str, StructuralMaterial] = {}
        self.revision = 0

    def register(self, item: StructuralMaterial, *, replace: bool = False) -> None:
        if item.material_id in self._items and not replace:
            raise KeyError(f"Material ya registrado: {item.material_id}")
        self._items[item.material_id] = item
        self.revision += 1

    def get(self, material_id: str) -> StructuralMaterial:
        try:
            return self._items[material_id]
        except KeyError as exc:
            raise KeyError(f"Material desconocido: {material_id}") from exc

    def remove(self, material_id: str) -> StructuralMaterial:
        item = self.get(material_id)
        self._items.pop(material_id)
        self.revision += 1
        return item


class StructuralProfileCatalog:
    def __init__(self) -> None:
        self._items: dict[str, StructuralProfile] = {}
        self.revision = 0

    def register(self, item: StructuralProfile, *, replace: bool = False) -> None:
        if item.profile_id in self._items and not replace:
            raise KeyError(f"Perfil ya registrado: {item.profile_id}")
        self._items[item.profile_id] = item
        self.revision += 1

    def get(self, profile_id: str) -> StructuralProfile:
        try:
            return self._items[profile_id]
        except KeyError as exc:
            raise KeyError(f"Perfil desconocido: {profile_id}") from exc

    def remove(self, profile_id: str) -> StructuralProfile:
        item = self.get(profile_id)
        self._items.pop(profile_id)
        self.revision += 1
        return item
