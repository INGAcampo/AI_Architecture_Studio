import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from dataclasses import dataclass

import pytest

from gui.property_palette import (
    PropertyDescriptor,
    PropertyEditAction,
    PropertyPaletteController,
    PropertyPaletteModel,
    PropertySchemaRegistry,
    PropertySelectionAdapter,
    PropertyValueType,
    default_wall_schema,
)


@dataclass
class WallLike:
    object_type: str = "Wall"
    name: str = "Muro"
    height: float = 3.0
    thickness: float = 0.20
    base_elevation: float = 0.0
    ifc_class: str = "IfcWall"
    length: float = 5.0
    area: float = 15.0
    volume: float = 3.0


def registry():
    result = PropertySchemaRegistry()
    result.register("Wall", default_wall_schema())
    return result


def test_descriptor_validation():
    with pytest.raises(ValueError):
        PropertyDescriptor("", "Nombre")
    with pytest.raises(ValueError):
        PropertyDescriptor("name", "")
    with pytest.raises(ValueError):
        PropertyDescriptor(
            "state",
            "Estado",
            value_type=PropertyValueType.ENUM,
        )


def test_model_set_entries_and_groups():
    adapter = PropertySelectionAdapter(registry())
    model = PropertyPaletteModel()
    model.set_entries(adapter.build_entries([WallLike()]))
    assert "Dimensiones" in model.groups()
    assert model.require("height").value == 3.0


def test_duplicate_entries_rejected():
    descriptor = PropertyDescriptor("name", "Nombre")
    from gui.property_palette import PropertyEntry
    model = PropertyPaletteModel()
    with pytest.raises(KeyError):
        model.set_entries([
            PropertyEntry(descriptor, "A"),
            PropertyEntry(descriptor, "B"),
        ])


def test_float_normalization_and_range():
    model = PropertyPaletteModel()
    from gui.property_palette import PropertyEntry
    model.set_entries([
        PropertyEntry(
            PropertyDescriptor(
                "height",
                "Altura",
                value_type=PropertyValueType.LENGTH,
                minimum=0.1,
            ),
            3.0,
        )
    ])
    assert model.update_value("height", "4.25").value == 4.25
    with pytest.raises(ValueError):
        model.update_value("height", 0)


def test_read_only_rejected():
    model = PropertyPaletteModel()
    from gui.property_palette import PropertyEntry
    model.set_entries([
        PropertyEntry(
            PropertyDescriptor(
                "area",
                "Área",
                value_type=PropertyValueType.READ_ONLY,
                editable=False,
            ),
            10.0,
        )
    ])
    with pytest.raises(PermissionError):
        model.update_value("area", 20)


def test_boolean_normalization():
    model = PropertyPaletteModel()
    from gui.property_palette import PropertyEntry
    model.set_entries([
        PropertyEntry(
            PropertyDescriptor(
                "visible",
                "Visible",
                value_type=PropertyValueType.BOOLEAN,
            ),
            False,
        )
    ])
    assert model.update_value("visible", "sí").value is True
    with pytest.raises(ValueError):
        model.update_value("visible", "quizás")


def test_enum_validation():
    model = PropertyPaletteModel()
    from gui.property_palette import PropertyEntry
    model.set_entries([
        PropertyEntry(
            PropertyDescriptor(
                "phase",
                "Fase",
                value_type=PropertyValueType.ENUM,
                enum_values=("Existing", "New"),
            ),
            "New",
        )
    ])
    with pytest.raises(ValueError):
        model.update_value("phase", "Other")


def test_model_filter():
    adapter = PropertySelectionAdapter(registry())
    model = PropertyPaletteModel()
    model.set_entries(adapter.build_entries([WallLike()]))
    assert model.filter("altura")[0].descriptor.property_id == "height"
    assert any(
        entry.descriptor.property_id == "volume"
        for entry in model.filter("cantidades")
    )


def test_registry_duplicate_rejected():
    schemas = registry()
    with pytest.raises(KeyError):
        schemas.register("Wall", default_wall_schema())


def test_adapter_single_selection():
    adapter = PropertySelectionAdapter(registry())
    entries = adapter.build_entries([WallLike(height=3.5)])
    by_id = {entry.descriptor.property_id: entry for entry in entries}
    assert by_id["height"].value == 3.5
    assert not by_id["height"].mixed


def test_adapter_multiple_selection_mixed():
    adapter = PropertySelectionAdapter(registry())
    entries = adapter.build_entries([
        WallLike(height=3.0),
        WallLike(height=4.0),
    ])
    by_id = {entry.descriptor.property_id: entry for entry in entries}
    assert by_id["height"].mixed
    assert by_id["height"].value is None
    assert not by_id["thickness"].mixed


def test_controller_edits_single_object():
    wall = WallLike()
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
    )
    controller.set_selection([wall])
    controller.edit_property("height", 4.0)
    assert wall.height == 4.0
    assert controller.model.require("height").value == 4.0


def test_controller_edits_multiple_objects():
    walls = [WallLike(height=3.0), WallLike(height=4.0)]
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
    )
    controller.set_selection(walls)
    controller.edit_property("height", 3.5)
    assert [wall.height for wall in walls] == [3.5, 3.5]
    assert not controller.model.require("height").mixed


def test_controller_requires_selection():
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
    )
    with pytest.raises(RuntimeError):
        controller.edit_property("height", 3)


def test_history_action_undo_redo():
    wall = WallLike(height=3.0)
    action = PropertyEditAction.create([wall], "height", 4.0)
    action.redo()
    assert wall.height == 4.0
    action.undo()
    assert wall.height == 3.0


def test_controller_uses_history_execute():
    class History:
        def __init__(self):
            self.action = None
        def execute(self, action):
            self.action = action
            action.redo()

    wall = WallLike()
    history = History()
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
        history_manager=history,
    )
    controller.set_selection([wall])
    controller.edit_property("height", 4)
    assert history.action.property_id == "height"
    assert wall.height == 4.0


def test_events_are_published():
    events = []
    wall = WallLike()
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
        event_dispatcher=lambda name, payload: events.append((name, payload)),
    )
    controller.set_selection([wall])
    controller.edit_property("height", 4)
    assert events[-1][0] == "property_palette.property.changed"


def test_clear_selection():
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
    )
    controller.set_selection([WallLike()])
    controller.clear_selection()
    assert controller.selection == ()
    assert controller.model.entries() == ()


def test_qt_widget_builds_groups():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication
    from gui.property_palette import PropertyPaletteWidget

    app = QApplication.instance() or QApplication([])
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
    )
    controller.set_selection([WallLike()])
    widget = PropertyPaletteWidget(controller)
    assert "height" in widget._editors
    assert "area" in widget._editors
    widget.close()


def test_qt_widget_empty_state():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication
    from gui.property_palette import PropertyPaletteWidget

    app = QApplication.instance() or QApplication([])
    controller = PropertyPaletteController(
        PropertyPaletteModel(),
        PropertySelectionAdapter(registry()),
    )
    widget = PropertyPaletteWidget(controller)
    assert widget.empty_label.isVisible() or not widget.scroll.isVisible()
    widget.close()
