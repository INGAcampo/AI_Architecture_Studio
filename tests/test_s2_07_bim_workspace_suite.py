import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from dataclasses import dataclass
import pytest

from gui.bim_workspace import (
    BimWorkspaceBuilder,
    BimWorkspaceController,
    BimWorkspaceNode,
    BimWorkspaceNodeKind,
    BimWorkspaceTree,
    FamilyCatalog,
    FamilyDefinition,
    FamilyTypeDefinition,
    MaterialCatalog,
    MaterialDefinition,
)


@dataclass
class Obj:
    object_id: str
    name: str
    level_name: str = "Nivel 1"
    category: str = "Walls"
    phase: str = "New Construction"
    family_id: str | None = None
    type_id: str | None = None


@pytest.mark.parametrize("index", range(20))
def test_tree_adds_distinct_nodes(index):
    tree = BimWorkspaceTree()
    tree.add(
        BimWorkspaceNode(
            f"group.{index}",
            f"Grupo {index}",
            BimWorkspaceNodeKind.GROUP,
        )
    )
    assert tree.require(f"group.{index}").title == f"Grupo {index}"


@pytest.mark.parametrize("query,expected", [
    ("con", "Concreto"),
    ("steel", "Steel"),
    ("wood", "Wood"),
    ("glass", "Glass"),
    ("brick", "Brick"),
    ("stone", "Stone"),
    ("gypsum", "Gypsum"),
    ("insulation", "Insulation"),
    ("paint", "Paint"),
    ("tile", "Tile"),
])
def test_material_catalog_search(query, expected):
    catalog = MaterialCatalog()
    names = ["Concreto", "Steel", "Wood", "Glass", "Brick", "Stone", "Gypsum", "Insulation", "Paint", "Tile"]
    for i, name in enumerate(names):
        catalog.register(MaterialDefinition(f"m{i}", name, "General"))
    assert catalog.search(query)[0].name == expected


@pytest.mark.parametrize("category", [
    "Walls", "Doors", "Windows", "Floors", "Roofs",
    "Columns", "Beams", "Stairs", "Furniture", "MEP",
])
def test_family_catalog_groups_by_category(category):
    catalog = FamilyCatalog()
    family = FamilyDefinition(f"f.{category}", f"Family {category}", category)
    catalog.register(family)
    assert catalog.by_category()[category][0] == family


@pytest.mark.parametrize("level", [f"Nivel {i}" for i in range(1, 11)])
def test_builder_creates_levels(level):
    tree = BimWorkspaceBuilder().build([Obj(f"o.{level}", "Objeto", level_name=level)])
    assert tree.require(f"level.{level}").kind is BimWorkspaceNodeKind.LEVEL


@pytest.mark.parametrize("category", [
    "Walls", "Doors", "Windows", "Floors", "Roofs",
    "Columns", "Beams", "Stairs", "Furniture", "Spaces",
])
def test_builder_creates_categories(category):
    tree = BimWorkspaceBuilder().build([Obj(f"o.{category}", "Objeto", category=category)])
    node = tree.require(f"level.Nivel 1.category.{category}")
    assert node.kind is BimWorkspaceNodeKind.CATEGORY


@pytest.mark.parametrize("phase", [
    "Existing", "Demolition", "New Construction", "Future",
    "Phase A", "Phase B", "Phase C", "Tender", "Construction", "As Built",
])
def test_builder_creates_phases(phase):
    tree = BimWorkspaceBuilder().build([Obj(f"o.{phase}", "Objeto", phase=phase)])
    assert tree.require(f"phase.{phase}").kind is BimWorkspaceNodeKind.PHASE


@pytest.mark.parametrize("kind", [
    BimWorkspaceNodeKind.LEVEL,
    BimWorkspaceNodeKind.CATEGORY,
    BimWorkspaceNodeKind.FAMILY,
    BimWorkspaceNodeKind.TYPE,
    BimWorkspaceNodeKind.INSTANCE,
    BimWorkspaceNodeKind.MATERIAL,
    BimWorkspaceNodeKind.PHASE,
    BimWorkspaceNodeKind.GROUP,
    BimWorkspaceNodeKind.ROOT,
    BimWorkspaceNodeKind.INSTANCE,
])
def test_filter_by_kind(kind):
    tree = BimWorkspaceTree()
    if kind is BimWorkspaceNodeKind.ROOT:
        assert tree.filter(kinds={kind})[0].kind is kind
        return
    tree.add(BimWorkspaceNode(f"n.{kind.value}", kind.value, kind))
    assert tree.filter(kinds={kind})[0].kind is kind


@pytest.mark.parametrize("name", [
    "Concreto 25 MPa", "Acero A36", "Madera laminada", "Vidrio 10 mm",
    "Ladrillo", "Piedra", "Yeso", "Aislante", "Pintura", "Cerámica",
])
def test_material_validation_and_registration(name):
    catalog = MaterialCatalog()
    material = MaterialDefinition(name.lower().replace(" ", "."), name, density=1000)
    catalog.register(material)
    assert catalog.get(material.material_id).name == name


@pytest.mark.parametrize("type_name", [
    "100 mm", "150 mm", "200 mm", "250 mm", "300 mm",
    "450 mm", "600 mm", "900 mm", "1200 mm", "1500 mm",
])
def test_family_type_registration(type_name):
    family = FamilyDefinition("wall.basic", "Basic Wall", "Walls")
    catalog = FamilyCatalog()
    catalog.register(family)
    updated = catalog.add_type(
        family.family_id,
        FamilyTypeDefinition(
            f"type.{type_name}",
            type_name,
            family.family_id,
        ),
    )
    assert updated.types[-1].name == type_name


def test_node_validation():
    with pytest.raises(ValueError):
        BimWorkspaceNode("", "Nodo", BimWorkspaceNodeKind.GROUP)


def test_tree_duplicate_rejected():
    tree = BimWorkspaceTree()
    tree.add(BimWorkspaceNode("a", "A", BimWorkspaceNodeKind.GROUP))
    with pytest.raises(KeyError):
        tree.add(BimWorkspaceNode("a", "A2", BimWorkspaceNodeKind.GROUP))


def test_tree_remove_subtree():
    tree = BimWorkspaceTree()
    tree.add(BimWorkspaceNode("a", "A", BimWorkspaceNodeKind.GROUP))
    tree.add(BimWorkspaceNode("b", "B", BimWorkspaceNodeKind.INSTANCE, parent_id="a"))
    assert set(tree.remove("a")) == {"a", "b"}


def test_material_duplicate_rejected():
    catalog = MaterialCatalog()
    material = MaterialDefinition("m1", "Concreto")
    catalog.register(material)
    with pytest.raises(KeyError):
        catalog.register(material)


def test_family_duplicate_rejected():
    catalog = FamilyCatalog()
    family = FamilyDefinition("f1", "Wall", "Walls")
    catalog.register(family)
    with pytest.raises(KeyError):
        catalog.register(family)


def test_builder_includes_family_hierarchy():
    catalog = FamilyCatalog()
    family = FamilyDefinition(
        "f1",
        "Basic Wall",
        "Walls",
        types=(FamilyTypeDefinition("t1", "200 mm", "f1"),),
    )
    catalog.register(family)
    tree = BimWorkspaceBuilder().build([], families=catalog)
    assert tree.require("family.f1").kind is BimWorkspaceNodeKind.FAMILY
    assert tree.require("type.t1").kind is BimWorkspaceNodeKind.TYPE


def test_builder_includes_material_hierarchy():
    catalog = MaterialCatalog()
    catalog.register(MaterialDefinition("m1", "Concreto", "Structural"))
    tree = BimWorkspaceBuilder().build([], materials=catalog)
    assert tree.require("material.m1").kind is BimWorkspaceNodeKind.MATERIAL


def test_controller_selects_workspace_object():
    class Workspace:
        def __init__(self):
            self.selection = ()
        def set_selection(self, values):
            self.selection = tuple(values)

    tree = BimWorkspaceBuilder().build([Obj("w1", "Muro")])
    workspace = Workspace()
    controller = BimWorkspaceController(tree, workspace=workspace)
    controller.select_node("instance.w1")
    assert workspace.selection == ("w1",)


def test_controller_filter_and_state():
    tree = BimWorkspaceBuilder().build([Obj("w1", "Muro principal")])
    controller = BimWorkspaceController(tree)
    result = controller.set_filter("principal", {BimWorkspaceNodeKind.INSTANCE})
    assert result[0].object_id == "w1"
    assert controller.state.query == "principal"


def test_controller_refresh_preserves_selection():
    first = BimWorkspaceBuilder().build([Obj("w1", "Muro")])
    controller = BimWorkspaceController(first)
    controller.select_node("instance.w1")
    second = BimWorkspaceBuilder().build([Obj("w1", "Muro actualizado")])
    controller.refresh(second)
    assert controller.state.selected_node_id == "instance.w1"


def test_qt_widget_builds():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication
    from gui.bim_workspace import BimWorkspaceWidget

    app = QApplication.instance() or QApplication([])
    controller = BimWorkspaceController(
        BimWorkspaceBuilder().build([Obj("w1", "Muro")])
    )
    widget = BimWorkspaceWidget(controller)
    assert widget.tree.topLevelItemCount() == 1
    widget.close()


@pytest.mark.parametrize("index", range(9))
def test_material_catalog_remove_cases(index):
    catalog = MaterialCatalog()
    material = MaterialDefinition(f"remove.{index}", f"Material {index}")
    catalog.register(material)
    removed = catalog.remove(material.material_id)
    assert removed == material
    with pytest.raises(KeyError):
        catalog.get(material.material_id)
