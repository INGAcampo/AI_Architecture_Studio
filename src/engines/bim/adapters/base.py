"""Contrato común para adaptadores BIM."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..categories import BimCategory
from ..element import BimElement
from ..parameters import BimParameterSet


class BimAdapter(ABC):
    category = BimCategory.GENERIC
    source_types: tuple[type, ...] = ()

    def supports(self, source: Any) -> bool:
        return bool(self.source_types) and isinstance(source, self.source_types)

    @abstractmethod
    def to_bim_element(
        self,
        source: Any,
        *,
        level_id: str | None = None,
    ) -> BimElement:
        raise NotImplementedError

    def element_id(self, source: Any) -> str | None:
        for attribute in (
            "door_id",
            "window_id",
            "room_id",
            "slab_id",
            "beam_id",
            "column_id",
            "foundation_id",
            "id",
        ):
            value = getattr(source, attribute, None)
            if value:
                return str(value)
        return None

    def source_name(self, source: Any) -> str:
        return str(
            getattr(
                source,
                "name",
                source.__class__.__name__,
            )
        )

    def source_properties(self, source: Any) -> BimParameterSet:
        raw = getattr(source, "properties", {}) or {}
        return BimParameterSet(raw)

    def add_parameter(
        self,
        parameters: BimParameterSet,
        name: str,
        value: Any,
        *,
        unit: str | None = None,
        group: str = "General",
    ) -> None:
        if value is not None:
            parameters.set(name, value, unit=unit, group=group)

    def build_element(
        self,
        source: Any,
        *,
        level_id: str | None = None,
        parameters: BimParameterSet | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> BimElement:
        return BimElement(
            name=self.source_name(source),
            category=self.category,
            element_id=self.element_id(source) or "",
            type_name=source.__class__.__name__,
            level_id=level_id,
            geometry_ref=getattr(source, "geometry", None),
            source_object_id=self.element_id(source),
            parameters=parameters or self.source_properties(source),
            metadata={
                "aias_module": source.__class__.__module__,
                "aias_class": source.__class__.__name__,
                "adapter": self.__class__.__name__,
                **dict(metadata or {}),
            },
        )
