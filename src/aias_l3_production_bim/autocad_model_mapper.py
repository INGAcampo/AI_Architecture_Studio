"""Read-only AutoCAD ActiveX entity mapping for AIAS."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AutoCADAuthority:
    """Machine-proven AutoCAD 2027 authority and compatibility metadata."""

    product: str = "AutoCAD 2027"
    primary_progid: str = "AutoCAD.Application.26"
    documented_specific_progid: str = "AutoCAD.Application.26.0"
    generic_progid: str = "AutoCAD.Application"

    @property
    def candidates(self) -> tuple[str, ...]:
        """Return the machine-proven authority before compatibility fallbacks."""
        return (
            self.primary_progid,
            self.documented_specific_progid,
            self.generic_progid,
        )


def _get(obj: Any, name: str, default: Any = None) -> Any:
    try:
        return getattr(obj, name)
    except Exception:
        return default


def _number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _point(value: Any) -> tuple[float, ...] | None:
    if value is None:
        return None
    try:
        return tuple(float(x) for x in value)
    except (TypeError, ValueError):
        return None


def _base(entity: Any) -> dict[str, Any]:
    return {
        "object_name": _get(entity, "ObjectName"),
        "handle": _get(entity, "Handle"),
        "layer": _get(entity, "Layer"),
        "color": _get(entity, "Color"),
        "linetype": _get(entity, "Linetype"),
        "visible": _get(entity, "Visible"),
    }


def map_entity(entity: Any) -> dict[str, Any]:
    """Map one COM-like AutoCAD entity to an AIAS-neutral record."""
    data = _base(entity)
    name = str(data.get("object_name") or "")
    lowered = name.lower()

    if "line" in lowered and "polyline" not in lowered:
        data.update(
            kind="line",
            start=_point(_get(entity, "StartPoint")),
            end=_point(_get(entity, "EndPoint")),
        )
    elif "polyline" in lowered:
        data.update(
            kind="polyline",
            coordinates=_point(_get(entity, "Coordinates")),
            closed=bool(_get(entity, "Closed", False)),
            elevation=_number(_get(entity, "Elevation")),
        )
    elif "circle" in lowered:
        data.update(
            kind="circle",
            center=_point(_get(entity, "Center")),
            radius=_number(_get(entity, "Radius")),
        )
    elif "arc" in lowered:
        data.update(
            kind="arc",
            center=_point(_get(entity, "Center")),
            radius=_number(_get(entity, "Radius")),
            start_angle=_number(_get(entity, "StartAngle")),
            end_angle=_number(_get(entity, "EndAngle")),
        )
    elif "text" in lowered:
        data.update(
            kind="text",
            text=_get(entity, "TextString"),
            insertion_point=_point(_get(entity, "InsertionPoint")),
            height=_number(_get(entity, "Height")),
            rotation=_number(_get(entity, "Rotation")),
        )
    elif "blockreference" in lowered or "insert" in lowered:
        data.update(
            kind="block_reference",
            name=_get(entity, "EffectiveName", _get(entity, "Name")),
            insertion_point=_point(_get(entity, "InsertionPoint")),
            rotation=_number(_get(entity, "Rotation")),
            x_scale=_number(_get(entity, "XScaleFactor")),
            y_scale=_number(_get(entity, "YScaleFactor")),
            z_scale=_number(_get(entity, "ZScaleFactor")),
        )
    else:
        data["kind"] = "generic"
        for attr, key in (
            ("StartPoint", "start"),
            ("EndPoint", "end"),
            ("Center", "center"),
            ("InsertionPoint", "insertion_point"),
            ("Coordinates", "coordinates"),
            ("Radius", "radius"),
            ("Area", "area"),
            ("Length", "length"),
            ("Rotation", "rotation"),
        ):
            value = _get(entity, attr)
            if value is None:
                continue
            if attr in {"StartPoint", "EndPoint", "Center", "InsertionPoint", "Coordinates"}:
                data[key] = _point(value)
            else:
                data[key] = _number(value)

    return data


def map_collection(collection: Any, limit: int | None = None) -> list[dict[str, Any]]:
    """Map a bounded COM-like collection without changing it."""
    try:
        count = int(collection.Count)
    except Exception:
        try:
            items = list(collection)
        except Exception:
            return []
        if limit is not None:
            items = items[:limit]
        return [map_entity(item) for item in items]

    if limit is not None:
        count = min(count, max(0, int(limit)))

    result: list[dict[str, Any]] = []
    for index in range(count):
        try:
            result.append(map_entity(collection.Item(index)))
        except Exception as exc:
            result.append({
                "kind": "mapping_error",
                "index": index,
                "error": f"{type(exc).__name__}: {exc}",
            })
    return result


def map_document_snapshot(document: Any, *, entity_limit: int = 1000) -> dict[str, Any]:
    """Create a bounded read-only snapshot of an AutoCAD document."""
    layers = _get(document, "Layers")
    modelspace = _get(document, "ModelSpace")
    paperspace = _get(document, "PaperSpace")

    layer_names: list[str] = []
    if layers is not None:
        try:
            for index in range(int(layers.Count)):
                layer_names.append(str(_get(layers.Item(index), "Name", "")))
        except Exception:
            pass

    return {
        "name": _get(document, "Name"),
        "full_name": _get(document, "FullName"),
        "path": _get(document, "Path"),
        "read_only": _get(document, "ReadOnly"),
        "saved": _get(document, "Saved"),
        "layers": layer_names,
        "modelspace": map_collection(modelspace, entity_limit) if modelspace is not None else [],
        "paperspace": map_collection(paperspace, entity_limit) if paperspace is not None else [],
        "source": "AutoCAD ActiveX",
        "authority": "AutoCAD.Application.26",
        "mutated": False,
    }
