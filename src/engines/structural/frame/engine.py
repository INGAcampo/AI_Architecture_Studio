from __future__ import annotations

from typing import Any

from .catalog import StructuralMaterialCatalog, StructuralProfileCatalog
from .model import StructuralMember
from .quantities import StructuralQuantityCalculator
from .validation import StructuralMemberValidator


class IntelligentStructuralFrameEngine:
    def __init__(self, *, event_dispatcher=None) -> None:
        self.materials = StructuralMaterialCatalog()
        self.profiles = StructuralProfileCatalog()
        self.validator = StructuralMemberValidator()
        self.quantities = StructuralQuantityCalculator()
        self.event_dispatcher = event_dispatcher
        self._members: dict[str, StructuralMember] = {}

    def register_material(self, material) -> None:
        self.materials.register(material)
        self._publish("structural.material.registered", material_id=material.material_id)

    def register_profile(self, profile) -> None:
        self.profiles.register(profile)
        self._publish("structural.profile.registered", profile_id=profile.profile_id)

    def add_member(self, member: StructuralMember) -> StructuralMember:
        if member.member_id in self._members:
            raise KeyError(f"Elemento ya existente: {member.member_id}")
        self.materials.get(member.material_id)
        self.profiles.get(member.profile_id)
        result = self.validator.validate(member)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._members[member.member_id] = member
        self._publish("structural.member.added", member_id=member.member_id)
        return member

    def get_member(self, member_id: str) -> StructuralMember:
        try:
            return self._members[member_id]
        except KeyError as exc:
            raise KeyError(f"Elemento desconocido: {member_id}") from exc

    def remove_member(self, member_id: str) -> StructuralMember:
        member = self.get_member(member_id)
        self._members.pop(member_id)
        self._publish("structural.member.removed", member_id=member_id)
        return member

    def change_profile(self, member_id: str, profile_id: str) -> StructuralMember:
        self.profiles.get(profile_id)
        member = self.get_member(member_id)
        if member.profile_id != profile_id:
            member.profile_id = profile_id
            member.touch()
            self._publish("structural.member.profile.changed", member_id=member_id, profile_id=profile_id)
        return member

    def change_material(self, member_id: str, material_id: str) -> StructuralMember:
        self.materials.get(material_id)
        member = self.get_member(member_id)
        if member.material_id != material_id:
            member.material_id = material_id
            member.touch()
            self._publish("structural.member.material.changed", member_id=member_id, material_id=material_id)
        return member

    def set_rotation(self, member_id: str, rotation_degrees: float) -> StructuralMember:
        member = self.get_member(member_id)
        member.rotation_degrees = float(rotation_degrees)
        member.touch()
        return member

    def calculate_quantities(self, member_id: str):
        member = self.get_member(member_id)
        return self.quantities.calculate(
            member,
            self.profiles.get(member.profile_id),
            self.materials.get(member.material_id),
        )

    def _publish(self, name: str, **payload: Any) -> None:
        target = self.event_dispatcher
        if target is None:
            return
        if callable(target):
            target(name, payload)
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
