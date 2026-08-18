"""Boundary adapters for AEKS calculation knowledge and enterprise registration."""
from __future__ import annotations
import json
from pathlib import Path

class AEKSCalculationKnowledgeAdapter:
    """Load CKU JSON only when its executable knowledge contract is complete."""
    def load_cku(self, path: Path) -> dict:
        """Load a calculation knowledge unit and enforce its mandatory fields."""
        data = json.loads(path.read_text(encoding="utf-8"))
        required = {"cku_id","title","method","inputs","outputs","traceability"}
        missing = required - data.keys()
        if missing:
            raise ValueError("missing_cku_fields:" + ",".join(sorted(missing)))
        return data

class EnterpriseRegistryAdapter:
    """Create stable calculation-asset registration records for enterprise consumers."""
    def registration_record(self, asset_id: str, asset_type: str, version: str, path: str) -> dict:
        """Build an active enterprise registration payload for a calculation asset."""
        return {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "version": version,
            "path": path,
            "status": "ACTIVE",
        }
