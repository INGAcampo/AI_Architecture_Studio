from __future__ import annotations

from engines.bim import (
    BimCategory,
    BimDocument,
    RelationshipType,
    create_default_bim_adapter_registry,
)
from engines.geometry.point import Point
from models.architectural.door import Door
from models.architectural.grid import Grid
from models.architectural.level import Level
from models.architectural.room import Room
from models.architectural.slab import Slab
from models.architectural.wall import Wall
from models.architectural.window import Window
from models.structural.beam import Beam
from models.structural.column import Column
from models.structural.foundation import Foundation


def test_default_registry_contains_ten_native_adapters() -> None:
    registry = create_default_bim_adapter_registry()

    assert len(registry.adapters) == 10


def test_level_and_grid_are_adapted_with_native_parameters() -> None:
    registry = create_default_bim_adapter_registry()
    level = Level("Nivel 2", 3.20)
    grid = Grid("A", Point(0, 0), Point(10, 0))

    level_bim = registry.adapt(level)
    grid_bim = registry.adapt(grid, level_id=level_bim.element_id)

    assert level_bim.category is BimCategory.STOREY
    assert level_bim.parameters["Elevation"] == 3.20
    assert grid_bim.category is BimCategory.GRID
    assert grid_bim.parameters["Label"] == "A"
    assert grid_bim.level_id == level_bim.element_id


def test_wall_door_and_window_preserve_identity_and_host_relations() -> None:
    registry = create_default_bim_adapter_registry()
    document = BimDocument()
    wall = Wall(
        [Point(0, 0), Point(5, 0)],
        thickness=0.20,
        height=3.00,
    )

    class Opening:
        def __init__(self, host_wall):
            self.host_wall = host_wall
            self.center_point = Point(1, 0)

    opening = Opening(wall)
    door = Door(opening=opening, width=0.90)
    window = Window(opening=opening, width=1.20)

    wall_bim = registry.add_to_document(document, wall)
    door_bim = registry.add_to_document(document, door)
    window_bim = registry.add_to_document(document, window)

    assert wall_bim.element_id == wall.id
    assert door_bim.element_id == door.id
    assert window_bim.element_id == window.id
    assert door_bim.parameters["Width"] == 0.90
    assert window_bim.parameters["SillHeight"] == 0.90

    door_relations = document.relationships_for(door_bim.element_id)
    window_relations = document.relationships_for(window_bim.element_id)

    assert door_relations[0].relationship_type is RelationshipType.HOSTS
    assert window_relations[0].relationship_type is RelationshipType.HOSTS
    assert door_relations[0].source_id == wall_bim.element_id


def test_room_and_slab_create_space_containment_relation() -> None:
    registry = create_default_bim_adapter_registry()
    document = BimDocument()
    boundary = [
        Point(0, 0),
        Point(4, 0),
        Point(4, 3),
        Point(0, 3),
    ]
    room = Room(boundary=boundary, name="Dormitorio", number="101")
    slab = Slab(host_room=room, thickness=0.18)

    room_bim = registry.add_to_document(document, room)
    slab_bim = registry.add_to_document(document, slab)

    assert room_bim.category is BimCategory.SPACE
    assert room_bim.parameters["Area"] == 12.0
    assert slab_bim.category is BimCategory.SLAB
    assert slab_bim.parameters["Thickness"] == 0.18
    assert document.relationships_for(slab_bim.element_id)[0].source_id == room_bim.element_id


def test_structural_objects_receive_bim_categories_and_parameters() -> None:
    registry = create_default_bim_adapter_registry()

    beam = Beam()
    beam.length = 5.0
    column = Column()
    foundation = Foundation()

    beam_bim = registry.adapt(beam)
    column_bim = registry.adapt(column)
    foundation_bim = registry.adapt(foundation)

    assert beam_bim.category is BimCategory.BEAM
    assert beam_bim.parameters["Length"] == 5.0
    assert column_bim.category is BimCategory.COLUMN
    assert column_bim.parameters["Width"] == 0.30
    assert foundation_bim.category is BimCategory.FOUNDATION
    assert foundation_bim.parameters["SoilBearingCapacity"] == 150.0


def test_unknown_object_is_rejected_explicitly() -> None:
    registry = create_default_bim_adapter_registry()

    class Unknown:
        pass

    try:
        registry.adapt(Unknown())
    except TypeError as error:
        assert "No existe un adaptador BIM" in str(error)
    else:
        raise AssertionError("Un objeto desconocido no debe adaptarse silenciosamente.")
