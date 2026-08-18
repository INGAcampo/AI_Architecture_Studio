from __future__ import annotations

from engines.bim import (
    BIM_SCHEMA_VERSION,
    BimCategory,
    BimDocument,
    BimElement,
    BimParameterSet,
    RelationshipType,
)


def test_bim_parameter_set_preserves_metadata() -> None:
    parameters = BimParameterSet()
    parameters.set(
        "Altura",
        3.0,
        unit="m",
        group="Geometría",
    )

    definition = parameters.get_definition("Altura")

    assert parameters["Altura"] == 3.0
    assert definition is not None
    assert definition.unit == "m"
    assert definition.group == "Geometría"


def test_bim_document_registers_and_filters_elements() -> None:
    document = BimDocument("Edificio A")
    wall = document.add_element(
        BimElement("Muro M-01", BimCategory.WALL, level_id="L1")
    )
    door = document.add_element(
        BimElement("Puerta P-01", BimCategory.DOOR, level_id="L1")
    )

    assert document.element_count == 2
    assert document.require_element(wall.element_id) is wall
    assert document.elements(category="Wall") == (wall,)
    assert {item.element_id for item in document.elements(level_id="L1")} == {wall.element_id, door.element_id}


def test_bim_relationships_are_explicit_and_validated() -> None:
    document = BimDocument()
    wall = document.add_element(BimElement("Muro", "Wall"))
    door = document.add_element(BimElement("Puerta", "Door"))

    relation = document.relate(
        wall.element_id,
        door.element_id,
        RelationshipType.HOSTS,
    )

    assert relation.relationship_type is RelationshipType.HOSTS
    assert document.relationship_count == 1
    assert document.relationships_for(wall.element_id) == (relation,)


def test_bim_document_round_trip() -> None:
    source = BimDocument(
        "Proyecto",
        metadata={"country": "VE", "units": "SI"},
    )
    level = source.add_element(BimElement("Nivel 1", "Storey"))
    wall = source.add_element(
        BimElement(
            "Muro",
            "Wall",
            level_id=level.element_id,
            parameters={"Espesor": 0.20},
        )
    )
    source.relate(level.element_id, wall.element_id, "contains")

    restored = BimDocument.from_dict(source.to_dict())

    assert restored.document_id == source.document_id
    assert restored.schema_version == BIM_SCHEMA_VERSION
    assert restored.element_count == 2
    assert restored.relationship_count == 1
    assert restored.require_element(wall.element_id).parameters["Espesor"] == 0.20


def test_existing_aias_object_can_be_adapted_without_mutation() -> None:
    class ExistingWall:
        id = "wall-existing-01"
        name = "Muro existente"
        object_type = "Wall"
        geometry = object()
        properties = {"Espesor": 0.25}

    source = ExistingWall()
    document = BimDocument()
    element = document.add_aias_object(source)

    assert element.element_id == source.id
    assert element.category is BimCategory.WALL
    assert element.parameters["Espesor"] == 0.25
    assert source.properties == {"Espesor": 0.25}
