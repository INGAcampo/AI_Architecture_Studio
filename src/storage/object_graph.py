"""Serialización JSON segura de grafos de objetos Python usados por la escena AIAS."""
from __future__ import annotations

import importlib
from enum import Enum
from pathlib import Path
from typing import Any


class ObjectGraphError(RuntimeError):
    pass


class ObjectGraphCodec:
    """Codifica objetos simples conservando referencias compartidas y clases."""

    _SKIP_NAMES = {
        "kernel", "services", "parent", "_parent", "renderer", "canvas",
        "workspace", "command_manager", "tool_manager", "selection_manager",
        "highlight", "grip_editor", "dynamic_input_manager",
    }

    def encode(self, value: Any) -> Any:
        self._memo: dict[int, str] = {}
        self._counter = 0
        return self._encode(value)

    def decode(self, payload: Any) -> Any:
        self._objects: dict[str, Any] = {}
        return self._decode(payload)

    def _new_ref(self) -> str:
        self._counter += 1
        return str(self._counter)

    def _encode(self, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, Path):
            return {"$path": str(value)}
        if isinstance(value, Enum):
            cls = value.__class__
            return {"$enum": f"{cls.__module__}:{cls.__qualname__}", "value": value.value}

        object_id = id(value)
        if object_id in self._memo:
            return {"$ref": self._memo[object_id]}
        ref = self._new_ref()
        self._memo[object_id] = ref

        if isinstance(value, list):
            return {"$id": ref, "$list": [self._encode(v) for v in value]}
        if isinstance(value, tuple):
            return {"$id": ref, "$tuple": [self._encode(v) for v in value]}
        if isinstance(value, set):
            return {"$id": ref, "$set": [self._encode(v) for v in value]}
        if isinstance(value, dict):
            return {
                "$id": ref,
                "$dict": [[self._encode(k), self._encode(v)] for k, v in value.items()],
            }

        module = value.__class__.__module__
        qualname = value.__class__.__qualname__
        if module.startswith("PySide6"):
            raise ObjectGraphError(f"Objeto Qt no serializable: {module}.{qualname}")

        state = {}
        for name, item in vars(value).items():
            if name in self._SKIP_NAMES or name.startswith("_qt_"):
                continue
            try:
                state[name] = self._encode(item)
            except (ObjectGraphError, TypeError):
                continue
        return {
            "$id": ref,
            "$class": f"{module}:{qualname}",
            "$state": state,
        }

    @staticmethod
    def _resolve_class(spec: str):
        module_name, qualname = spec.split(":", 1)
        module = importlib.import_module(module_name)
        obj = module
        for part in qualname.split("."):
            obj = getattr(obj, part)
        return obj

    def _decode(self, payload: Any) -> Any:
        if payload is None or isinstance(payload, (bool, int, float, str)):
            return payload
        if not isinstance(payload, dict):
            raise ObjectGraphError("Payload de grafo inválido")
        if "$ref" in payload:
            return self._objects[payload["$ref"]]
        if "$path" in payload:
            return Path(payload["$path"])
        if "$enum" in payload:
            return self._resolve_class(payload["$enum"])(payload["value"])

        ref = payload.get("$id")
        if "$list" in payload:
            obj: Any = []
            if ref: self._objects[ref] = obj
            obj.extend(self._decode(v) for v in payload["$list"])
            return obj
        if "$tuple" in payload:
            temp = [self._decode(v) for v in payload["$tuple"]]
            obj = tuple(temp)
            if ref: self._objects[ref] = obj
            return obj
        if "$set" in payload:
            obj = set()
            if ref: self._objects[ref] = obj
            obj.update(self._decode(v) for v in payload["$set"])
            return obj
        if "$dict" in payload:
            obj = {}
            if ref: self._objects[ref] = obj
            for key, value in payload["$dict"]:
                obj[self._decode(key)] = self._decode(value)
            return obj
        if "$class" in payload:
            cls = self._resolve_class(payload["$class"])
            obj = cls.__new__(cls)
            if ref: self._objects[ref] = obj
            for name, value in payload.get("$state", {}).items():
                setattr(obj, name, self._decode(value))
            return obj
        raise ObjectGraphError("Nodo de grafo desconocido")
