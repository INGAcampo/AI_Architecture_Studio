from __future__ import annotations
from aias_i18n.runtime import tr

from collections import defaultdict
from typing import Any, Iterable

from .catalogs import FamilyCatalog, MaterialCatalog
from .entities import BimWorkspaceNode, BimWorkspaceNodeKind
from .tree import BimWorkspaceTree


def _read(obj: Any, name: str, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


class BimWorkspaceBuilder:
    GROUPS = {
        "levels": ("group.levels", tr("group.levels")),
        "families": ("group.families", tr("group.families")),
        "materials": ("group.materials", tr("group.materials")),
        "phases": ("group.phases", tr("group.phases")),
    }

    def build(
        self,
        objects: Iterable[Any],
        *,
        materials: MaterialCatalog | None = None,
        families: FamilyCatalog | None = None,
        title: str = "BIM Workspace",
    ) -> BimWorkspaceTree:
        tree = BimWorkspaceTree(title)
        for group_id, group_title in self.GROUPS.values():
            tree.add(
                BimWorkspaceNode(
                    group_id,
                    group_title,
                    BimWorkspaceNodeKind.GROUP,
                )
            )

        grouped: dict[str, dict[str, list[Any]]] = defaultdict(lambda: defaultdict(list))
        phases: set[str] = set()

        for obj in objects:
            level = str(_read(obj, "level_name", "Nivel 0"))
            category = str(
                _read(obj, "category", _read(obj, "object_type", type(obj).__name__))
            )
            grouped[level][category].append(obj)
            phases.add(str(_read(obj, "phase", "New Construction")))

        for level_name in sorted(grouped):
            level_id = f"level.{level_name}"
            tree.add(
                BimWorkspaceNode(
                    level_id,
                    level_name,
                    BimWorkspaceNodeKind.LEVEL,
                    parent_id="group.levels",
                )
            )
            for category_name in sorted(grouped[level_name]):
                category_id = f"{level_id}.category.{category_name}"
                tree.add(
                    BimWorkspaceNode(
                        category_id,
                        category_name,
                        BimWorkspaceNodeKind.CATEGORY,
                        parent_id=level_id,
                    )
                )
                for obj in sorted(
                    grouped[level_name][category_name],
                    key=lambda item: str(_read(item, "name", _read(item, "object_id", ""))),
                ):
                    object_id = str(_read(obj, "object_id", _read(obj, "id", id(obj))))
                    title_value = str(_read(obj, "name", _read(obj, "title", object_id)))
                    tree.add(
                        BimWorkspaceNode(
                            f"instance.{object_id}",
                            title_value,
                            BimWorkspaceNodeKind.INSTANCE,
                            parent_id=category_id,
                            object_id=object_id,
                            metadata={
                                "level": level_name,
                                "category": category_name,
                                "phase": str(_read(obj, "phase", "New Construction")),
                                "family_id": _read(obj, "family_id"),
                                "type_id": _read(obj, "type_id"),
                            },
                        )
                    )

        for phase in sorted(phases):
            tree.add(
                BimWorkspaceNode(
                    f"phase.{phase}",
                    phase,
                    BimWorkspaceNodeKind.PHASE,
                    parent_id="group.phases",
                )
            )

        if families:
            for category, category_families in families.by_category().items():
                category_id = f"family.category.{category}"
                tree.add(
                    BimWorkspaceNode(
                        category_id,
                        category,
                        BimWorkspaceNodeKind.CATEGORY,
                        parent_id="group.families",
                    )
                )
                for family in category_families:
                    family_id = f"family.{family.family_id}"
                    tree.add(
                        BimWorkspaceNode(
                            family_id,
                            family.name,
                            BimWorkspaceNodeKind.FAMILY,
                            parent_id=category_id,
                            metadata={"family_id": family.family_id},
                        )
                    )
                    for family_type in family.types:
                        tree.add(
                            BimWorkspaceNode(
                                f"type.{family_type.type_id}",
                                family_type.name,
                                BimWorkspaceNodeKind.TYPE,
                                parent_id=family_id,
                                metadata={
                                    "family_id": family.family_id,
                                    "type_id": family_type.type_id,
                                },
                            )
                        )

        if materials:
            for category, category_materials in materials.by_category().items():
                category_id = f"material.category.{category}"
                tree.add(
                    BimWorkspaceNode(
                        category_id,
                        category,
                        BimWorkspaceNodeKind.CATEGORY,
                        parent_id="group.materials",
                    )
                )
                for material in category_materials:
                    tree.add(
                        BimWorkspaceNode(
                            f"material.{material.material_id}",
                            material.name,
                            BimWorkspaceNodeKind.MATERIAL,
                            parent_id=category_id,
                            metadata={
                                "material_id": material.material_id,
                                "density": material.density,
                            },
                        )
                    )

        return tree
