"""Lossless JSON persistence for nested engineering-object aggregates."""
from __future__ import annotations
import json
from pathlib import Path
from .models import EngineeringObject, EngineeringState, Material, Load

class EngineeringObjectSerializer:
    """Serialize objects to readable JSON and reconstruct their typed nested records."""
    def save(self, obj: EngineeringObject, path: Path) -> Path:
        """Persist the complete object aggregate as readable UTF-8 JSON."""
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(obj.to_dict(),indent=2,ensure_ascii=False),encoding="utf-8")
        return path

    def load(self, path: Path) -> EngineeringObject:
        """Reconstruct nested material, load and lifecycle records from JSON."""
        data=json.loads(path.read_text(encoding="utf-8"))
        data["materials"]=[Material(**m) for m in data["materials"]]
        data["loads"]=[Load(**l) for l in data["loads"]]
        data["state"]=EngineeringState(**data["state"])
        return EngineeringObject(**data)
