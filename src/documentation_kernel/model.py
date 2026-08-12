from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

class AnnotationKind(str, Enum):
    TEXT = "text"
    DIMENSION = "dimension"
    TAG = "tag"
    SYMBOL = "symbol"

@dataclass(frozen=True, slots=True)
class Annotation:
    annotation_id: str
    kind: AnnotationKind
    text: str
    x: float
    y: float
    style_id: str = "default"

    def __post_init__(self):
        if not self.annotation_id.strip():
            raise ValueError("annotation_id es obligatorio")

@dataclass(frozen=True, slots=True)
class DocumentationView:
    view_id: str
    name: str
    scale: float
    model_revision: int = 0
    annotations: tuple[Annotation, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.view_id.strip() or not self.name.strip():
            raise ValueError("view_id y name son obligatorios")
        if self.scale <= 0:
            raise ValueError("scale debe ser positiva")

@dataclass(frozen=True, slots=True)
class Viewport:
    viewport_id: str
    view_id: str
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self):
        if min(self.width, self.height) <= 0:
            raise ValueError("Viewport inválido")

@dataclass(frozen=True, slots=True)
class Sheet:
    sheet_id: str
    number: str
    title: str
    width: float
    height: float
    viewports: tuple[Viewport, ...] = ()

    def __post_init__(self):
        if not self.sheet_id.strip() or not self.number.strip():
            raise ValueError("sheet_id y number son obligatorios")
        if min(self.width, self.height) <= 0:
            raise ValueError("Tamaño de hoja inválido")
