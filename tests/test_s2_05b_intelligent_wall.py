import math

import pytest

from engines.bim.object_model import (
    MaterialRef,
    ObjectType,
    Wall,
    WallLayer,
    WallPoint,
)


def test_wall_is_bim_wall():
    wall = Wall((0, 0), (5, 0))
    assert wall.object_type is ObjectType.WALL
    assert wall.IFC_CLASS == "IfcWall"


def test_wall_default_dimensions():
    wall = Wall((0, 0), (5, 0))
    assert wall.height == 3.0
    assert wall.thickness == 0.20
    assert wall.base_elevation == 0.0


def test_wall_rejects_zero_length_axis():
    with pytest.raises(ValueError):
        Wall((1, 1), (1, 1))


def test_wall_rejects_non_positive_dimensions():
    with pytest.raises(ValueError):
        Wall((0, 0), (1, 0), height=0)
    with pytest.raises(ValueError):
        Wall((0, 0), (1, 0), thickness=-0.1)


def test_wall_length_works_in_3d():
    wall = Wall((0, 0, 0), (3, 4, 12))
    assert wall.length == 13.0


def test_wall_direction_is_normalized():
    wall = Wall((0, 0), (3, 4))
    assert wall.direction == pytest.approx((0.6, 0.8, 0.0))


def test_wall_midpoint():
    wall = Wall((0, 0, 0), (4, 2, 6))
    assert wall.midpoint.to_tuple() == (2.0, 1.0, 3.0)


def test_wall_quantities():
    wall = Wall((0, 0), (5, 0), height=3, thickness=0.2)
    assert wall.gross_side_area == pytest.approx(15.0)
    assert wall.footprint_area == pytest.approx(1.0)
    assert wall.gross_volume == pytest.approx(3.0)


def test_wall_top_elevation():
    wall = Wall((0, 0), (2, 0), height=3.2, base_elevation=1.5)
    assert wall.top_elevation == pytest.approx(4.7)


def test_set_axis_updates_revision_and_quantities():
    wall = Wall((0, 0), (2, 0))
    assert wall.set_axis((0, 0), (4, 0))
    assert wall.length == 4.0
    assert wall.revision == 1


def test_set_axis_ignores_redundant_change():
    wall = Wall((0, 0), (2, 0))
    assert wall.set_axis((0, 0), (2, 0)) is False
    assert wall.revision == 0


def test_height_change_updates_revision():
    wall = Wall((0, 0), (2, 0))
    assert wall.set_height(4.0)
    assert wall.height == 4.0
    assert wall.revision == 1
    assert wall.set_height(4.0) is False


def test_base_elevation_change_updates_top():
    wall = Wall((0, 0), (2, 0), height=3)
    wall.set_base_elevation(-0.5)
    assert wall.top_elevation == 2.5


def test_wall_layer_validation():
    with pytest.raises(ValueError):
        WallLayer("", 0.1)
    with pytest.raises(ValueError):
        WallLayer("Acabado", 0)


def test_wall_layers_must_match_total_thickness():
    layers = [WallLayer("Core", 0.15), WallLayer("Finish", 0.04)]
    with pytest.raises(ValueError):
        Wall((0, 0), (2, 0), thickness=0.20, layers=layers)


def test_wall_accepts_valid_composite_layers():
    layers = [
        WallLayer("Exterior", 0.025, function="finish"),
        WallLayer("Core", 0.15, function="core"),
        WallLayer("Interior", 0.025, function="finish"),
    ]
    wall = Wall((0, 0), (2, 0), thickness=0.20, layers=layers)
    assert wall.layers == tuple(layers)
    assert wall.properties.get("layer_count") == 3


def test_set_layers_updates_revision_once():
    wall = Wall((0, 0), (2, 0), thickness=0.20)
    layers = [WallLayer("Core", 0.20)]
    assert wall.set_layers(layers)
    assert wall.revision == 1
    assert wall.set_layers(layers) is False


def test_thickness_change_requires_layer_policy():
    wall = Wall(
        (0, 0),
        (2, 0),
        thickness=0.20,
        layers=[WallLayer("Core", 0.20)],
    )
    with pytest.raises(ValueError):
        wall.set_thickness(0.25)
    assert wall.set_thickness(0.25, clear_layers=True)
    assert wall.layers == ()


def test_layer_materials_are_registered_by_role():
    concrete = MaterialRef("mat-concrete", "Concrete", "core")
    wall = Wall((0, 0), (2, 0), thickness=0.20)
    wall.set_layers([WallLayer("Core", 0.20, concrete, "structure")])
    material = wall.materials.get("wall_layer_0:structure")
    assert material is not None
    assert material.material_id == "mat-concrete"


def test_snapshot_contains_geometry_quantities_and_ifc():
    wall = Wall((0, 0), (5, 0), height=3, thickness=0.2)
    snapshot = wall.snapshot()
    assert snapshot["geometry"]["start"] == (0.0, 0.0, 0.0)
    assert snapshot["quantities"]["gross_volume"] == pytest.approx(3.0)
    assert snapshot["ifc_class"] == "IfcWall"
