"""Exact native Level/Grid bridge for AIAS L3 Production BIM 001F."""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from inspect import Parameter, signature
from typing import Any

from engines.architectural.level_manager import LevelManager
from engines.architectural.grid_manager import GridManager
from engines.bim.adapters.native import LevelBimAdapter, GridBimAdapter


class NativeLevelGridContractError(RuntimeError):
    """Raised when a declared native Level/Grid contract cannot be satisfied."""


@dataclass(slots=True)
class NativeMirrorResult:
    """Record one successful canonical-to-native mirror."""

    canonical_id: str
    native_source: Any
    bim_element: Any


_LEVEL_CANDIDATES = (
    ("models.architectural.level", "Level"),
    ("aias_bim_professional_foundation.core", "Level"),
)

_GRID_CANDIDATES = (
    ("models.architectural.grid", "Grid"),
)

_LEVEL_ALIASES = {
    "id": "id",
    "level_id": "id",
    "uid": "id",
    "name": "name",
    "label": "name",
    "elevation": "elevation",
    "elevation_m": "elevation",
    "z": "elevation",
    "properties": "properties",
    "metadata": "properties",
}

_GRID_ALIASES = {
    "id": "id",
    "grid_id": "id",
    "uid": "id",
    "name": "name",
    "label": "name",
    "start": "start",
    "end": "end",
    "start_point": "start",
    "end_point": "end",
    "p1": "start",
    "p2": "end",
    "properties": "properties",
    "metadata": "properties",
}


def _resolve_model(candidates: tuple[tuple[str, str], ...], adapter: Any, sample: dict[str, Any], aliases: dict[str, str]):
    errors: list[str] = []
    for module_name, symbol in candidates:
        try:
            cls = getattr(import_module(module_name), symbol)
        except Exception as exc:
            errors.append(f"{module_name}.{symbol}: import {type(exc).__name__}: {exc}")
            continue
        try:
            obj = _construct_exact(cls, sample, aliases)
            if not adapter.supports(obj):
                errors.append(f"{module_name}.{symbol}: adapter.supports=False")
                continue
            adapter.to_bim_element(obj)
            return cls
        except Exception as exc:
            errors.append(f"{module_name}.{symbol}: {type(exc).__name__}: {exc}")
    raise NativeLevelGridContractError("; ".join(errors) or "no_native_model_candidate")


def _construct_exact(cls: type, values: dict[str, Any], aliases: dict[str, str]):
    """Construct a native model using only explicit, audited parameter aliases."""
    sig = signature(cls)
    kwargs: dict[str, Any] = {}
    missing: list[str] = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            continue

        source_name = aliases.get(name)
        if source_name is not None and source_name in values:
            kwargs[name] = values[source_name]
        elif param.default is Parameter.empty:
            missing.append(name)

    if missing:
        raise NativeLevelGridContractError(
            f"{cls.__module__}.{cls.__name__} unsupported required parameters: {missing}"
        )
    return cls(**kwargs)


class NativeLevelGridBridge:
    """Mirror canonical Level 3 levels/grids into native managers and BIM adapters."""

    def __init__(self) -> None:
        self.level_manager = LevelManager()
        self.grid_manager = GridManager()
        self.level_adapter = LevelBimAdapter()
        self.grid_adapter = GridBimAdapter()

        self.level_model = _resolve_model(
            _LEVEL_CANDIDATES,
            self.level_adapter,
            {
                "id": "LVL-PREFLIGHT",
                "name": "Preflight",
                "elevation": 0.0,
                "properties": {},
            },
            _LEVEL_ALIASES,
        )
        self.grid_model = _resolve_model(
            _GRID_CANDIDATES,
            self.grid_adapter,
            {
                "id": "GRID-PREFLIGHT",
                "name": "A",
                "start": (0.0, 0.0),
                "end": (0.0, 10.0),
                "properties": {},
            },
            _GRID_ALIASES,
        )
        self.levels: dict[str, NativeMirrorResult] = {}
        self.grids: dict[str, NativeMirrorResult] = {}

    def mirror_level(self, canonical: Any) -> NativeMirrorResult:
        """Create a native Level, register it, then produce its BIM element."""
        native = _construct_exact(
            self.level_model,
            {
                "id": canonical.id,
                "name": canonical.name,
                "elevation": float(canonical.elevation),
                "properties": dict(canonical.properties),
            },
            _LEVEL_ALIASES,
        )
        if not self.level_adapter.supports(native):
            raise NativeLevelGridContractError("LevelBimAdapter rejected native Level")
        self.level_manager.add_level(native)
        bim = self.level_adapter.to_bim_element(native)
        result = NativeMirrorResult(canonical.id, native, bim)
        self.levels[canonical.id] = result
        return result

    def mirror_grid(self, canonical: Any) -> NativeMirrorResult:
        """Create a native Grid, register it, then produce its BIM element."""
        native = _construct_exact(
            self.grid_model,
            {
                "id": canonical.id,
                "name": canonical.name,
                "start": tuple(canonical.start),
                "end": tuple(canonical.end),
                "properties": dict(canonical.properties),
            },
            _GRID_ALIASES,
        )
        if not self.grid_adapter.supports(native):
            raise NativeLevelGridContractError("GridBimAdapter rejected native Grid")
        self.grid_manager.add_grid(native)
        bim = self.grid_adapter.to_bim_element(native)
        result = NativeMirrorResult(canonical.id, native, bim)
        self.grids[canonical.id] = result
        return result

    def report(self) -> dict[str, Any]:
        """Return exact runtime authority information."""
        return {
            "level_model": f"{self.level_model.__module__}.{self.level_model.__name__}",
            "grid_model": f"{self.grid_model.__module__}.{self.grid_model.__name__}",
            "native_levels": len(self.level_manager.get_levels()),
            "native_grids": len(self.grid_manager.get_grids()),
            "mirrored_level_ids": sorted(self.levels),
            "mirrored_grid_ids": sorted(self.grids),
        }
