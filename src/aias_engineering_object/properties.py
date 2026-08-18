"""Non-destructive operations for extensible engineering property dictionaries."""
from __future__ import annotations

class PropertySystem:
    """Set, retrieve, require and merge named engineering properties."""
    def set(self, properties: dict, key: str, value):
        """Assign a property after rejecting an empty key."""
        if not key.strip():
            raise ValueError("empty_property_key")
        properties[key] = value

    def get(self, properties: dict, key: str, default=None):
        """Return a property value or caller-provided default."""
        return properties.get(key, default)

    def require(self, properties: dict, keys: list[str]) -> list[str]:
        """Return required property keys absent from the mapping."""
        return [key for key in keys if key not in properties]

    def merge(self, base: dict, overlay: dict) -> dict:
        """Return a new mapping where overlay values take precedence."""
        result = dict(base)
        result.update(overlay)
        return result
