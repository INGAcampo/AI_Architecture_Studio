from uuid import UUID

import pytest

from engines.bim.object_model import (
    BimObject,
    MaterialContainer,
    MaterialRef,
    ObjectId,
    ObjectState,
    ObjectType,
    PropertyContainer,
    Relationship,
    RelationshipManager,
    RelationshipType,
)


def test_object_id_is_unique():
    assert ObjectId.new() != ObjectId.new()


def test_object_id_roundtrip():
    original = ObjectId.new()
    assert ObjectId.parse(str(original)) == original
    assert isinstance(original.value, UUID)


def test_bim_object_defaults():
    obj = BimObject("Elemento")
    assert obj.object_type is ObjectType.GENERIC
    assert obj.state is ObjectState.ACTIVE
    assert obj.revision == 0


def test_bim_object_rejects_blank_name():
    with pytest.raises(ValueError):
        BimObject("  ")


def test_rename_increments_revision_only_on_change():
    obj = BimObject("A")
    assert obj.rename("A") is False
    assert obj.rename("B") is True
    assert obj.revision == 1


def test_state_transitions_increment_revision():
    obj = BimObject("A")
    assert obj.set_state(ObjectState.HIDDEN)
    assert obj.state is ObjectState.HIDDEN
    assert obj.revision == 1


def test_deleted_object_cannot_reactivate():
    obj = BimObject("A")
    obj.set_state(ObjectState.DELETED)
    with pytest.raises(ValueError):
        obj.set_state(ObjectState.ACTIVE)


def test_property_container_rejects_blank_key():
    values = PropertyContainer()
    with pytest.raises(ValueError):
        values.set("", 1)


def test_property_container_detects_redundant_value():
    values = PropertyContainer()
    assert values.set("height", 3.0)
    assert values.set("height", 3.0) is False


def test_property_snapshot_is_read_only():
    values = PropertyContainer({"height": 3.0})
    snapshot = values.snapshot()
    with pytest.raises(TypeError):
        snapshot["height"] = 4.0


def test_bim_object_property_change_updates_revision():
    obj = BimObject("Muro", ObjectType.WALL)
    assert obj.set_property("height", 3.2)
    assert obj.revision == 1
    assert obj.set_property("height", 3.2) is False
    assert obj.revision == 1


def test_material_ref_validates_identity():
    with pytest.raises(ValueError):
        MaterialRef("", "Concreto")


def test_material_container_replaces_by_role():
    first = MaterialRef("m1", "Concreto", "core")
    second = MaterialRef("m2", "Mampostería", "core")
    container = MaterialContainer([first])
    assert container.add(second)
    assert container.get("core") == second
    assert len(container) == 1


def test_material_change_updates_object_revision():
    obj = BimObject("Losa", ObjectType.SLAB)
    assert obj.add_material(MaterialRef("m1", "Concreto", "core"))
    assert obj.revision == 1


def test_relationship_rejects_self_reference():
    object_id = ObjectId.new()
    with pytest.raises(ValueError):
        Relationship(object_id, object_id, RelationshipType.CONTAINS)


def test_relationship_manager_prevents_duplicates():
    manager = RelationshipManager()
    relation = Relationship(ObjectId.new(), ObjectId.new(), RelationshipType.HOSTS)
    assert manager.add(relation)
    assert manager.add(relation) is False
    assert len(manager) == 1


def test_relationship_manager_queries_direction():
    manager = RelationshipManager()
    source, target = ObjectId.new(), ObjectId.new()
    relation = Relationship(source, target, RelationshipType.CONTAINS)
    manager.add(relation)
    assert manager.outgoing(source) == (relation,)
    assert manager.incoming(target) == (relation,)


def test_relationship_manager_filters_type():
    manager = RelationshipManager()
    source = ObjectId.new()
    a = Relationship(source, ObjectId.new(), RelationshipType.CONTAINS)
    b = Relationship(source, ObjectId.new(), RelationshipType.REFERENCES)
    manager.add(a)
    manager.add(b)
    assert manager.outgoing(source, RelationshipType.CONTAINS) == (a,)


def test_relationship_manager_remove_object_cleans_both_directions():
    manager = RelationshipManager()
    center, a, b = ObjectId.new(), ObjectId.new(), ObjectId.new()
    manager.add(Relationship(center, a, RelationshipType.CONTAINS))
    manager.add(Relationship(b, center, RelationshipType.REFERENCES))
    assert manager.remove_object(center) == 2
    assert len(manager) == 0


def test_snapshot_contains_stable_foundation_fields():
    obj = BimObject("Nivel 1", ObjectType.LEVEL, metadata={"code": "L01"})
    obj.set_property("elevation", 0.0)
    snapshot = obj.snapshot()
    assert snapshot["id"] == str(obj.id)
    assert snapshot["object_type"] == "level"
    assert snapshot["metadata"]["code"] == "L01"
    assert snapshot["properties"]["elevation"] == 0.0
