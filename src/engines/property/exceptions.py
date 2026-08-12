"""Excepciones públicas del Property Engine."""


class PropertyError(Exception):
    """Error base del motor de propiedades."""


class PropertyValidationError(PropertyError, ValueError):
    """El valor no cumple la definición o sus validadores."""


class PropertyNotFoundError(PropertyError, KeyError):
    """No existe la definición o el valor solicitado."""


class DuplicatePropertyError(PropertyError, ValueError):
    """Ya existe una propiedad con la misma clave."""


class PropertyReadOnlyError(PropertyError, PermissionError):
    """Se intentó modificar una propiedad de solo lectura."""


class UnitConversionError(PropertyError, ValueError):
    """No se pudo convertir entre las unidades solicitadas."""
