from __future__ import annotations

import json

import pytest

from engines.property import (
    DuplicatePropertyError,
    IfcMapping,
    ParameterBinding,
    ParameterDiscipline,
    ParameterScope,
    PropertyDefinition,
    PropertyService,
    PropertyType,
    SharedParameter,
    SharedParameterLibrary,
    StandardParameterCatalog,
)


def make_parameter(
    name: str = "AssetCode",
    guid: str = "asset-code-guid",
) -> SharedParameter:
    return SharedParameter(
        guid=guid,
        discipline=ParameterDiscipline.FACILITY,
        scope=ParameterScope.INSTANCE,
        tags=("asset", "facility"),
        definition=PropertyDefinition(name, PropertyType.TEXT),
        ifc_mapping=IfcMapping("Pset_ManufacturerTypeInformation", name),
    )


def test_shared_parameter_exposes_definition_metadata() -> None:
    parameter = make_parameter()

    assert parameter.name == "AssetCode"
    assert parameter.discipline is ParameterDiscipline.FACILITY
    assert parameter.ifc_mapping.property_name == "AssetCode"


def test_library_registers_by_guid_and_name_case_insensitively() -> None:
    library = SharedParameterLibrary()
    parameter = make_parameter()
    library.register(parameter)

    assert library.require(parameter.guid) is parameter
    assert library.require("assetcode") is parameter


def test_library_rejects_duplicate_name_or_guid() -> None:
    library = SharedParameterLibrary()
    library.register(make_parameter())

    with pytest.raises(DuplicatePropertyError):
        library.register(make_parameter(guid="another-guid"))


def test_category_binding_filters_parameters() -> None:
    library = SharedParameterLibrary()
    parameter = make_parameter()
    library.register(parameter)
    library.add_binding(
        ParameterBinding(
            parameter.guid,
            scope=ParameterScope.CATEGORY,
            categories=("Wall", "Door"),
        )
    )

    assert library.parameters_for(category="Wall") == (parameter,)
    assert library.parameters_for(category="Beam") == ()


def test_selection_binding_matches_only_selected_owner_ids() -> None:
    binding = ParameterBinding(
        "guid-01",
        scope=ParameterScope.SELECTION,
        target_ids=("wall-01", "wall-02"),
    )

    assert binding.applies_to(owner_id="wall-01") is True
    assert binding.applies_to(owner_id="wall-03") is False


def test_install_and_bind_owner_integrates_with_property_service() -> None:
    library = SharedParameterLibrary()
    parameter = make_parameter()
    library.register(parameter)
    service = PropertyService()

    library.install_into(service)
    bound = library.bind_owner(
        service,
        "door-01",
        values={"AssetCode": "D-001"},
    )

    assert len(bound) == 1
    assert service.get_value("door-01", "AssetCode") == "D-001"
    assert bound[0].source == "shared"


def test_library_round_trip_preserves_parameters_bindings_and_ifc(tmp_path) -> None:
    library = SharedParameterLibrary("Corporate Parameters")
    parameter = make_parameter()
    library.register(parameter)
    library.add_binding(
        ParameterBinding(
            parameter.guid,
            scope=ParameterScope.CATEGORY,
            categories=("Door",),
            required=True,
        )
    )

    path = library.save(tmp_path / "shared_parameters.json")
    restored = SharedParameterLibrary.load(path)

    restored_parameter = restored.require("AssetCode")
    assert restored.name == "Corporate Parameters"
    assert restored_parameter.guid == parameter.guid
    assert restored_parameter.ifc_mapping.property_set == (
        "Pset_ManufacturerTypeInformation"
    )
    assert restored.bindings[0].required is True


def test_saved_library_is_valid_utf8_json(tmp_path) -> None:
    library = StandardParameterCatalog.create()
    path = library.save(tmp_path / "catalog.json")

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "1.0"
    assert len(payload["parameters"]) >= 7


def test_standard_catalog_contains_cross_discipline_parameters() -> None:
    catalog = StandardParameterCatalog.create()

    assert catalog.require("FireRating").discipline is (
        ParameterDiscipline.ARCHITECTURE
    )
    assert catalog.require("ConcreteStrength").discipline is (
        ParameterDiscipline.STRUCTURAL
    )
    assert catalog.require("Flow").discipline is ParameterDiscipline.MEP
    assert catalog.require("UnitCost").discipline is ParameterDiscipline.COST


def test_standard_catalog_category_bindings_are_effective() -> None:
    catalog = StandardParameterCatalog.create()

    wall_names = {
        parameter.name
        for parameter in catalog.parameters_for(category="Wall")
    }
    beam_names = {
        parameter.name
        for parameter in catalog.parameters_for(category="Beam")
    }

    assert "FireRating" in wall_names
    assert "ThermalResistance" in wall_names
    assert "ConcreteStrength" not in wall_names
    assert "ConcreteStrength" in beam_names
