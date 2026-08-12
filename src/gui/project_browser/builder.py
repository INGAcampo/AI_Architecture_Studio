from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from .model import BrowserNode, BrowserNodeKind, ProjectBrowserModel


def _value(obj: Any, name: str, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


class ProjectBrowserBuilder:
    """Construye una jerarquía estable a partir de objetos BIM."""

    LEVELS_GROUP_ID = "group.levels"
    MATERIALS_GROUP_ID = "group.materials"

    def build(
        self,
        objects: Iterable[Any],
        *,
        title: str = "Proyecto",
    ) -> ProjectBrowserModel:
        model = ProjectBrowserModel(title)
        model.add_node(
            BrowserNode(
                self.LEVELS_GROUP_ID,
                "Niveles",
                BrowserNodeKind.GROUP,
            )
        )
        model.add_node(
            BrowserNode(
                self.MATERIALS_GROUP_ID,
                "Materiales",
                BrowserNodeKind.GROUP,
            )
        )

        grouped: dict[str, dict[str, list[Any]]] = defaultdict(
            lambda: defaultdict(list)
        )
        material_names: set[str] = set()

        for obj in objects:
            level = str(_value(obj, "level_name", "Nivel 0"))
            category = str(
                _value(
                    obj,
                    "category",
                    _value(obj, "object_type", type(obj).__name__),
                )
            )
            grouped[level][category].append(obj)

            materials = _value(obj, "materials", ())
            if isinstance(materials, dict):
                materials = materials.values()
            for material in materials or ():
                name = str(
                    _value(material, "name", _value(material, "material_id", material))
                )
                if name:
                    material_names.add(name)

        for level_name in sorted(grouped):
            level_id = f"level.{level_name}"
            model.add_node(
                BrowserNode(
                    level_id,
                    level_name,
                    BrowserNodeKind.LEVEL,
                    parent_id=self.LEVELS_GROUP_ID,
                )
            )
            for category_name in sorted(grouped[level_name]):
                category_id = f"{level_id}.category.{category_name}"
                model.add_node(
                    BrowserNode(
                        category_id,
                        category_name,
                        BrowserNodeKind.CATEGORY,
                        parent_id=level_id,
                    )
                )
                objects_in_category = grouped[level_name][category_name]
                for obj in sorted(
                    objects_in_category,
                    key=lambda item: str(
                        _value(item, "name", _value(item, "object_id", ""))
                    ),
                ):
                    object_id = str(
                        _value(
                            obj,
                            "object_id",
                            _value(obj, "id", id(obj)),
                        )
                    )
                    title_value = str(
                        _value(
                            obj,
                            "name",
                            _value(obj, "title", object_id),
                        )
                    )
                    model.add_node(
                        BrowserNode(
                            node_id=f"object.{object_id}",
                            title=title_value,
                            kind=BrowserNodeKind.OBJECT,
                            parent_id=category_id,
                            object_id=object_id,
                            metadata={
                                "category": category_name,
                                "level": level_name,
                            },
                        )
                    )

        for name in sorted(material_names):
            model.add_node(
                BrowserNode(
                    node_id=f"material.{name}",
                    title=name,
                    kind=BrowserNodeKind.MATERIAL,
                    parent_id=self.MATERIALS_GROUP_ID,
                    metadata={"material_name": name},
                )
            )

        return model
