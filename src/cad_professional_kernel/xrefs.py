from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class ExternalReference:
    name: str
    path: Path
    loaded: bool = True

class XrefManager:
    def __init__(self) -> None:
        self._refs: dict[str, ExternalReference] = {}

    def attach(self, ref: ExternalReference) -> None:
        self._refs[ref.name] = ref

    def detach(self, name: str) -> ExternalReference:
        return self._refs.pop(name)

    def all(self) -> tuple[ExternalReference, ...]:
        return tuple(self._refs.values())
