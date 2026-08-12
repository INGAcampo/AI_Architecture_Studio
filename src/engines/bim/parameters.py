"""Parámetros BIM tipados y serializables."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from copy import deepcopy
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BimParameter:
    name: str
    value: Any
    unit: str | None = None
    group: str = "General"
    read_only: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": deepcopy(self.value),
            "unit": self.unit,
            "group": self.group,
            "read_only": self.read_only,
        }


class BimParameterSet(Mapping[str, Any]):
    """Colección de parámetros con API simple y estable."""

    def __init__(self, initial: Mapping[str, Any] | None = None):
        self._parameters: dict[str, BimParameter] = {}
        for name, value in dict(initial or {}).items():
            self.set(name, value)

    def __getitem__(self, name: str) -> Any:
        return self._parameters[name].value

    def __iter__(self) -> Iterator[str]:
        return iter(self._parameters)

    def __len__(self) -> int:
        return len(self._parameters)

    def set(
        self,
        name: str,
        value: Any,
        *,
        unit: str | None = None,
        group: str = "General",
        read_only: bool = False,
    ) -> None:
        key = str(name).strip()
        if not key:
            raise ValueError("El nombre del parámetro no puede estar vacío.")

        current = self._parameters.get(key)
        if current is not None and current.read_only:
            raise ValueError(f"El parámetro {key!r} es de solo lectura.")

        self._parameters[key] = BimParameter(
            name=key,
            value=deepcopy(value),
            unit=unit,
            group=str(group or "General"),
            read_only=bool(read_only),
        )

    def get_definition(self, name: str) -> BimParameter | None:
        return self._parameters.get(name)

    def remove(self, name: str) -> None:
        current = self._parameters.get(name)
        if current is not None and current.read_only:
            raise ValueError(f"El parámetro {name!r} es de solo lectura.")
        self._parameters.pop(name, None)

    def to_dict(self) -> dict[str, Any]:
        return {
            name: parameter.to_dict()
            for name, parameter in self._parameters.items()
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BimParameterSet":
        result = cls()
        for name, raw in data.items():
            if isinstance(raw, Mapping) and "value" in raw:
                result.set(
                    name,
                    raw.get("value"),
                    unit=raw.get("unit"),
                    group=raw.get("group", "General"),
                    read_only=bool(raw.get("read_only", False)),
                )
            else:
                result.set(name, raw)
        return result
