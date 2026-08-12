"""Stable identity generation and syntax validation for engineering objects."""
from __future__ import annotations
import re, uuid

OBJECT_ID = re.compile(r"^EO-[A-Z0-9]{8}$")

class EngineeringIdentityService:
    """Issue compact unique object identifiers and validate their canonical form."""
    def new_id(self) -> str:
        """Issue an uppercase EO identifier from a random UUID prefix."""
        return "EO-" + uuid.uuid4().hex[:8].upper()

    def validate(self, object_id: str) -> bool:
        """Check an object identifier against the canonical EO syntax."""
        return bool(OBJECT_ID.fullmatch(object_id))
