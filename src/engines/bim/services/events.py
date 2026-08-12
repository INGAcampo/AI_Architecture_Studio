"""Eventos públicos emitidos por el servicio BIM de AIAS."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class BimEventName(str, Enum):
    DOCUMENT_CHANGED = "bim.document.changed"
    ELEMENT_REGISTERED = "bim.element.registered"
    ELEMENT_UPDATED = "bim.element.updated"
    ELEMENT_REMOVED = "bim.element.removed"
    PARAMETER_CHANGED = "bim.parameter.changed"
    RELATIONSHIP_CREATED = "bim.relationship.created"
    DOCUMENT_SAVED = "bim.document.saved"
    DOCUMENT_LOADED = "bim.document.loaded"


@dataclass(frozen=True)
class BimEvent:
    name: BimEventName
    document_id: str
    element_id: str | None = None
    payload: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name.value,
            "document_id": self.document_id,
            "element_id": self.element_id,
            "payload": dict(self.payload or {}),
        }
