"""Lossless JSON persistence for nested typed foundation aggregates."""
from __future__ import annotations
import json
from pathlib import Path
from .models import FoundationObject, FoundationGeometry, SoilProfile, ColumnSupport
from .enums import FoundationType, ShapeType

class FoundationSerializer:
    """Save readable foundation JSON and reconstruct enums and nested records."""
    def save(self, obj: FoundationObject, path: Path) -> Path:
        """Persist a foundation aggregate as readable JSON."""
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(obj.to_dict(),indent=2),encoding="utf-8")
        return path

    def load(self, path: Path) -> FoundationObject:
        """Reconstruct enums, geometry, soil and support records from JSON."""
        d=json.loads(path.read_text(encoding="utf-8"))
        d["foundation_type"]=FoundationType(d["foundation_type"])
        d["geometry"]["shape"]=ShapeType(d["geometry"]["shape"])
        d["geometry"]=FoundationGeometry(**d["geometry"])
        d["soil"]=SoilProfile(**d["soil"])
        d["supports"]=[ColumnSupport(**s) for s in d["supports"]]
        return FoundationObject(**d)
