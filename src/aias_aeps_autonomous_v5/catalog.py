"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
import json
from pathlib import Path
from .models import AssetRecord

class PersistentAssetCatalog:
    """Execute the public PersistentAssetCatalog operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def __init__(self, path: Path) -> None:
        self.path = path
        self.assets: dict[str, AssetRecord] = {}
        if path.exists():
            self.load()

    def add(self, asset: AssetRecord) -> None:
        """Add add to autonomous engineering planning and controlled execution while enforcing identity constraints."""
        if asset.asset_id in self.assets:
            raise ValueError(f"Duplicate asset: {asset.asset_id}")
        self.assets[asset.asset_id] = asset

    def find_reusable(self, domain: str, asset_type: str) -> tuple[AssetRecord, ...]:
        """Return reusable from autonomous engineering planning and controlled execution using deterministic lookup rules."""
        return tuple(
            a for a in self.assets.values()
            if a.reusable and a.domain == domain and a.asset_type == asset_type
        )

    def save(self) -> None:
        """Persist save for autonomous engineering planning and controlled execution in its stable external representation."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([
            {
                "asset_id": a.asset_id,
                "asset_type": a.asset_type,
                "domain": a.domain,
                "version": a.version,
                "payload": a.payload,
                "reusable": a.reusable,
            }
            for a in self.assets.values()
        ], indent=2), encoding="utf-8")

    def load(self) -> None:
        """Load load for autonomous engineering planning and controlled execution while preserving typed state."""
        self.assets.clear()
        for row in json.loads(self.path.read_text(encoding="utf-8")):
            asset = AssetRecord(**row)
            self.assets[asset.asset_id] = asset
