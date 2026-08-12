"""AIAS Level 2 canonical BIM vertical-slice integration."""
from .model import BimProjectState, Wall, Opening, Room
from .service import VerticalSliceService
from .authority import AUTHORITY_MAP, AuthorityResolver

__all__ = [
    "AUTHORITY_MAP", "AuthorityResolver", "BimProjectState",
    "Opening", "Room", "VerticalSliceService", "Wall",
]
