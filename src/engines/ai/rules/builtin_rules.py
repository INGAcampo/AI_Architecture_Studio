from __future__ import annotations
from typing import Any, Iterable

from .issue import Issue, IssueSeverity
from .rule import Rule, RuleContext


def _value(element: Any, name: str, default: Any = None) -> Any:
    if isinstance(element, dict):
        return element.get(name, default)
    return getattr(element, name, default)


def _element_id(element: Any) -> str:
    value = (
        _value(element, "element_id")
        or _value(element, "object_id")
        or _value(element, "id")
        or _value(element, "guid")
    )
    return str(value or "unknown")


class DoorWidthRule(Rule):
    rule_id = "bim.door.minimum_width"
    name = "Door Minimum Width"
    description = "Valida el ancho mínimo de puertas."
    default_severity = IssueSeverity.ERROR
    tags = ("architecture", "accessibility", "door")

    def __init__(self, minimum_width: float = 0.80) -> None:
        if minimum_width <= 0:
            raise ValueError("minimum_width debe ser positivo")
        self.minimum_width = minimum_width

    def applies_to(self, element: Any, context: RuleContext) -> bool:
        kind = str(_value(element, "kind", _value(element, "type", ""))).lower()
        return kind == "door"

    def evaluate(self, element: Any, context: RuleContext) -> Iterable[Issue]:
        width = _value(element, "width")
        if width is None:
            return ()
        if float(width) < self.minimum_width:
            return (Issue(
                rule_id=self.rule_id,
                rule_name=self.name,
                severity=self.default_severity,
                element_id=_element_id(element),
                message=f"Ancho de puerta {width:.3f} m inferior a {self.minimum_width:.3f} m.",
                recommendation=f"Aumentar el ancho a por lo menos {self.minimum_width:.3f} m.",
            ),)
        return ()


class MissingMaterialRule(Rule):
    rule_id = "bim.element.missing_material"
    name = "Missing Material"
    description = "Detecta elementos sin material."
    default_severity = IssueSeverity.WARNING
    tags = ("bim", "materials")

    def evaluate(self, element: Any, context: RuleContext) -> Iterable[Issue]:
        material = _value(element, "material_id", _value(element, "material"))
        if material in (None, ""):
            return (Issue(
                rule_id=self.rule_id,
                rule_name=self.name,
                severity=self.default_severity,
                element_id=_element_id(element),
                message="El elemento no tiene material asignado.",
                recommendation="Asignar un material BIM válido.",
            ),)
        return ()


class DuplicateGuidRule(Rule):
    rule_id = "bim.element.duplicate_guid"
    name = "Duplicate GUID"
    description = "Detecta GUID repetidos en el proyecto."
    default_severity = IssueSeverity.CRITICAL
    tags = ("bim", "identity", "coordination")

    def evaluate(self, element: Any, context: RuleContext) -> Iterable[Issue]:
        guid = _value(element, "guid")
        if not guid:
            return ()
        project = context.project
        elements = (
            tuple(project.get("elements", ()))
            if isinstance(project, dict)
            else tuple(getattr(project, "elements", ()))
        )
        count = sum(_value(candidate, "guid") == guid for candidate in elements)
        if count > 1:
            return (Issue(
                rule_id=self.rule_id,
                rule_name=self.name,
                severity=self.default_severity,
                element_id=_element_id(element),
                message=f"GUID duplicado: {guid}.",
                recommendation="Regenerar el GUID para garantizar identidad única.",
                metadata={"guid": guid, "occurrences": count},
            ),)
        return ()


class InvalidLevelRule(Rule):
    rule_id = "bim.element.invalid_level"
    name = "Invalid Level"
    description = "Detecta referencias a niveles inexistentes."
    default_severity = IssueSeverity.ERROR
    tags = ("bim", "levels", "coordination")

    def evaluate(self, element: Any, context: RuleContext) -> Iterable[Issue]:
        level_id = _value(element, "level_id")
        if level_id in (None, ""):
            return ()
        valid_levels = set(context.metadata.get("valid_level_ids", ()))
        if valid_levels and level_id not in valid_levels:
            return (Issue(
                rule_id=self.rule_id,
                rule_name=self.name,
                severity=self.default_severity,
                element_id=_element_id(element),
                message=f"Nivel inexistente: {level_id}.",
                recommendation="Asignar el elemento a un nivel registrado.",
            ),)
        return ()


class EmptyPropertyRule(Rule):
    rule_id = "bim.element.empty_required_property"
    name = "Empty Required Property"
    description = "Valida propiedades obligatorias."
    default_severity = IssueSeverity.WARNING
    tags = ("bim", "properties")

    def __init__(self, required_properties: tuple[str, ...] = ("name",)) -> None:
        self.required_properties = tuple(required_properties)
        if not self.required_properties:
            raise ValueError("Debe existir al menos una propiedad requerida")

    def evaluate(self, element: Any, context: RuleContext) -> Iterable[Issue]:
        issues = []
        for property_name in self.required_properties:
            value = _value(element, property_name)
            if value in (None, ""):
                issues.append(Issue(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    severity=self.default_severity,
                    element_id=_element_id(element),
                    message=f"Propiedad obligatoria vacía: {property_name}.",
                    recommendation=f"Completar la propiedad {property_name}.",
                    metadata={"property": property_name},
                ))
        return tuple(issues)
