"""Reglas para enlazar parámetros compartidos con elementos BIM."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .shared_parameter import ParameterScope


@dataclass(frozen=True)
class ParameterBinding:
    parameter_guid: str
    scope: ParameterScope | str = ParameterScope.INSTANCE
    categories: tuple[str, ...] = field(default_factory=tuple)
    families: tuple[str, ...] = field(default_factory=tuple)
    target_ids: tuple[str, ...] = field(default_factory=tuple)
    required: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "scope", ParameterScope(self.scope))
        object.__setattr__(
            self,
            "categories",
            self._normalize_many(self.categories),
        )
        object.__setattr__(
            self,
            "families",
            self._normalize_many(self.families),
        )
        object.__setattr__(
            self,
            "target_ids",
            self._normalize_many(self.target_ids),
        )

    def applies_to(
        self,
        *,
        owner_id: str | None = None,
        category: str | None = None,
        family: str | None = None,
    ) -> bool:
        if self.scope is ParameterScope.PROJECT:
            return True
        if self.scope is ParameterScope.CATEGORY:
            return self._contains(self.categories, category)
        if self.scope is ParameterScope.FAMILY:
            return self._contains(self.families, family)
        if self.scope is ParameterScope.SELECTION:
            return self._contains(self.target_ids, owner_id)

        category_ok = not self.categories or self._contains(
            self.categories,
            category,
        )
        family_ok = not self.families or self._contains(
            self.families,
            family,
        )
        target_ok = not self.target_ids or self._contains(
            self.target_ids,
            owner_id,
        )
        return category_ok and family_ok and target_ok

    def to_dict(self) -> dict[str, Any]:
        return {
            "parameter_guid": self.parameter_guid,
            "scope": self.scope.value,
            "categories": list(self.categories),
            "families": list(self.families),
            "target_ids": list(self.target_ids),
            "required": self.required,
        }

    @staticmethod
    def _normalize_many(values) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    str(value).strip()
                    for value in values
                    if str(value).strip()
                }
            )
        )

    @staticmethod
    def _contains(values: tuple[str, ...], candidate: str | None) -> bool:
        if candidate is None:
            return False
        normalized = str(candidate).strip().casefold()
        return any(value.casefold() == normalized for value in values)
