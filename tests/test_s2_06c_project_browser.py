import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from dataclasses import dataclass

import pytest

from gui.project_browser import (
    BrowserNode,
    BrowserNodeKind,
    ProjectBrowserBuilder,
    ProjectBrowserController,
    ProjectBrowserModel,
    ProjectBrowserState,
)


def test_node_validation():
    with pytest.raises(ValueError):
        BrowserNode("", "Nodo", BrowserNodeKind.GROUP)
    with pytest.raises(ValueError):
        BrowserNode("node", "", BrowserNodeKind.GROUP)


def test_add_node_and_children():
    model = ProjectBrowserModel()
    node = model.add_node(
        BrowserNode("levels", "Niveles", BrowserNodeKind.GROUP)
    )
    assert model.children_of(model.ROOT_ID) == (node,)
    assert model.revision == 1


def test_duplicate_node_rejected():
    model = ProjectBrowserModel()
    model.add_node(BrowserNode("a", "A", BrowserNodeKind.GROUP))
    with pytest.raises(KeyError):
        model.add_node(BrowserNode("a", "A2", BrowserNodeKind.GROUP))


def test_remove_subtree():
    model = ProjectBrowserModel()
    model.add_node(BrowserNode("a", "A", BrowserNodeKind.GROUP))
    model.add_node(
        BrowserNode("b", "B", BrowserNodeKind.OBJECT, parent_id="a")
    )
    removed = model.remove_node("a")
    assert set(removed) == {"a", "b"}
    with pytest.raises(KeyError):
        model.require("b")


def test_root_cannot_be_removed():
    with pytest.raises(ValueError):
        ProjectBrowserModel().remove_node(ProjectBrowserModel.ROOT_ID)


def test_move_node():
    model = ProjectBrowserModel()
    model.add_node(BrowserNode("a", "A", BrowserNodeKind.GROUP))
    model.add_node(BrowserNode("b", "B", BrowserNodeKind.GROUP))
    model.add_node(
        BrowserNode("c", "C", BrowserNodeKind.OBJECT, parent_id="a")
    )
    model.move_node("c", "b")
    assert model.require("c").parent_id == "b"


def test_find_by_object_id():
    model = ProjectBrowserModel()
    model.add_node(
        BrowserNode(
            "object.wall",
            "Wall",
            BrowserNodeKind.OBJECT,
            object_id="wall",
        )
    )
    assert model.find_by_object_id("wall").node_id == "object.wall"


def test_filter_by_title_and_metadata():
    model = ProjectBrowserModel()
    model.add_node(
        BrowserNode(
            "object.wall",
            "Muro exterior",
            BrowserNodeKind.OBJECT,
            object_id="w1",
            metadata={"level": "Nivel 1"},
        )
    )
    assert model.filter("exterior")[0].object_id == "w1"
    assert model.filter("nivel 1")[0].object_id == "w1"


@dataclass
class Obj:
    object_id: str
    name: str
    level_name: str
    category: str
    materials: tuple = ()


def test_builder_creates_levels_categories_and_objects():
    model = ProjectBrowserBuilder().build(
        [
            Obj("w1", "Muro 1", "Nivel 1", "Walls"),
            Obj("d1", "Puerta 1", "Nivel 1", "Doors"),
        ]
    )
    assert model.find_by_object_id("w1").metadata["category"] == "Walls"
    assert model.require("level.Nivel 1").kind is BrowserNodeKind.LEVEL


def test_builder_creates_materials():
    model = ProjectBrowserBuilder().build(
        [
            Obj(
                "w1",
                "Muro",
                "Nivel 1",
                "Walls",
                materials=({"name": "Concreto"},),
            )
        ]
    )
    assert model.require("material.Concreto").kind is BrowserNodeKind.MATERIAL


def test_builder_accepts_dict_objects():
    model = ProjectBrowserBuilder().build(
        [
            {
                "object_id": "x1",
                "name": "Objeto",
                "level_name": "Nivel 2",
                "category": "Generic",
            }
        ]
    )
    assert model.find_by_object_id("x1").title == "Objeto"


def test_state_roundtrip():
    state = ProjectBrowserState(
        expanded_node_ids={"a", "b"},
        selected_node_id="a",
        filter_text="muro",
    )
    assert ProjectBrowserState.from_snapshot(state.snapshot()).snapshot() == state.snapshot()


def test_controller_filter():
    model = ProjectBrowserModel()
    model.add_node(BrowserNode("a", "Muros", BrowserNodeKind.GROUP))
    controller = ProjectBrowserController(model)
    assert controller.set_filter("muro")[0].node_id == "a"
    assert controller.state.filter_text == "muro"


def test_controller_selects_object_in_workspace():
    class Workspace:
        def __init__(self):
            self.selection = None
        def set_selection(self, values):
            self.selection = tuple(values)

    model = ProjectBrowserModel()
    model.add_node(
        BrowserNode(
            "object.w1",
            "Muro",
            BrowserNodeKind.OBJECT,
            object_id="w1",
        )
    )
    workspace = Workspace()
    controller = ProjectBrowserController(model, workspace=workspace)
    controller.select_node("object.w1")
    assert workspace.selection == ("w1",)


def test_controller_select_object():
    model = ProjectBrowserModel()
    model.add_node(
        BrowserNode(
            "object.w1",
            "Muro",
            BrowserNodeKind.OBJECT,
            object_id="w1",
        )
    )
    controller = ProjectBrowserController(model)
    assert controller.select_object("w1") == "object.w1"
    assert controller.select_object("missing") is None


def test_controller_expansion_state():
    model = ProjectBrowserModel()
    model.add_node(BrowserNode("a", "A", BrowserNodeKind.GROUP))
    controller = ProjectBrowserController(model)
    controller.set_expanded("a", True)
    assert "a" in controller.state.expanded_node_ids
    controller.set_expanded("a", False)
    assert "a" not in controller.state.expanded_node_ids


def test_controller_refresh_preserves_selected_object():
    first = ProjectBrowserModel()
    first.add_node(
        BrowserNode(
            "object.w1",
            "Muro",
            BrowserNodeKind.OBJECT,
            object_id="w1",
        )
    )
    controller = ProjectBrowserController(first)
    controller.select_node("object.w1")

    second = ProjectBrowserModel()
    second.add_node(
        BrowserNode(
            "new.w1",
            "Muro actualizado",
            BrowserNodeKind.OBJECT,
            object_id="w1",
        )
    )
    controller.refresh(second)
    assert controller.state.selected_node_id == "new.w1"


def test_controller_workspace_selection():
    model = ProjectBrowserModel()
    model.add_node(
        BrowserNode(
            "object.w1",
            "Muro",
            BrowserNodeKind.OBJECT,
            object_id="w1",
        )
    )
    controller = ProjectBrowserController(model)
    assert controller.handle_workspace_selection(["w1"]) == "object.w1"
    assert controller.handle_workspace_selection([]) is None


def test_qt_widget_builds_tree():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication
    from gui.project_browser import ProjectBrowserWidget

    app = QApplication.instance() or QApplication([])
    model = ProjectBrowserModel()
    model.add_node(BrowserNode("a", "A", BrowserNodeKind.GROUP))
    widget = ProjectBrowserWidget(ProjectBrowserController(model))
    assert widget.tree.topLevelItemCount() == 1
    widget.close()


def test_qt_widget_select_object():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication
    from gui.project_browser import ProjectBrowserWidget

    app = QApplication.instance() or QApplication([])
    model = ProjectBrowserModel()
    model.add_node(
        BrowserNode(
            "object.w1",
            "Muro",
            BrowserNodeKind.OBJECT,
            object_id="w1",
        )
    )
    widget = ProjectBrowserWidget(ProjectBrowserController(model))
    assert widget.select_object("w1")
    assert not widget.select_object("missing")
    widget.close()
