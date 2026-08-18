"""Administración centralizada de parámetros BIM."""

from __future__ import annotations

from typing import Any

from ..document import BimDocument


class BimParameterManager:
    def __init__(self, document: BimDocument) -> None:
        self.document = document

    def set(
        self,
        element_id: str,
        name: str,
        value: Any,
        *,
        unit: str | None = None,
        group: str = "General",
    ) -> Any:
        element = self.document.require_element(element_id)
        previous = element.parameters.get(name)
        element.parameters.set(
            name,
            value,
            unit=unit,
            group=group,
        )
        return previous

    def get(self, element_id: str, name: str, default: Any = None) -> Any:
        element = self.document.require_element(element_id)
        return element.parameters.get(name, default)

    def remove(self, element_id: str, name: str) -> Any:
        element = self.document.require_element(element_id)
        previous = element.parameters.get(name)
        element.parameters.remove(name)
        return previous
