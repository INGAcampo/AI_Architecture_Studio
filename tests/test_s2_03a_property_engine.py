from __future__ import annotations

from datetime import date

import pytest

from engines.property import (
    AllowedValuesValidator,
    DuplicatePropertyError,
    PropertyDefinition,
    PropertyGroup,
    PropertyReadOnlyError,
    PropertyRegistry,
    PropertySerializer,
    PropertyService,
    PropertyType,
    PropertyValidationError,
    RangeValidator,
    UnitConversionError,
    UnitConverter,
)


def test_property_definition_coerces_and_validates_numeric_value() -> None:
    definition = PropertyDefinition(
        name="Thickness",
        display_name="Espesor",
        property_type=PropertyType.LENGTH,
        group=PropertyGroup.GEOMETRY,
        unit="m",
        default=0.20,
        validators=(RangeValidator(minimum=0.01, maximum=2.0),),
    )

    assert definition.validate("0.25") == 0.25
    assert definition.display_name == "Espesor"

    with pytest.raises(PropertyValidationError):
        definition.validate(3.0)


def test_registry_is_case_insensitive_and_rejects_duplicates() -> None:
    registry = PropertyRegistry()
    definition = PropertyDefinition("Material", PropertyType.MATERIAL)
    registry.register(definition)

    assert registry.require("material") is definition

    with pytest.raises(DuplicatePropertyError):
        registry.register(PropertyDefinition("MATERIAL", PropertyType.TEXT))


def test_property_service_binds_sets_and_snapshots_values() -> None:
    service = PropertyService()
    service.register_definition(
        PropertyDefinition("Height", PropertyType.LENGTH, unit="m")
    )
    service.register_definition(
        PropertyDefinition("Comments", PropertyType.TEXT)
    )

    service.bind_many("wall-01", {"Height": 3.0, "Comments": "Exterior"})
    previous = service.set_value("wall-01", "Height", 3.2)

    assert previous == 3.0
    assert service.get_value("wall-01", "Height") == 3.2
    assert service.snapshot("wall-01") == {
        "Height": 3.2,
        "Comments": "Exterior",
    }


def test_read_only_property_requires_explicit_force() -> None:
    service = PropertyService()
    service.register_definition(
        PropertyDefinition(
            "Area",
            PropertyType.AREA,
            unit="m²",
            read_only=True,
        )
    )
    service.bind("room-01", "Area", 12.0)

    with pytest.raises(PropertyReadOnlyError):
        service.set_value("room-01", "Area", 14.0)

    service.set_value("room-01", "Area", 14.0, force=True)
    assert service.get_value("room-01", "Area") == 14.0


def test_allowed_values_validator_supports_case_insensitive_text() -> None:
    definition = PropertyDefinition(
        "StructuralRole",
        PropertyType.ENUM,
        validators=(
            AllowedValuesValidator(
                ("Bearing", "Non-bearing"),
                case_sensitive=False,
            ),
        ),
    )

    assert definition.validate("bearing") == "bearing"

    with pytest.raises(PropertyValidationError):
        definition.validate("Decorative")


def test_default_unit_converter_handles_length_pressure_and_temperature() -> None:
    converter = UnitConverter()

    assert converter.convert(1.0, "m", "ft") == pytest.approx(
        3.280839895, rel=1e-8
    )
    assert converter.convert(1.0, "MPa", "psi") == pytest.approx(
        145.0377377, rel=1e-8
    )
    assert converter.convert(0.0, "°C", "°F") == pytest.approx(32.0)


def test_unit_converter_rejects_incompatible_dimensions() -> None:
    converter = UnitConverter()

    with pytest.raises(UnitConversionError):
        converter.convert(1.0, "m", "MPa")


def test_service_accepts_input_unit_and_stores_definition_unit() -> None:
    service = PropertyService()
    service.register_definition(
        PropertyDefinition("Length", PropertyType.LENGTH, unit="m")
    )
    service.bind("beam-01", "Length", 1.0)

    service.set_value("beam-01", "Length", 10.0, input_unit="ft")

    assert service.get_value("beam-01", "Length") == pytest.approx(3.048)


def test_date_values_are_coerced_and_serialized() -> None:
    definition = PropertyDefinition(
        "InspectionDate",
        PropertyType.DATE,
    )
    service = PropertyService()
    service.register_definition(definition)
    value = service.bind("column-01", "InspectionDate", "2026-07-23")

    assert value.value == date(2026, 7, 23)
    assert value.to_dict()["value"] == "2026-07-23"


def test_definition_serialization_round_trip_preserves_public_metadata() -> None:
    definition = PropertyDefinition(
        "FireRating",
        PropertyType.TEXT,
        display_name="Resistencia al fuego",
        group=PropertyGroup.IDENTITY,
        required=True,
        description="Clasificación del elemento.",
    )
    registry = PropertyRegistry()
    registry.register(definition)

    payload = PropertySerializer.definitions_to_dict(registry)
    restored = PropertySerializer.registry_from_dict(payload)
    restored_definition = restored.require("FireRating")

    assert restored_definition.display_name == "Resistencia al fuego"
    assert restored_definition.group is PropertyGroup.IDENTITY
    assert restored_definition.required is True
